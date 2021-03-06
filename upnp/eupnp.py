#!/usr/bin/env python
# encoding: utf-8

import os
import struct
import socket

# import urllib2
from xml.etree import ElementTree
# import xml.dom.minidom
from pprint import pprint

from efl import ecore, ecore_con
from efl.ecore import ECORE_CALLBACK_CANCEL, ECORE_CALLBACK_RENEW
from efl import elementary as elm


__all__ = ['UPnP_Network', 'UPnP_Device', 'UPnP_Service',
           'UPNP_EVENT_DEVICE_FOUND', 'UPNP_EVENT_DEVICE_GONE',
           'UPNP_EVENT_SERVICE_FOUND', 'UPNP_EVENT_SERVICE_GONE']


#-----  Utils -----------------------------------------------------------------
from collections import defaultdict


def strip_ns(s):
    if s.startswith('{') and '}' in s:
        return s.split('}')[1]
    return s


def etree_to_dict2(t):

    tag = strip_ns(t.tag)

    d = {tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict2, children):
            for k, v in dc.iteritems():
                dd[strip_ns(k)].append(v)
        d = {tag: {k:v[0] if len(v) == 1 else v for k, v in dd.iteritems()}}
    if t.attrib:
        d[tag].update(('@' + k, v) for k, v in t.attrib.iteritems())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
              d[tag]['#text'] = text
        else:
            d[tag] = text
    return d


def split_usn(usn):
    """ Utility function to split the USN into UUID and URN

    USN:  "uuid:20102adc-7298-5948-1d49-51836164fec2::urn:schemas-upnp-org:service:ConnectionManager:1"
    UUID: "20102adc-7298-5948-1d49-51836164fec2"
    URN:  "schemas-upnp-org:service:ConnectionManager:1"
    """
    uuid, urn = usn.split('::', 1)
    if uuid and uuid.startswith('uuid:'):
        uuid = uuid[5:]
    if urn and urn.startswith('urn:'):
        urn = urn[4:]

    return uuid, urn


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

#-------------

class UPnP_Service(object):
    def __init__(self, parent_device, usn, xml_url, control_url, event_url):
        self._device = parent_device
        self._usn = usn
        
        self._xml_url = xml_url
        self.control_url = control_url
        self.event_url = event_url

        self.request_xml()

    def __str__(self):
        return "<UPnP_Service '{}' at '{}'>".format(
                self.urn, self._device.name)

    @property
    def parent_device(self):
        """ Parent UPnP_Device instance """
        return self._device

    @property
    def usn(self):
        """ uuid:20102adc-7298-5948-1d49-51836164fec2::urn:schemas-upnp-org:service:ContentDirectory:1 """
        return self._usn

    @property
    def uuid(self):
        """ 20102adc-7298-5948-1d49-51836164fec2 """
        return split_usn(self._usn)[0]

    @property
    def urn(self):
        """ schemas-upnp-org:service:ContentDirectory:1 """
        return split_usn(self._usn)[1]

    @property
    def type(self):
        """ ContentDirectory:1 """
        return ':'.join(self._usn.split(':')[-2:])

    # XML stuff...
    def request_xml(self):
        # if self._device._net.verbose_xml:
            # print("XML request Service info from: '{}'".format(self._xml_url))
        u = UrlSimple(self._xml_url, self._xml_complete)
        u.additional_header_add('USER-AGENT', 'UPnP/2.0')
        u.additional_header_add('CONTENT-TYPE','text/xml; charset="utf-8"')
        u.get()

    def _xml_complete(self, url, status, data):
        # if self._device._net.verbose_xml:
            # print("XML Device done {} {}".format(status, url if status != 200 else ''))

        # print(data)
        # print("========================================")
        # pass

        # emit the event
        self._device._net.event_callbacks_call(UPNP_EVENT_SERVICE_FOUND, self)

class UPnP_Icon(object):
    def __init__(self, url, mimetype, width, height, depth):
        self.url = url
        self.mimetype = mimetype
        self.width = int(width)
        self.height = int(height)
        self.depth = int(depth)

    def __str__(self):
        return "<UPnP_Icon at {} [{}x{}]>".format(self.url, self.width, self.height)

        
