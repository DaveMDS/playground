###############################################################################
###                      THIS FILE IS MANUALLY WRITTEN                      ###
###############################################################################

from __future__ import absolute_import, print_function, division

from cffi import FFI
import os

ffi = FFI()


with open(os.path.join(os.path.dirname(__file__), 'eolian.h')) as f:
    ffi.cdef(f.read())

lib = ffi.dlopen('eolian')

# arg = ffi.new("char[]", "world")         # equivalent to C code: char arg[] = "world";
# lib.printf("hi there, %s.\n", arg)         # call printf


###  utils (TO BE SHARED)  ####################################################
import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY3:
    text_type = str
    binary_type = bytes
else:
    text_type = unicode
    binary_type = str
    
def _pystr_to_bytes(s):
    if isinstance(s, binary_type):
        return s
    return text_type(s).encode('utf-8')


def _cstr_to_unicode(ffi, s):
    if s == ffi.NULL:
        return None
    s = ffi.string(s)
    if isinstance(s, text_type):
        return s
    return binary_type(s).decode('utf-8')

def _cstr_to_unicode2(s):
    if s == ffi.NULL:
        return None
    s = ffi.string(ffi.cast('char *', s))
    if isinstance(s, text_type):
        return s
    return binary_type(s).decode('utf-8')

"""
cdef class EoIterator:

    def __iter__(self):
        return self

    def __next__(self):
        cdef:
            void* tmp
            Eina_Bool result

        if not eina_iterator_next(self.itr, &tmp):
            raise StopIteration

        return object_from_instance(<cEo *>tmp)

    def __dealloc__(self):
        eina_iterator_free(self.itr)
"""

class Iterator:
    def __init__(self, conv_func, iter_obj):
        self.next = self.__next__ # py2 compat
        self._conv = conv_func
        self._iter = iter_obj
        self._tmp = ffi.new('void*[1]')

    def __iter__(self):
        return self

    def __next__(self):
        if not lib.eina_iterator_next(self._iter, self._tmp):
            lib.eina_iterator_free(self._iter)
            raise StopIteration

        return self._conv(self._tmp[0])
        
    def free(self):
        lib.eina_iterator_free(self._iter)


def _c_eolian_function_to_py(f):
    return Function(f)

def _c_eolian_parameter_to_py(p):
    return Parameter(p)

def _c_eolian_typedecl_to_py(t):
    return Typedecl(t)

def _c_eolian_enum_field_to_py(f):
    return Enum_Type_Field(f)

def _c_eolian_declaration_to_py(f):
    return Declaration(f)

###  module init/shutdown  ####################################################
print("EOLIAN INIT")
import atexit
lib.eolian_init()
atexit.register(lambda: lib.eolian_shutdown())


###  module level functions ###################################################
def file_parse(fname):
    return bool(lib.eolian_file_parse(_pystr_to_bytes(fname)))
   
def all_eot_files_parse():
    return bool(lib.eolian_all_eot_files_parse())
   
def system_directory_scan():
    return bool(lib.eolian_system_directory_scan())

def database_validate(silent_types=False):
    return bool(lib.eolian_database_validate(silent_types))

def typedecl_enums_get_by_file(fname):
    return Iterator(_c_eolian_typedecl_to_py, lib.eolian_typedecl_enums_get_by_file(fname))

def declarations_get_by_file(fname):
    return Iterator(_c_eolian_declaration_to_py, lib.eolian_declarations_get_by_file(fname))
# Eina_Iterator            *eolian_declarations_get_by_file(const char *fname);

###  eolian.Class  ############################################################

class Class(object):
    def __init__(self, eo_file):
        eo_file = _pystr_to_bytes(eo_file)
        self._obj = lib.eolian_class_get_by_file(eo_file) # const Eolian_Class *klass

    def __repr__(self):
        return "<eolian.Class '{0.full_name}', prefix '{0.eo_prefix}'>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_class_name_get(self._obj))

    @property
    def full_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_class_full_name_get(self._obj))

    @property
    def legacy_prefix(self):
        return _cstr_to_unicode(ffi, lib.eolian_class_legacy_prefix_get(self._obj))

    @property
    def eo_prefix(self):
        return _cstr_to_unicode(ffi, lib.eolian_class_eo_prefix_get(self._obj))

    @property
    def data_type(self):
        return _cstr_to_unicode(ffi, lib.eolian_class_data_type_get(self._obj))

    @property
    def inherits(self):
        return Iterator(_cstr_to_unicode2, lib.eolian_class_inherits_get(self._obj))

    @property
    def functions(self):
        return Iterator(_c_eolian_function_to_py, lib.eolian_class_functions_get(self._obj, lib.EOLIAN_METHOD))

    @property
    def properties(self):
        return Iterator(_c_eolian_function_to_py, lib.eolian_class_functions_get(self._obj, lib.EOLIAN_PROPERTY))


