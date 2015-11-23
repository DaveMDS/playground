#!/usr/bin/env python
# encoding: utf-8

import os
import struct
import socket

# import urllib2
from xml.etree import ElementTree
# import xml.dom.minidom


from efl import ecore, ecore_con
from efl import elementary as elm



#-------------
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
#-------------


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
    def __init__(self, parent_host, service_id, service_type, xml_url, control_url, event_url):
        self.parent_host = parent_host
        self.service_id = service_id
        self.service_type = service_type
        self.xml_url = xml_url
        self.control_url = control_url
        self.event_url = event_url

        self.request_xml()

    def __str__(self):
        return "<UPnP_Service '{}' at '{}'>".format(
                self.service_id, self.parent_host.friendly_name)

    # XML stuff...
    def request_xml(self):
        print("REQUEST SERVICE XML " + self.xml_url)
        u = UrlSimple(self.xml_url, self._xml_complete)
        u.additional_header_add('USER-AGENT', 'UPnP/2.0')
        u.additional_header_add('CONTENT-TYPE','text/xml; charset="utf-8"')
        u.get()

    def _xml_complete(self, url, status, data):
        print("SERVICE DONE " + str(status) + str(url if status != 200 else ''))
        # print(data)
        # print("========================================")
        # pass


class UPnP_Host(object):
    def __init__(self, uuid, xml_url):
        print("VALID!!! " + uuid)
        self.uuid = uuid
        self._xml_url = xml_url
        self._base_url = ''

        self.device_info = {} # raw info from xml
        self.services = {}    # key:serviceId val:UPnP_Service() instance

        self.request_xml()

    def __str__(self):
        return "<UPnP_Host '{}' of type '{}'>".format(
                self.friendly_name, self.device_type)

    @property
    def UDN(self):
        return self.device_info.get('UDN')

    @property
    def device_type(self):
        return self.device_info.get('deviceType')

    @property
    def friendly_name(self):
        return self.device_info.get('friendlyName')

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

    # XML stuff...
    def request_xml(self):
        print("REQUEST DEVICE XML " + self._xml_url)
        u = UrlSimple(self._xml_url, self._xml_complete)
        u.additional_header_add('USER-AGENT', 'UPnP/2.0')
        u.additional_header_add('CONTENT-TYPE','text/xml; charset="utf-8"')
        u.get()

    def _xml_complete(self, url, status, data):

        if status != 200:
            return

        from pprint import pprint
            
        print("@@@@@@@@@@@")
        # print(url)
        # print(status)
        # print(data)
        # print("---")

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
        lis = device_info['serviceList']['service']
        if not isinstance(lis, list):
            lis = [lis]

        for service in lis:
            service_id = service['serviceId']
            if not service_id in self.services:
                s = UPnP_Service(self, service_id,
                                 service['serviceType'],
                                 self._fix_base_url(service['SCPDURL']),
                                 self._fix_base_url(service['controlURL']),
                                 self._fix_base_url(service['eventSubURL']))
                self.services[service_id] = s
        del device_info['serviceList']

        # TODO handle icons
        

        self.device_info = device_info


        # debug...
        print("--- COMPLETED HOST:")
        print(self)
        # pprint(self.device_info)
        for service in self.services:
            print(self.services[service])


        print("---")

    def _fix_base_url(self, url):
        if url.startswith(self._base_url):
            return url
        if not self._base_url.endswith('/') and not url.startswith('/'):
            return self._base_url + '/' + url
        return self._base_url + url

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
