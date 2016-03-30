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
EO_CALLBACK_CONTINUE = lib.EO_CALLBACK_CONTINUE
EO_CALLBACK_STOP = lib.EO_CALLBACK_STOP

EO_CALLBACK_PRIORITY_BEFORE = lib.EO_CALLBACK_PRIORITY_BEFORE
EO_CALLBACK_PRIORITY_DEFAULT = lib.EO_CALLBACK_PRIORITY_DEFAULT
EO_CALLBACK_PRIORITY_AFTER = lib.EO_CALLBACK_PRIORITY_AFTER


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
@ffi.def_extern()  #  TODO @ffi.def_extern(onerror=my_handler)
def _eo_base_event_cb(c_data, c_event):

    func, args, kargs = ffi.from_handle(c_data)

    if callable(func):
        ret = func(*args, **kargs) # TODO pass obj (and event?)

    # TODO conversion functions for c_event??

    return ret

@ffi.def_extern()  #  TODO @ffi.def_extern(onerror=my_handler)
def _eo_base_del_cb(c_data, c_event):
    print("DEL "*20)

    lib.eo_event_callback_del(c_event.obj, lib.EO_BASE_EVENT_DEL,
                              lib._eo_base_del_cb, ffi.NULL)
                                  
    return lib.EO_CALLBACK_CONTINUE


EO_BASE_EVENT_DEL = lib.EO_BASE_EVENT_DEL
EO_BASE_EVENT_CALLBACK_ADD = lib.EO_BASE_EVENT_CALLBACK_ADD
EO_BASE_EVENT_CALLBACK_DEL = lib.EO_BASE_EVENT_CALLBACK_DEL

@_class_register('Eo.Base')
class Base(object):
    """

    Base class used by all the object in the EFL.

    """
    # _events = {
        # 'del': lib.EO_BASE_EVENT_DEL),
        # 'callback,add': lib.EO_BASE_EVENT_CALLBACK_ADD),
        # 'callback,del': lib.EO_BASE_EVENT_CALLBACK_DEL),
    # }
    def __init__(self, klass, parent, finalize=True, **kargs):
        # print("Eo Base __init__ for klass:", klass)
        self._priv = dict()  # for bindings internal usage

        self._obj = lib._eo_add_internal_start(ffi.NULL, 0, klass,
                                            parent._obj if parent else ffi.NULL,
                                            False, # add ref ?
                                            False  # is fallback ?
                                            )
        if self._obj == ffi.NULL:
            raise MemoryError("Could not create the object")

        if finalize is True:
            self.__init__end__(**kargs)

    def __init__end__(self, **kargs):
        
        lib._eo_add_end(self._obj, False)  # is fallback ?

        # set_properties_from_keyword_args
        if kargs:
            for k, v in kargs.items():
                setattr(self, k, v)


        lib.eo_event_callback_add(self._obj, lib.EO_BASE_EVENT_DEL,
                                  lib._eo_base_del_cb, ffi.NULL)

    def __nonzero__(self):
        return 1 if (self._obj != None) and (self._obj != ffi.NULL) else 0

    def delete(self):
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

    def event_callback_add(self, ev, func, *args, **kargs):
        c_data = ffi.new_handle((func, args, kargs))
        self.TEST = c_data # TODO FIXME !!!!!!!!!!!!!!!!!!!!!!!

        return bool(lib.eo_event_callback_add(self._obj, ev,
                                              lib._eo_base_event_cb, c_data))

    """
    def event_callback_priority_add(self, priority, callback, *args, **kargs):
        userdata = ffi.new_handle(self)
        self._priv['self_h'] = userdata   # must keep this alive!   :/
        
        return bool(lib.eo_event_callback_priority_add(self._obj, ev, priority,
                                            lib._eo_base_event_cb, userdata))
    
    """
