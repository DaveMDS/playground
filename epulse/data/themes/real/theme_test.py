#!/usr/bin/env python
# encoding: utf-8

import os

from efl.evas import EVAS_HINT_EXPAND, EVAS_HINT_FILL, EXPAND_BOTH, FILL_BOTH, FILL_VERT
from efl import elementary
from efl.elementary.window import StandardWindow
from efl.elementary.scroller import Scroller
from efl.elementary.background import Background
from efl.elementary.box import Box
from efl.elementary.frame import Frame
from efl.elementary.icon import Icon
from efl.elementary.label import Label
from efl.elementary.separator import Separator
from efl.elementary.slider import Slider
from efl.elementary.theme import theme_extension_add

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
THEME_FILE = os.path.join(SCRIPT_PATH, 'real.edj')


class MixerWin(StandardWindow):
    def __init__(self):
        StandardWindow.__init__(self, "E Pulse Mixer", "epulsemixer", 
                                autodel=True, size=(600, 300))
        self.callback_delete_request_add(lambda o: elementary.exit())

        bg = Background(self, style='pulse', size_hint_weight=EXPAND_BOTH)
        self.resize_object_add(bg)
        bg.show()
        
        box = Box(self, horizontal=True, size_hint_weight=EXPAND_BOTH)
        box.padding = (25, 0) # TODO REMOVEME
        self.resize_object_add(box)

        theme_extension_add(THEME_FILE)
        
        # frame 0
        fr = Frame(box, style='pulse', text="PLAYBACK",
                   size_hint_align=FILL_BOTH)
        box.pack_end(fr)
        fr.show()
        
        sbox = Box(fr, horizontal=True, size_hint_weight=EXPAND_BOTH)
        fr.content = sbox

        for label in ("System Sound", "Quod Libet"):
            sl = Slider(sbox, style='pulse', text=label,
                        horizontal=False, inverted=True,
                        size_hint_weight=EXPAND_BOTH, size_hint_fill=FILL_VERT)
            sbox.pack_end(sl)
            sl.show()
        
        # frame 1
        fr = Frame(box, style='pulse', text="INPUTS",
                   size_hint_align=FILL_BOTH)
        box.pack_end(fr)
        fr.show()
        
        sbox = Box(fr, horizontal=True, size_hint_weight=EXPAND_BOTH)
        fr.content = sbox
        
        # for label in ("Stereo analogico", "Digital Stereo (HDMI)"):
        for label in ("Audio interno Stereo digitale", ):
            sl = Slider(sbox, style='pulse', text=label,
                        horizontal=False, inverted=True,
                        size_hint_weight=EXPAND_BOTH, size_hint_fill=FILL_VERT)
            sbox.pack_end(sl)
            sl.show()
        
        # frame 2
        fr = Frame(box, style='pulse', text="OUTPUTS",
                   size_hint_align=FILL_BOTH)
        box.pack_end(fr)
        fr.show()
        
        sbox = Box(fr, horizontal=True, size_hint_weight=EXPAND_BOTH)
        fr.content = sbox
        
        sep = None
        # for label in ("Stereo analogico", "Digital Stereo (HDMI)"):
        # for label in ("Stereo", "(HDMI) asdasdasd asd asd asd asd a asd"):
        for label in ("Stereo", "(HDMI)"):
            sl1 = Slider(sbox, style='pulse_double_left', text=label,
                        horizontal=False, inverted=True, 
                        size_hint_weight=EXPAND_BOTH, size_hint_fill=FILL_VERT)
            sbox.pack_end(sl1)
            sl1.show()

            sl2 = Slider(sbox, style='pulse_double_right', text='',
                        horizontal=False, inverted=True, 
                        size_hint_weight=EXPAND_BOTH, size_hint_fill=FILL_VERT)
            sbox.pack_end(sl2)
            sl2.show()
            
            sl1.callback_changed_add(lambda sl: setattr(sl2, 'value', sl.value))
            
            if sep is None:
                sep = Separator(sbox)
                sbox.pack_end(sep)
                sep.show()
            



        box.show()
        self.show()
    
if __name__ == "__main__":

    win = MixerWin()
    elementary.run()
