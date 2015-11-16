#!/usr/bin/env python
# encoding: utf-8


import struct
import socket

import urllib2


from efl import ecore, ecore_con
from efl import elementary as elm


class UrlSimple(ecore_con.Url):
    def __init__(self, url, done_cb=None, prog_cb=None, **kargs):

        self.done_cb = done_cb
        self.kargs = kargs
        self.received_data = []

        ecore_con.Url.__init__(self, url)
        self.on_complete_event_add(self._complete_cb)
        self.on_data_event_add(self._data_cb)
        if prog_cb is not None:
            self.on_progress_event_add(prog_cb)

    def _complete_cb(self, event):
        data = ''.join(self.received_data)
        self.done_cb(event.url, event.status, data, **self.kargs)
        
        self.delete()

    def _data_cb(self, event):
        self.received_data.append(event.data)


class UPnP_Host(object):
    def __init__(self, uuid, xml_url):
        print("VALID!!! " + uuid)
        self.uuid = uuid
        self.xml_url = xml_url

        self.request_xml()

    # XML stuff...
    def _xml_complete(self, url, status, data):
        print("@@@@@@@@@@@")
        print(url)
        print(status)
        print(data)

    def request_xml(self):
        u = UrlSimple(self.xml_url, self._xml_complete)
        u.additional_header_add('USER-AGENT', 'UPnP/2.0')
        u.additional_header_add('CONTENT-TYPE','text/xml; charset="utf-8"')
        u.get()


class UPnP_Network(object):
    def __init__(self):

        self.ip = '239.255.255.250'
        self.port = 1900
        self.hosts = {} # uuid -> UPnP_Host
        self._ssock = None
        self._csock = None

        self.listen_on_the_multicast_group()
        self.perform_an_msearch_discover()

    def parse_ssdp(self, data):
        known = ('M-SEARCH', 'NOTIFY', 'HTTP/1.1')
        if not data.startswith(known):
            print("Unknown ssdp header %s" % data)
            return None

        lines = data.split('\r\n')
        header = lines.pop(0)
        res = {}
        for line in lines:
            if line:
                name, val = line.split(':', 1)
                res[name.strip().upper()] = val.strip()

        return (header, res)

    def listen_on_the_multicast_group(self):
        #Set up server socket
        self._ssock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self._ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # BSD systems also need to set SO_REUSEPORT     
        try:
            self._ssock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        except:
            pass

        #Only bind to this interface
        # if self.IFACE != None:
            # print '\nBinding to interface',self.IFACE,'...\n'
            # self._ssock.setsockopt(SOL_SOCKET,IN.SO_BINDTODEVICE,struct.pack("%ds" % (len(self.IFACE)+1,), self.IFACE))
            # self._csock.setsockopt(SOL_SOCKET,IN.SO_BINDTODEVICE,struct.pack("%ds" % (len(self.IFACE)+1,), self.IFACE))

        try:
            self._ssock.bind(('', self.port))
        except Exception, e:
            print("WARNING: Failed to bind %s:%d: %s" , (self.ip, self.port, e))
        else:
            print("BIND OK")

        try:
            # needed to join a multicast group
            mreq = struct.pack("4sl", socket.inet_aton(self.ip), socket.INADDR_ANY)
            self._ssock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except Exception, e:
            print('WARNING: Failed to join multicast group:', e)
        else:
            print("MULTICAST OK")
            
        ecore.FdHandler(self._ssock, ecore.ECORE_FD_READ | ecore.ECORE_FD_ERROR,
                                    self._multicast_group_data_cb, self._ssock)

    def _multicast_group_data_cb(self, fdh, sock):

        header, ssdp = self.parse_ssdp(sock.recv(2048))
        print(header + " -> " + str(ssdp))
        return ecore.ECORE_CALLBACK_RENEW

    def perform_an_msearch_discover(self):
        request = 'M-SEARCH * HTTP/1.1\r\n' \
                  'HOST: 239.255.255.250:1900\r\n' \
                  'MAN: "ssdp:discover"\r\n' \
                  'MX: 1\r\n' \
                  'ST: upnp:rootdevice\r\n' \
                  '\r\n'
                  # TODO:
                  # USER-AGENT: OS/version UPnP/2.0 product/version
                  # CPFN.UPNP.ORG: friendly name of the control point
                  # CPUUID.UPNP.ORG: uuid of the control point

        # Set up client socket
        self._csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._csock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        ecore.FdHandler(self._csock, ecore.ECORE_FD_READ | ecore.ECORE_FD_ERROR,
                                     self._msearch_data_cb, self._csock)
        self._csock.sendto(request, (self.ip, self.port))

        # TODO: resend again in a short time (maybe 2/3 times)
        # TODO: close the socket !!

    def _msearch_data_cb(self, fdh, sock):
        if fdh.has_error():
            print("ERROR")
            return ecore.ECORE_CALLBACK_CANCEL

        data = sock.recv(2048)
        header, ssdp = self.parse_ssdp(data)
        print(header + " -> " + str(ssdp))

        if ssdp and 'LOCATION' in ssdp and 'USN' in ssdp:
            uuid = ssdp['USN'] # TODO strip "uuid:" ??
            xml_url = ssdp['LOCATION']
            if not uuid in self.hosts:
                self.hosts[uuid] = UPnP_Host(uuid, xml_url)

        
        return ecore.ECORE_CALLBACK_RENEW


if __name__ == '__main__':
    n = UPnP_Network()

    elm.run()
