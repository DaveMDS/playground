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

from ._evas_ffi import ffi, lib
from ._utils import _to_bytes, _to_unicode
from . import eo
from . import efl


###  module init/shutdown  ####################################################
print("EVAS INIT")
import atexit
lib.evas_init()
atexit.register(lambda: lib.evas_shutdown())


###  enums  ###################################################################
# ELM_WIN_BASIC = lib.ELM_WIN_BASIC


###  module level functions  ##################################################



###  Evas.Object  #############################################################
class Object(eo.Eo, efl.Gfx_Base):
    def __init__(self, parent):

        # standard constructor
        eo.Eo.__init__(self, lib.evas_object_class_get(), parent._obj)
        print("Evas.Object INIT")


###  Evas.Object_Smart  #######################################################
class Object_Smart(Object):
    def __init__(self, *args, **kargs):
        # standard constructor
        eo.Eo.__init__(self, lib.evas_object_smart_class_get(), parent._obj)
        print("Evas.Object_Smart INIT")


###  Evas.Signal_Interface  ################################################
class Signal_Interface(object):
    pass

###  Evas.Clickable_Interface  ################################################
class Clickable_Interface(Signal_Interface):
    """
    events {
      clicked
      clicked,double
      clicked,triple
      clicked,right
      pressed
      unpressed
      longpressed
      repeated
    }
    """
    pass