class UPnP_Device(object):
    def __init__(self, net, usn, xml_url):
        self._net = net
        self._usn = usn
        self._xml_url = xml_url
        self._xml_received = False
        self._base_url = ''

        self.device_info = {} # raw device info from xml
        self.services = {}    # usn -> UPnP_Service
        self.icons = []       # UPnP_Icon instances

        self.request_xml()

    def __str__(self):
        if self._xml_received:
            return "<UPnP_Device '{}' USN:'{}'>".format(
                   self.name, self.usn)
        else:
            return "<UPnP_Device !!NOT READY!! USN:'{}'>".format(self.usn)

    @property
    def usn(self):
        """ uuid:3553f223-fa6f-5e58-8b2f-bd5a9d5d2197::urn:schemas-upnp-org:device:MediaServer:1 """
        return self._usn

    @property
    def uuid(self):
        """ 3553f223-fa6f-5e58-8b2f-bd5a9d5d2197 """
        return split_usn(self._usn)[0]

    @property
    def urn(self):
        """ schemas-upnp-org:device:MediaServer:1 """
        return split_usn(self._usn)[1]

    @property
    def type(self):
        """ MediaServer:1 """
        return ':'.join(self._usn.split(':')[-2:])

    @property
    def name(self):
        return self.device_info.get('friendlyName')

    ###
    # @property
    # def device_type(self):
        # return self.device_info.get('deviceType')

    # @property
    # def friendly_name(self):
        # return self.device_info.get('friendlyName')

    @property
    def manufacturer(self):
        return self.device_info.get('manufacturer')

    @property
    def manufacturer_url(self):
        return self.device_info.get('manufacturerURL')

    @property
    def model_name(self):
        return self.device_info.get('modelName')

    @property
    def model_number(self):
        return self.device_info.get('modelNumber')

    @property
    def model_url(self):
        return self.device_info.get('modelURL')

    @property
    def serial_number(self):
        return self.device_info.get('serialNumber')

    @property
    def bigger_icon_url(self):
        if self.icons:
            return self.icons[0].url

    # XML stuff...
    def request_xml(self):
        if self._net.verbose_xml:
            print("XML request Device info from: '{}'".format(self._xml_url))

        u = UrlSimple(self._xml_url, self._xml_complete)
        u.additional_header_add('USER-AGENT', 'UPnP/2.0')
        u.additional_header_add('CONTENT-TYPE','text/xml; charset="utf-8"')
        u.get()

    def _xml_complete(self, url, status, data):
        if self._net.verbose_xml:
            print("XML Device done {} {}".format(status, url if status != 200 else ''))

        if status != 200:
            return

        ns = '{urn:schemas-upnp-org:device-1-0}'
        root = ElementTree.fromstring(data)
        # print(root)

        # honor the old URLBase spec (or use the xml base path)
        node = root.find(ns+'URLBase')
        if node is not None:
            self._base_url = node.text
        else:
            self._base_url = os.path.dirname(self._xml_url)

        # build a dict of the whole <device> tag
        device = root.find(ns+'device')
        device_info = etree_to_dict2(device)
        device_info = device_info['device'] # :/


        # handle services
        services = device_info['serviceList']['service']
        if not isinstance(services, list):
            services = [services]
        for service in services:
            usn = 'uuid:{}::{}'.format(self.uuid, service['serviceType'])
            if not usn in self.services:
                s = UPnP_Service(self, usn,
                                 # service['serviceType'],
                                 self._fix_base_url(service['SCPDURL']),
                                 self._fix_base_url(service['controlURL']),
                                 self._fix_base_url(service['eventSubURL']))
                self.services[usn] = s
        del device_info['serviceList']


        # handle icons
        if 'iconList' in device_info:
            icons = device_info['iconList']['icon']
            if not isinstance(icons, list):
                icons = [icons]
            for ic in icons:
                # only keep png icons (that are mandatory)
                if ic['mimetype'] == 'image/png':
                    ic['url'] = self._fix_base_url(ic['url'])
                    self.icons.append(UPnP_Icon(**ic))
            self.icons.sort(key=lambda i: i.width, reverse=True)
            del device_info['iconList']


        # finalize and emit the user event
        self._xml_received = True
        self.device_info = device_info
        self._net.event_callbacks_call(UPNP_EVENT_DEVICE_FOUND, self)

    def _fix_base_url(self, url):
        if url.startswith(self._base_url):
            return url
        if not self._base_url.endswith('/') and not url.startswith('/'):
            return self._base_url + '/' + url
        return self._base_url + url

