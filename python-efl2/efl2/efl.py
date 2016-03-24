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

from ._efl_ffi import ffi, lib
from ._utils import _to_bytes, _to_unicode
from . import eo


###  module init/shutdown  ####################################################
# print("EFL INIT")
# import atexit
# lib.efl_init()
# atexit.register(lambda: lib.efl_shutdown())


###  enums  ###################################################################
# ELM_WIN_BASIC = lib.ELM_WIN_BASIC


###  module level functions  ##################################################



###  Efl.Gfx.Base (Interface) #################################################
class Gfx_Base(object):
    @property
    def visible(self):
        return lib.efl_gfx_visible_get(self._obj)

    @visible.setter
    def visible(self, v):
        lib.efl_gfx_visible_set(self._obj, v)

