#!/usr/bin/env python
# encoding: utf-8


# https://en.wikipedia.org/wiki/Universal_Plug_and_Play
# https://git.enlightenment.org/legacy/subversion-history.git/tree/trunk/PROTO/eupnp


from efl.evas import EXPAND_BOTH, FILL_BOTH

from efl import elementary as elm
from efl.elementary import StandardWindow, Box, Label, Button, Icon, \
    Progressbar, Genlist, GenlistItemClass, ELM_LIST_COMPRESS





class MyItemClass(GenlistItemClass):
    def __init__(self):
        GenlistItemClass.__init__(self, item_style="default")

    def text_get(self, obj, part, item_data):
        return "Item # %i (itc2)" % item_data

    def content_get(self, obj, part, item_data):
        if part == 'elm.swallow.icon':
            return  Icon(obj, standard='user-trash')
        elif part == 'elm.swallow.end':
            return  Icon(obj, standard='user-home')

itc = MyItemClass()





class TestWin(StandardWindow):

    def __init__(self):
        StandardWindow.__init__(self, "upnp_test", "UPnp Test",
                                size=(480, 600), autodel=True)

        # main vertical box
        box = Box(self, size_hint_weight=EXPAND_BOTH)
        self.resize_object_add(box)
        box.show()

        # buttons
        vbox = Box(self, horizontal=True)
        box.pack_end(vbox)
        vbox.show()

        bt = Button(self, text="Discover")
        vbox.pack_end(bt)
        bt.show()

        # animated wheel to see blocking issues
        pb = Progressbar(self, style='wheel', pulse_mode=True)
        vbox.pack_end(pb)
        pb.pulse(True)
        pb.show()
        

        # Genlist
        gl = Genlist(self, homogeneous=True, mode=ELM_LIST_COMPRESS,
                     size_hint_weight=EXPAND_BOTH, size_hint_align=FILL_BOTH)
        gl.callback_selected_add(self.list_selected_cb)
        box.pack_end(gl)
        gl.show()

        # populate the genlist
        # for i in range(0, 10):
            # item = gl.item_append(itc, i)


        # show the window
        self.show()


    def list_selected_cb(self, gl, gli):
        print("\n---Genlist selected---")
        print(gl)
        print(gli)


if __name__ == "__main__":
    elm.policy_set(elm.ELM_POLICY_QUIT, elm.ELM_POLICY_QUIT_LAST_WINDOW_CLOSED)

    TestWin()

    ##########
    # from upnp import UPnP
    # u = UPnP()
    # u.msearch()

    ###########
    from eupnp import UPnP_Network
    n = UPnP_Network()
    n.msearch()


    
    elm.run()
