#!/usr/bin/env python
# encoding: utf-8


# https://en.wikipedia.org/wiki/Universal_Plug_and_Play
# https://git.enlightenment.org/legacy/subversion-history.git/tree/trunk/PROTO/eupnp
# http://www.upnp-hacks.org


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
# http://brisa.garage.maemo.org/doc/html/upnp/


from efl.evas import EXPAND_BOTH, FILL_BOTH, EXPAND_HORIZ, FILL_HORIZ
from efl import elementary as elm
from efl.elementary import StandardWindow, Box, Frame, Entry, Button, Icon, \
    Progressbar, Genlist, GenlistItemClass, ELM_GENLIST_ITEM_TREE, \
    utf8_to_markup

from eupnp import *


class DeviceItemClass(GenlistItemClass):
    def __init__(self):
        GenlistItemClass.__init__(self, item_style="default")

    def text_get(self, obj, part, device):
        return '{} ({})'.format(device.name, device.type)

    def content_get(self, obj, part, device):
        if part == 'elm.swallow.icon':
            icon_url = device.bigger_icon_url
            if icon_url is not None:
                return Icon(obj, file=icon_url)
            else:
                return Icon(obj, standard='user-home')


class ServiceItemClass(GenlistItemClass):
    def __init__(self):
        GenlistItemClass.__init__(self, item_style="no_icon")

    def text_get(self, obj, part, service):
        return service.type

device_itc = DeviceItemClass()
service_itc = ServiceItemClass()





class TestWin(StandardWindow):

    def __init__(self):
        StandardWindow.__init__(self, "upnp_test", "UPnP Inspector",
                                size=(400, 500), autodel=True)

        # main vertical box
        box = Box(self, size_hint_weight=EXPAND_BOTH)
        self.resize_object_add(box)
        box.show()

        # buttons
        vbox = Box(self, horizontal=True)
        box.pack_end(vbox)
        vbox.show()

        # bt = Button(self, text="Discover")
        # vbox.pack_end(bt)
        # bt.show()

        # animated wheel to see blocking issues
        pb = Progressbar(self, style='wheel', pulse_mode=True)
        vbox.pack_end(pb)
        pb.pulse(True)
        pb.show()

        # Genlist
        gl = Genlist(self, homogeneous=True, #mode=ELM_LIST_COMPRESS,
                     size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        gl.callback_selected_add(self.list_item_selected_cb)
        gl.callback_expand_request_add(lambda g, i: setattr(i, 'expanded', True))
        gl.callback_contract_request_add(lambda g, i: setattr(i, 'expanded', False))
        gl.callback_expanded_add(self.list_item_expanded_cb)
        gl.callback_contracted_add(lambda g, i: i.subitems_clear())
        box.pack_end(gl)
        gl.show()
        self.gl = gl

        # detailed info frame + entry
        fr = Frame(self, text='Detailed info:', size_hint_expand=EXPAND_HORIZ,
                   size_hint_fill=FILL_HORIZ)
        box.pack_end(fr)
        fr.show()

        en = Entry(fr, #scrollable=True,
                   text='Select an item to show detailed info.',
                   size_hint_expand=EXPAND_HORIZ, size_hint_fill=FILL_HORIZ)
        fr.content = en
        en.show()
        self.info_entry = en
        
        # show the window
        self.show()

    def list_item_expanded_cb(self, gl, gli):
        obj = gli.data
        if isinstance(obj, UPnP_Device):
            device = obj
            for usn, service in device.services.items():
                gl.item_append(service_itc, service, gli,
                               flags=ELM_GENLIST_ITEM_TREE)

        elif isinstance(obj, UPnP_Service):
            service = obj
            print("TODO !!!!!")

    def list_item_selected_cb(self, gl, gli):
        obj = gli.data
        if isinstance(obj, UPnP_Device):
            device = obj
            self.info_entry.text = utf8_to_markup(str(device))
        elif isinstance(obj, UPnP_Service):
            service = obj
            self.info_entry.text = utf8_to_markup(str(service))
        

    def device_add(self, device):
        self.gl.item_append(device_itc, device, flags=ELM_GENLIST_ITEM_TREE)

    def device_del(self, device):
        for item in self.gl:
            if item.data == device:
                item.delete()
                return
        

    # def service_add(self, service):
        # print("SERVICE ADD " + str(service))
        # item = self.gl.item_append(device_itc, device)


def _on_upnp_events(net, event, obj, win):

        if event is UPNP_EVENT_DEVICE_FOUND:
            print("--- UPNP_DEVICE_FOUND:" + str(obj))
            win.device_add(obj)

        elif event is UPNP_EVENT_DEVICE_GONE:
            print("--- UPNP_DEVICE_GONE:" + str(obj))
            win.device_del(obj)

        elif event is UPNP_EVENT_SERVICE_FOUND:
            print("--- UPNP_SERVICE_FOUND:" + str(obj))
            # win.service_add(obj)
        
        elif event is UPNP_EVENT_SERVICE_GONE:
            print("--- UPNP_SERVICE_GONE:" + str(obj))



if __name__ == "__main__":
    elm.policy_set(elm.ELM_POLICY_QUIT, elm.ELM_POLICY_QUIT_LAST_WINDOW_CLOSED)

    win = TestWin()


    
    n = UPnP_Network()
    n.events_callback_add(_on_upnp_events, win)

    
    elm.run()

    n.shutdown()