#-------------

class SSDP_Network(object):
    def __init__(self, ip='239.255.255.250', port=1900, verbose=True):
        self.ip = ip
        self.port = port
        self.verbose = verbose
        self.VALID_SSDP_HEADERS = ('NOTIFY * HTTP/1.1',
                                   'M-SEARCH * HTTP/1.1',
                                   'HTTP/1.1 200 OK')

        self._ssock = None # TODO close / keep up
        self._csock = None # TODO close / keep up
        self._expire_timers = {} # key:USN  val:Timer()

        self.listen_on_the_multicast_group()
        self.perform_an_msearch_discover()

    def shutdown(self):
        # TODO
        pass

    def ssdp_device_found(self, device_info):
        raise NotImplemented('ssdp_device_found')

    def ssdp_device_gone(self, usn):
        raise NotImplemented('ssdp_device_gone')

    def ssdp_service_found(self, service_info):
        raise NotImplemented('ssdp_service_found')

    def ssdp_service_gone(self, usn):
        raise NotImplemented('ssdp_service_gone')

    # msearch
    def perform_an_msearch_discover(self):
        request = 'M-SEARCH * HTTP/1.1\r\n' \
                  'HOST: 239.255.255.250:1900\r\n' \
                  'MAN: "ssdp:discover"\r\n' \
                  'MX: 1\r\n' \
                  'ST: ssdp:all\r\n' \
                  '\r\n'
                  # TODO:       # 'ST: upnp:rootdevice\r\n' \
                  # USER-AGENT: OS/version UPnP/2.0 product/version
                  # CPFN.UPNP.ORG: friendly name of the control point
                  # CPUUID.UPNP.ORG: uuid of the control point

        # Set up client socket
        self._csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._csock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
        ecore.FdHandler(self._csock, ecore.ECORE_FD_READ | ecore.ECORE_FD_ERROR,
                                     self._data_received_cb, self._csock)
        self._csock.sendto(request, (self.ip, self.port))

        # TODO: resend again in a short time (maybe 2/3 times)
        # TODO: close the socket !!

    # multicast listener
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
            if self.verbose:
                print("SSDP bind ok")

        try:
            # needed to join a multicast group
            mreq = struct.pack("4sl", socket.inet_aton(self.ip), socket.INADDR_ANY)
            self._ssock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        except Exception, e:
            print('WARNING: Failed to join multicast group:', e)
        else:
            if self.verbose:
                print("SSDP multicast ok")
            
        ecore.FdHandler(self._ssock, ecore.ECORE_FD_READ | ecore.ECORE_FD_ERROR,
                                    self._data_received_cb, self._ssock)

    def _data_received_cb(self, fdh, sock):
        """
        ON_REQUEST:
        ===========

        HTTP/1.1 200 OK
        {'CACHE-CONTROL': 'max-age=1800',
         'EXT': '',
         'LOCATION': 'http://192.168.1.5:55555/',
         'SERVER': 'POSIX, UPnP/1.0, Intel MicroStack/1.0.2547',
         'ST': 'urn:schemas-upnp-org:device:MediaServer:1',
         'USN': 'uuid:20102adc-7298-5948-1d49-51836164fec2::urn:schemas-upnp-org:device:MediaServer:1'}

        HTTP/1.1 200 OK
        {'CACHE-CONTROL': 'max-age=1800',
         'EXT': '',
         'LOCATION': 'http://192.168.1.5:55555/',
         'SERVER': 'POSIX, UPnP/1.0, Intel MicroStack/1.0.2547',
         'ST': 'urn:schemas-upnp-org:service:ConnectionManager:1',
         'USN': 'uuid:20102adc-7298-5948-1d49-51836164fec2::urn:schemas-upnp-org:service:ConnectionManager:1'}

        EVENTS:
        =======

        SSDP NOTIFY * HTTP/1.1
        {'CACHE-CONTROL': 'max-age=1800',
         'HOST': '239.255.255.250:1900',
         'LOCATION': 'http://192.168.1.254:8000/i63c3uv3a3o/WFA/WFA.xml',
         'NTS': 'ssdp:alive',
         'SERVER': 'Technicolor TG 582n 8.4.4.J UPnP/1.0 (08-76-FF-B5-93-D0)',
         'NT': 'urn:schemas-wifialliance-org:service:WFAWLANConfig:1',
         'USN': '8130585e-c641-5a85-a135-502774a7a34d::urn:schemas-wifialliance-org:service:WFAWLANConfig:1'}

        SSDP NOTIFY * HTTP/1.1
        {'CACHE-CONTROL': 'max-age=1800',
         'HOST': '239.255.255.250:1900',
         'LOCATION': 'http://192.168.1.5:50730/',
         'NTS': 'ssdp:alive',
         'SERVER': 'POSIX, UPnP/1.0, Intel MicroStack/1.0.2777',
         'NT': 'urn:schemas-upnp-org:device:WiNAS:1',
         'USN': 'uuid:0643d882-1fe4-5e1c-5cbd-6c004c0266d4::urn:schemas-upnp-org:device:WiNAS:1'}

        """
        if fdh.has_error():
            print("ERROR")
            return ECORE_CALLBACK_CANCEL

        # read packet from the socket and parse ssdp to dict
        try:
            data = sock.recv(2048)
            header, ssdp = self._ssdp_to_dict(data)
        except RuntimeError:
            print("ERROR")
            return ECORE_CALLBACK_RENEW

        if self.verbose:
            print("SSDP packet received: \n{}".format(data))


        # an m-search request?
        if header.startswith('M-SEARCH'):
            # TODO advertise our services
            return ECORE_CALLBACK_RENEW

        try:
            usn = ssdp['USN']
        except KeyError:
            return ECORE_CALLBACK_RENEW

        # hack to support USN not staring with 'uuid:' 
        if not usn.startswith('uuid:'):
            usn = 'uuid:' + usn
            ssdp['USN'] = usn

        # parse the USN
        usn, service_or_device, type = self._parse_usn(usn)
        if usn is None:
            return ECORE_CALLBACK_RENEW

        # extract max-age
        max_age = ssdp.get('CACHE-CONTROL')
        if max_age and max_age.startswith('max-age='):
            max_age = int(max_age[8:])
        else:
            max_age = None

        if ssdp.get('NTS') == 'ssdp:byebye':
            # clear the expire timer (if exists) and notify the user
            self._usn_expired_cb(usn, service_or_device)
        else: # ssdp:alive or M-SEARCH response
            if usn in self._expire_timers:
                # we know it, just renew the timer
                t = self._expire_timers[usn]
                t.interval = max_age
                t.reset()
            else:
                # a new service/device, send notification to the class user
                if service_or_device == 'service':
                    self.ssdp_service_found(ssdp)
                else:
                    self.ssdp_device_found(ssdp)
                # setup the expire timer
                self._expire_timers[usn] = \
                    ecore.Timer(max_age, self._usn_expired_cb, usn, service_or_device)

        return ECORE_CALLBACK_RENEW

    def _usn_expired_cb(self, usn, service_or_device):
        # print("EXPIRED " + usn)
        t = self._expire_timers.pop(usn, None)
        if t:
            t.delete()

            # send notification to the class user
            if service_or_device == 'service':
                self.ssdp_service_gone(usn)
            else:
                self.ssdp_device_gone(usn)
        
        return ECORE_CALLBACK_CANCEL
        
    def _parse_usn(self, usn):
        """
        USN can be in the following forms:
            (1) uuid:device-UUID    (IGNORED)
            (2) uuid:device-UUID::upnp:rootdevice    (IGNORED)
            (3) uuid:device-UUID::urn:schemas-upnp-org:device:deviceType:v
            (4) uuid:device-UUID::urn:schemas-upnp-org:service:serviceType:v
            (5) uuid:device-UUID::urn:domain-name:device:deviceType:v
            (6) uuid:device-UUID::urn:domain-name:service:serviceType:v
        """
        try:
            uuid, urn = usn.split('::')
            _, _, service_or_device, service_or_device_type = urn.split(':', 3)
        except:
            # print("UNPARSABLE USN: %s" % usn)
            return (None, None, None)

        return (usn, service_or_device, service_or_device_type)
        
    def _ssdp_to_dict(self, data):

        if not data.startswith(self.VALID_SSDP_HEADERS):
            raise RuntimeError("Unknown ssdp header: '{}'".format(data))

        if not data.endswith('\r\n\r\n'):
            raise RuntimeError("Incorrect ssdp termination: '{}'".format(data))

        lines = data.split('\r\n')
        header = lines.pop(0)
        if not header:
            raise RuntimeError("Invalid ssdp header")

        res = {}
        for line in lines:
            if not line:
                continue
            try:
                name, val = line.split(':', 1)
                res[name.strip().upper()] = val.strip()
            except:
                raise RuntimeError("Unparsable ssdp line: '{}'".format(data))

        return (header, res)





