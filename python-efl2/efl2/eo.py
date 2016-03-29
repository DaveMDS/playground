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

###  module init/shutdown  ####################################################
print("EO INIT")
import atexit
lib.eo_init()
atexit.register(lambda: lib.eo_shutdown())


###  enums  ###################################################################


###  utils for internal usage utils  ##########################################
_class_mapping = {} # { 'Eo.Base': <class 'efl2.eo.Base'>, ... }
# _event_mapping = {} # { 'del':, lib._EO_BASE_EVENT_DEL, ... }

def _class_register(class_name):
    """ This decorator must be used on each Eo derived class """
    def decorator(pyclass):
        print('Registering eo class: "{}" as: {}'.format(class_name, pyclass))
        _class_mapping[class_name] = pyclass
        
        try:
            print(pyclass._events)
            print("------------------------------------------------------------")
        except:
            pass
            
        return pyclass
    return decorator


###  Eo.Base  #################################################################
# Eina_Bool (*Eo_Event_Cb)(void *data, const Eo_Event *event);
@ffi.def_extern()
def _eo_base_event_cb(data, event):
    print("@@@@@ "*40)
    # self = ffi.from_handle(x)
    # if callable(self._priv['cb']):
        # return self._priv['cb'](*self._priv['cb_args'], **self._priv['cb_kargs'])

    return lib.EO_CALLBACK_CONTINUE

@ffi.def_extern()
def _eo_base_del_cb(data, event):
    print("DEL "*40)

    return lib.EO_CALLBACK_CONTINUE

# ufffaaaaa
@ffi.callback("Eina_Bool (*Eo_Event_Cb)(void *data, const Eo_Event *event)")
def my_global_callback(data, event):
    # return ffi.from_handle(handle).some
    print("DEL "*40)
    return lib.EO_CALLBACK_CONTINUE

EO_BASE_EVENT_DEL = lib._EO_BASE_EVENT_DEL
EO_BASE_EVENT_CALLBACK_ADD = lib._EO_BASE_EVENT_CALLBACK_ADD
EO_BASE_EVENT_CALLBACK_DEL = lib._EO_BASE_EVENT_CALLBACK_DEL

@_class_register('Eo.Base')
class Base(object):
    """

    Base class used by all the object in the EFL.

    """
    # _events = {
        # 'del': ffi.addressof(lib._EO_BASE_EVENT_DEL),
        # 'callback,add': ffi.addressof(lib._EO_BASE_EVENT_CALLBACK_ADD),
        # 'callback,del': ffi.addressof(lib._EO_BASE_EVENT_CALLBACK_DEL),
    # }
    def __init__(self, klass, parent, finalize=True):
        print("Eo Base __init__ for klass:", klass)
        self._priv = dict()  # for bindings internal usage

        self._obj = lib._eo_add_internal_start(ffi.NULL, 0, klass,
                                            parent._obj if parent else ffi.NULL,
                                            False, # add ref ?
                                            False  # is fallback ?
                                            )
        if self._obj == ffi.NULL:
            raise MemoryError("Could not create the object")

        if finalize is True:
            self._finalize()

    def _finalize(self):
        print("fin")
        
        lib._eo_add_end(self._obj, False)  # is fallback ?

        # daiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii !!!!!!!!!!!!!!!111
        print("---" + ffi.string(ffi.addressof(lib._EO_BASE_EVENT_CALLBACK_ADD).name))
        lib.eo_event_callback_add(self._obj,

                                    ffi.addressof(lib._EO_BASE_EVENT_DEL),
                                    # lib._EO_BASE_EVENT_DEL,

                                    # lib._eo_base_del_cb, ffi.NULL)
                                    my_global_callback, ffi.NULL)

    def _set_properties_from_keyword_args(self, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                setattr(self, k, v)

    def __nonzero__(self):
        return 1 if (self._obj != None) and (self._obj != ffi.NULL) else 0

    def delete(self):
        print("DEL", self)
        lib.eo_del(self._obj)
        # lib.eo_unref(self._obj)
        self._obj = None
        # TODO disconnect on_del

    @property
    def data(self):
        """ For user convenience (dict lazy created only when used) """
        if not hasattr(self, '_data'):
            self._data = dict()
        return self._data

    def event_callback_priority_add(self, priority, callback, *args, **kargs):
        userdata = ffi.new_handle(self)
        self._priv['self_h'] = userdata   # must keep this alive!   :/
        
        return bool(lib.eo_event_callback_priority_add(self._obj,
                #const Eo_Event_Description *desc,
                ffi.addressof(lib._EO_BASE_EVENT_DEL),
                priority,
                lib._eo_base_event_cb,
                userdata))

    def event_callback_add4(self, name, func, *args, **kargs):

        print("Connecting4: " + name)

        ret = lib.eo_event_callback_priority_byname_add(self._obj,
                                  "SUKA!!!!", lib.EO_CALLBACK_PRIORITY_DEFAULT,
                                  lib._eo_base_event_cb, ffi.NULL)
        print("Connetcing3: " + str(ret))

    def event_callback_add3(self, ev, *args, **kargs):
        # ev = self.__events.get(ev_name)

        print("Connecting3: " + str(ev))
        print("Connecting3: " + ffi.string(ev.name))
        # ev_ptr = ffi.new("struct _Eo_Event_Description *")
        # ev_ptr = ffi.addressof(ev)
        # ev_ptr = 
        # self._priv['daiiiiii'] = ev_ptr

        ret = lib.eo_event_callback_add(self._obj,
                                  # ev_ptr,
                                  ev,
                                  lib._eo_base_event_cb, ffi.NULL)
        print("Connetcing3: " + str(ret))

    def event_callback_add2(self, ev_name, *args, **kargs):
        # ev = self.__events.get(ev_name)
        ev = self._events.get(ev_name)
        if not ev:
            print("ERRRRRRRRRRRRRRRRROOOOOR")
            return

        print("Connecting2: " + ev_name)
        lib.eo_event_callback_add(self._obj,
                                  # ffi.addressof(ev),
                                  ev,
                                  lib._eo_base_event_cb, ffi.NULL)
        
    def event_callback_add(self, *args, **kargs):
        self.event_callback_priority_add(0, *args, **kargs)

        lib.eo_event_callback_add(self._obj,
                                 ffi.addressof(lib._EO_BASE_EVENT_DEL),
                                 lib._eo_del_cb, ffi.NULL)
