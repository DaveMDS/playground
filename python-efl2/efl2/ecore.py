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

from ._ecore_ffi import ffi, lib

from .eo import Eo

import atexit

print("ECORE INIT")
lib.ecore_init()
atexit.register(lambda: lib.ecore_shutdown())


# enums
ECORE_CALLBACK_CANCEL = lib.ECORE_CALLBACK_CANCEL
ECORE_CALLBACK_RENEW = lib.ECORE_CALLBACK_RENEW
ECORE_CALLBACK_PASS_ON = lib.ECORE_CALLBACK_PASS_ON
ECORE_CALLBACK_DONE = lib.ECORE_CALLBACK_DONE

def main_loop_begin():
    lib.ecore_main_loop_begin()

def main_loop_quit():
    lib.ecore_main_loop_quit()


@ffi.def_extern()
def _timer_cb(x):

    self = ffi.from_handle(x)
    if callable(self._priv['cb']):
        return self._priv['cb'](*self._priv['cb_args'], **self._priv['cb_kargs'])

    return 0


class Timer(Eo):
    def __init__(self, in_, callback, *args, **kargs):

        userdata = ffi.new_handle(self)

        # custom constructor
        super(Timer, self).__init__(lib.ecore_timer_class_get(), ffi.NULL, False)
        lib.ecore_obj_timer_constructor(self._obj, in_, lib._timer_cb, userdata)
        super(Timer, self)._finalize()

        print("Timer INIT", in_)

        self._priv['self_h'] = userdata   # must keep this alive!   :/
        self._priv['cb'] = callback
        self._priv['cb_args'] = args
        self._priv['cb_kargs'] = kargs
