#! /usr/bin/env python3
# encoding: utf-8

from enum import Enum
from ctypes import CDLL, cast, byref, c_uint, c_char_p, c_void_p

from .eolian_lib import lib


###  enums  ###################################################################

class Eolian_Function_Type(Enum):
    UNRESOLVED = 0
    PROPERTY = 1
    PROP_SET = 2
    PROP_GET = 3
    METHOD = 4


###  type converters  #########################################################

def _bytes_to_str(s):
    return s.decode('utf-8') if s else None

def _str_to_bytes(s):
    return s.encode('utf-8')

def _c_str_to_py(s):
    return _bytes_to_str(cast(s, c_char_p).value)

def _c_eolian_class_to_py(cls):
    return Class(c_class=cls)


###  module init/shutdown  ####################################################

import atexit
lib.eolian_init()
atexit.register(lambda: lib.eolian_shutdown())


###  module level functions ###################################################

def directory_scan(dir_path):
    return bool(lib.eolian_directory_scan(dir_path))

def system_directory_scan():
    return bool(lib.eolian_system_directory_scan())

def all_eot_files_parse():
    return bool(lib.eolian_all_eot_files_parse())

def all_eo_files_parse():
    return bool(lib.eolian_all_eo_files_parse())

def file_parse(fname):
    return bool(lib.eolian_file_parse(_str_to_bytes(fname)))

def database_validate(silent_types=False):
    return bool(lib.eolian_database_validate(silent_types))

def all_classes_get():
    return Iterator(_c_eolian_class_to_py, lib.eolian_all_classes_get())


###  Classes  #################################################################

class Iterator:
    def __init__(self, conv_func, iter_obj):
        self.next = self.__next__ # py2 compat
        self._conv = conv_func
        self._iter = iter_obj
        self._tmp = c_void_p(0)

    def __iter__(self):
        return self

    def __next__(self):
        if not lib.eina_iterator_next(self._iter, byref(self._tmp)):
            lib.eina_iterator_free(self._iter)
            raise StopIteration

        return self._conv(self._tmp)

    def free(self):
        lib.eina_iterator_free(self._iter)


class Class(object):
    def __init__(self, eo_file=None, c_class=None, class_name=None):
        if eo_file:
            self._obj = lib.eolian_class_get_by_file(_str_to_bytes(eo_file))
        elif class_name:
            self._obj = lib.eolian_class_get_by_name(_str_to_bytes(class_name))
        elif c_class:
            self._obj = c_class  # const Eolian_Class *
        else:
            ERR('Invalid Class constructor')

    def __repr__(self):
        return "<eolian.Class '{0.full_name}', prefix '{0.eo_prefix}'>".format(self)

    @property
    def name(self):
        return _bytes_to_str(lib.eolian_class_name_get(self._obj))

    @property
    def full_name(self):
        return _bytes_to_str(lib.eolian_class_full_name_get(self._obj))

    @property
    def legacy_prefix(self):
        return _bytes_to_str(lib.eolian_class_legacy_prefix_get(self._obj))

    @property
    def eo_prefix(self):
        return _bytes_to_str(lib.eolian_class_eo_prefix_get(self._obj))

    @property
    def data_type(self):
        return lib.eolian_class_data_type_get(self._obj)

    @property
    def inherits(self):
        return Iterator(_c_str_to_py, lib.eolian_class_inherits_get(self._obj))

    @property
    def c_get_function_name(self):
        return lib.eolian_class_c_get_function_name_get(self._obj)

    @property
    def file(self):
        return lib.eolian_class_file_get(self._obj)

    @property
    def ctor_enable(self):
        return bool(lib.eolian_class_ctor_enable_get(self._obj))

