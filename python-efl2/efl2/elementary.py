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

from ._eo_ffi import lib as eo_lib # TODO: can remove this ???
from .eo import Eo

import atexit

print("ELM INIT")
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


###  classes  #################################################################

class Win(Eo):
    def __init__(self, name, type, *args, **kargs):

        super(Win, self).__init__()
        print("Win INIT")

        self._obj = eo_lib._eo_add_internal_start(__file__, 0,
                                                  lib.elm_win_class_get(),
                                                  ffi.NULL, # parent
                                                  False); # add ref ?
        if self._obj == ffi.NULL:
            raise MemoryError("Could not create the object")

        # lib.ecore_obj_timer_constructor(self._obj, in_, lib._timer_cb, userdata)
        lib.elm_obj_win_type_set(self._obj, lib.ELM_WIN_BASIC) # FIXME type
        lib.elm_obj_win_name_set(self._obj, name) # encode/decode ???
        eo_lib._eo_add_end(self._obj)

    # TODO REMOVE
    def show(self):
        lib.evas_object_show(self._obj)
        lib.evas_object_resize(self._obj, 300, 300)