UPNP_EVENT_DEVICE_FOUND = 1
UPNP_EVENT_DEVICE_GONE = 2
UPNP_EVENT_SERVICE_FOUND = 3
UPNP_EVENT_SERVICE_GONE = 4

class UPnP_Network(SSDP_Network):
    
    def __init__(self, verbose_ssdp=False, verbose_xml=True):

        self.verbose_xml = verbose_xml
        self.devices = {}  # usn -> UPnP_Device

        self._events_cbs = [] # [(func, args, kargs),...]

        #######
        SSDP_Network.__init__(self, verbose=verbose_ssdp)

    def shutdown(self):
        # TODO !!
        SSDP_Network.shutdown(self)

    ###


    ###
    def events_callback_add(self, func, *args, **kargs):
        self._events_cbs.append((func, args, kargs))

    def events_callback_del(self, func, *args, **kargs):
        self._events_cbs.remove((func, args, kargs))

    def event_callbacks_call(self, event, obj):
        for func, args, kargs in self._events_cbs:
            func(self, event, obj, *args, **kargs)

    ###
    def ssdp_device_found(self, device_info):
        usn = device_info.get('USN')
        uuid, urn = split_usn(usn)
        self.devices[usn] = UPnP_Device(self, usn, device_info['LOCATION'])

    def ssdp_device_gone(self, usn):
        device = self.devices.pop(usn, None)
        if device:
            self.event_callbacks_call(UPNP_EVENT_DEVICE_GONE, device)

    def ssdp_service_found(self, service_info):
        # services are populated from the device xml...
        pass

    def ssdp_service_gone(self, usn):
        for _, device in self.devices.items():
            service = device.services.pop(usn, None)
            if service:
                self.event_callbacks_call(UPNP_EVENT_SERVICE_GONE, service)


# test

if __name__ == '__main__':

    def _on_events(net, event, obj):

        if event is UPNP_EVENT_DEVICE_FOUND:
            print("--- UPNP_DEVICE_FOUND:" + str(obj))

        elif event is UPNP_EVENT_DEVICE_GONE:
            print("--- UPNP_DEVICE_GONE:" + str(obj))

        elif event is UPNP_EVENT_SERVICE_FOUND:
            print("--- UPNP_SERVICE_FOUND:" + str(obj))
        
        elif event is UPNP_EVENT_SERVICE_GONE:
            print("--- UPNP_SERVICE_GONE:" + str(obj))

        else:
            print("--- UPNP UNKNOWN EVENT: {}".format(event))


    # main
    n = UPnP_Network(verbose_ssdp=False, verbose_xml=False)
    n.events_callback_add(_on_events)

    elm.run()
    n.shutdown()
