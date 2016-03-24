# Copyright (C) 2007-2016 various contributors (see AUTHORS)
#
# This file is part of Python-EFL.
#
# Python-EFL is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# Python-EFL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this Python-EFL.  If not, see <http://www.gnu.org/licenses/>.

from ._elementary_ffi import ffi, lib
from ._utils import _to_bytes, _to_unicode
from . import eo
from . import evas


###  module init/shutdown  ####################################################
print("ELM INIT")
import atexit
lib.elm_init(0, ffi.NULL)
atexit.register(lambda: lib.elm_shutdown())


###  enums  ###################################################################
ELM_WIN_BASIC = lib.ELM_WIN_BASIC
# TODO COMPLETE...


###  module level functions  ##################################################
def run():
    lib.elm_run()

def exit():
    lib.elm_exit()


###  Elm.Widget  ##############################################################
class Widget(evas.Object_Smart):
    pass


###  Elm.Container  ###########################################################
class Container(Widget):
    pass


###  Elm.Box  ##############################################################
class Box(Widget):
    def __init__(self, parent, *args, **kargs):
        eo.Eo.__init__(self, lib.elm_box_class_get(), parent._obj)

    def pack_end(self, subobj):
        lib.elm_obj_box_pack_end(self._obj, subobj._obj);

    def pack_start(self, subobj):
        lib.elm_obj_box_pack_start(self._obj, subobj._obj);

###  Elm.Layout  ##############################################################
class Layout(Container):
    def __init__(self, parent, *args, **kargs):
        eo.Eo.__init__(self, lib.elm_layout_class_get(), parent._obj)

    @property
    def text(self):
        # TODO FIX part
        return _to_unicode(ffi, lib.elm_obj_layout_text_get(self._obj, ffi.NULL))

    @text.setter
    def text(self, text):
        # TODO FIX part
        lib.elm_obj_layout_text_set(self._obj, ffi.NULL, _to_bytes(text))



###  Elm.Win  #################################################################
class Win(Widget):
    def __init__(self, name, type, *args, **kargs):

        name = _to_bytes(name)

        # custom constructor
        eo.Eo.__init__(self, lib.elm_win_class_get(), ffi.NULL, False)
        lib.elm_obj_win_type_set(self._obj, type)
        lib.elm_obj_win_name_set(self._obj, name) # encode/decode ???
        eo.Eo._finalize(self)

        print("Win INIT")

    @property
    def title(self):
        return _to_unicode(ffi, lib.elm_obj_win_title_get(self._obj))

    @title.setter
    def title(self, title):
        lib.elm_obj_win_title_set(self._obj, _to_bytes(title))

    def resize_object_add(self, subobj):
        lib.elm_obj_win_resize_object_add(self._obj, subobj._obj)


###  Elm.Win_Standard  ########################################################
class Win_Standard(Win):
    def __init__(self, name, *args, **kargs):

        # custom constructor
        # super(Eo, self).__init__(lib.elm_win_standard_class_get(), ffi.NULL, False)
        eo.Eo.__init__(self, lib.elm_win_standard_class_get(), ffi.NULL, False)
        lib.elm_obj_win_name_set(self._obj, name) # encode/decode ???
        eo.Eo._finalize(self)
        
        print("Standard INIT")


###  Elm.Label  ###############################################################
class Label(Layout):
    def __init__(self, parent, *args, **kargs):
        eo.Eo.__init__(self, lib.elm_label_class_get(), parent._obj)


###  Elm.Button  ##############################################################
class Button(Layout, evas.Clickable_Interface):
    def __init__(self, parent, *args, **kargs):
        eo.Eo.__init__(self, lib.elm_button_class_get(), parent._obj)

