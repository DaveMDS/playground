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

from ._eo_ffi import ffi, lib

import atexit

print("EO INIT")
lib.eo_init()
atexit.register(lambda: lib.eo_shutdown())

# 
# def main_loop_begin():
    # lib.ecore_main_loop_begin()
# 
# def main_loop_quit():
    # lib.ecore_main_loop_quit()



class Eo(object):
    def __init__(self, klass, parent, finalize=True):
        print("Eo obstract for klass:", klass)
        # self._obj = None
        self._priv = dict()

        self._obj = lib._eo_add_internal_start(__file__, 0, klass, parent, False) # add ref ?
        if self._obj == ffi.NULL:
            raise MemoryError("Could not create the object")

        if finalize:
            lib._eo_add_end(self._obj)

    def _finalize(self):
        lib._eo_add_end(self._obj)


    """
    cdef int _set_properties_from_keyword_args(self, dict kwargs) except 0:
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
        return 1
    """

    # def event_callback_add(
        # Eina_Bool eo_event_callback_add(Eo *obj, const Eo_Event_Description *desc, Eo_Event_Cb cb, const void *data);

