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
    def __init__(self):
        print("Eo obstract")
        self._obj = None
        self._priv = dict()

    def _add(self, klass, parent):
        self._obj = lib.eo_add(klass, parent)
        print("KLASS", klass)
        print("PAREN", parent)
        if self._obj == ffi.NULL:
            raise MemoryError("Could not create the object")

    """
    cdef int _set_properties_from_keyword_args(self, dict kwargs) except 0:
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)
        return 1
    """
