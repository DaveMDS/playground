#!/usr/bin/env python
# encoding: utf-8


import struct
from socket import *


#UPNP class for getting, sending and parsing SSDP/SOAP XML data (among other things...)
class UPnP(object):
    ip = False
    port = False
    completer = False
    msearchHeaders = {
        'MAN' : '"ssdp:discover"',
        'MX'  : '2'
    }
    DEFAULT_IP = "239.255.255.250"
    DEFAULT_PORT = 1900
    UPNP_VERSION = '1.0'
    MAX_RECV = 8192
    MAX_HOSTS = 0
    TIMEOUT = 0
    HTTP_HEADERS = []
    ENUM_HOSTS = {}
    VERBOSE = False
    UNIQ = False
    DEBUG = False
    LOG_FILE = False
    BATCH_FILE = None
    IFACE = None
    STARS = '****************************************************************'

    csock = False
    ssock = False

    # def __init__(self,ip,port,iface,appCommands):
    def __init__(self):
        self.initSockets()
        
    #Initialize default sockets
    # def initSockets(self,ip,port,iface):
    def initSockets(self):
        if self.csock:
            self.csock.close()
        if self.ssock:
            self.ssock.close()

        self.port = self.DEFAULT_PORT
        self.ip = self.DEFAULT_IP
        
        try:
            #This is needed to join a multicast group
            self.mreq = struct.pack("4sl", inet_aton(self.ip), INADDR_ANY)

            #Set up client socket
            self.csock = socket(AF_INET, SOCK_DGRAM)
            self.csock.setsockopt(IPPROTO_IP, IP_MULTICAST_TTL, 2)
            
            #Set up server socket
            self.ssock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
            self.ssock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

            # BSD systems also need to set SO_REUSEPORT     
            # try:
            self.ssock.setsockopt(SOL_SOCKET, SO_REUSEPORT, 1)
            # except:
                # pass

            #Only bind to this interface
            # if self.IFACE != None:
                # print '\nBinding to interface',self.IFACE,'...\n'
                # self.ssock.setsockopt(SOL_SOCKET,IN.SO_BINDTODEVICE,struct.pack("%ds" % (len(self.IFACE)+1,), self.IFACE))
                # self.csock.setsockopt(SOL_SOCKET,IN.SO_BINDTODEVICE,struct.pack("%ds" % (len(self.IFACE)+1,), self.IFACE))

            try:
                self.ssock.bind(('', self.port))
            except Exception, e:
                print("WARNING: Failed to bind %s:%d: %s" , (self.ip, self.port, e))

            try:
                self.ssock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, self.mreq)
            except Exception, e:
                print('WARNING: Failed to join multicast group:', e)

        except Exception, e:
            print("Failed to initialize UPNP sockets:", e)
            return False

        return True

    #Send network data
    def send(self, data, socket):
        #By default, use the client socket that's part of this class
        if socket == False:
            socket = self.csock
        try:
            socket.sendto(data, (self.ip, self.port))
            return True
        except Exception, e:
            print("SendTo method failed for %s:%d : %s" % (self.ip, self.port, e))
            return False
            
    #Actively search for UPNP devices
    def msearch(self):
        defaultST = "upnp:rootdevice"
        st = "schemas-upnp-org"
        myip = ''
        # lport = hp.port

        # if argc >= 3:
            # if argc == 4:
                # st = argv[1]
                # searchType = argv[2]
                # searchName = argv[3]
            # else:
                # searchType = argv[1]
                # searchName = argv[2]
            # st = "urn:%s:%s:%s:%s" % (st,searchType,searchName,hp.UPNP_VERSION.split('.')[0])
        # else:
            # st = defaultST
        st = defaultST

        #Build the request
        request = 'M-SEARCH * HTTP/1.1\r\n' \
                  'HOST:%s:%d\r\n' \
                  'ST:%s\r\n' % (self.ip, self.port, st)

        for header, value in self.msearchHeaders.iteritems():
            request += header + ':' + value + "\r\n"
        request += "\r\n" 

        print("Entering discovery mode for '%s', Ctl+C to stop..." % st)


        #Have to create a new socket since replies will be sent directly to our IP, not the multicast IP
        # server = hp.createNewListener(myip,lport)
        # if server == False:
            # print 'Failed to bind port %d' % lport
            # return

        self.send(request, server)
        count = 0
        start = time.time()

        while True:
            try:
                if self.MAX_HOSTS > 0 and count >= self.MAX_HOSTS:
                    break

                if self.TIMEOUT > 0 and (time.time() - start) > self.TIMEOUT:
                    raise Exception("Timeout exceeded")

                # if hp.parseSSDPInfo(hp.recv(1024,server),False,False):
                    # count += 1

            except Exception, e:
                print('\nDiscover mode halted...')
                break