class Function(object):
    def __init__(self, c_func):
        self._obj = c_func

    def __repr__(self):
        return "<eolian.Function '{0.name}', api: '{0.full_c_name}'>".format(self)
    
    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_function_name_get(self._obj))

    @property
    def full_c_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_function_full_c_name_get(self._obj, lib.eolian_function_type_get(self._obj), 0))

    @property
    def is_constructor(self):
        return lib.eolian_function_is_constructor(self._obj, lib.eolian_function_class_get(self._obj))


    @property
    def parameters(self):
        return Iterator(_c_eolian_parameter_to_py, lib.eolian_function_parameters_get(self._obj))


    @property
    def return_type(self):
        t = lib.eolian_function_return_type_get(self._obj, lib.EOLIAN_METHOD)
        if t != ffi.NULL:
            return Type(t)

    @property
    def full_c_define(self):
        ret = self.return_type
        if ret:
            ret = ret.c_type #  TODO TEST TEST TEST TEST TEST TEST TEST 
        else:
            ret = 'void'

        pars = ['Eo *obj'] # TODO "obj" only in class methods
        for p in self.parameters:
            pars.append('{0.type.c_type} {0.name}'.format(p))
        pars = ', '.join(pars)
        return '{0} {1}({2})'.format(ret, self.full_c_name, pars)


class Parameter(object):
    def __init__(self, c_param):
        self._obj = c_param

    def __repr__(self):
        return "<eolian.Parameter '{0.name}', type: {0.type}, optional: {0.is_optional}, nonull: {0.is_nonull}>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_parameter_name_get(self._obj))

    @property
    def is_nonull(self):
        return bool(lib.eolian_parameter_is_nonull(self._obj))

    @property
    def is_nullable(self):
        return bool(lib.eolian_parameter_is_nullable(self._obj))

    @property
    def is_optional(self):
        return bool(lib.eolian_parameter_is_optional(self._obj))

    @property
    def type(self):
        return Type(lib.eolian_parameter_type_get(self._obj))


class Type(object):
    def __init__(self, c_type):
        self._obj = c_type

    def __repr__(self):
        return "<eolian.Type '{0.name}', api: '{0.c_type}'>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_type_name_get(self._obj))

    @property
    def full_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_type_full_name_get(self._obj))

    @property
    def c_type(self):
        return _cstr_to_unicode(ffi, lib.eolian_type_c_type_get(self._obj))


class Typedecl(object):
    def __init__(self, c_typedecl):
        self._obj = c_typedecl

    def __repr__(self):
        return "<eolian.Typedecl '{0.name}'>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_typedecl_name_get(self._obj))

    @property
    def full_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_typedecl_full_name_get(self._obj))

    @property
    def c_type(self):
        return _cstr_to_unicode(ffi, lib.eolian_typedecl_c_type_get(self._obj))

    @property
    def enum_fields(self):
        return Iterator(_c_eolian_enum_field_to_py, lib.eolian_typedecl_enum_fields_get(self._obj))
    # Eina_Iterator                  *eolian_typedecl_enum_fields_get(const Eolian_Typedecl *tp);


class Enum_Type_Field(object):
    def __init__(self, c_enum_field):
        self._obj = c_enum_field # const Eolian_Enum_Type_Field *

    def __repr__(self):
        return "<eolian.Enum_Type_Field '{0.name}', api: '{0.c_name}'>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_typedecl_enum_field_name_get(self._obj)) 

    @property
    def c_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_typedecl_enum_field_c_name_get(self._obj)) 


class Declaration(object):
    def __init__(self, c_decl):
        self._obj = c_decl # const Eolian_Declaration *

    def __repr__(self):
        return "<eolian.Declaration '{0.name}'>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_declaration_name_get(self._obj)) 


    @property
    def type(self):
        return Type(lib.eolian_declaration_type_get(self._obj))
