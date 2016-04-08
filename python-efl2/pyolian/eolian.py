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


def _c_eolian_event_to_py(f):
    return Event(f)

def _c_eolian_function_to_py(f):
    return Function(f)

def _c_eolian_constructor_to_py(f):
    return Constructor(f)

def _c_eolian_parameter_to_py(p):
    return Parameter(p)

def _c_eolian_typedecl_to_py(t):
    return Typedecl(t)

def _c_eolian_enum_field_to_py(f):
    return Enum_Type_Field(f)

def _c_eolian_declaration_to_py(f):
    return Declaration(f)

###  module init/shutdown  ####################################################
import atexit
lib.eolian_init()
atexit.register(lambda: lib.eolian_shutdown())


###  enums  ###################################################################

# Eolian_Function_Type:
EOLIAN_UNRESOLVED = lib.EOLIAN_UNRESOLVED
EOLIAN_PROPERTY = lib.EOLIAN_PROPERTY
EOLIAN_PROP_SET = lib.EOLIAN_PROP_SET
EOLIAN_PROP_GET = lib.EOLIAN_PROP_GET
EOLIAN_METHOD = lib.EOLIAN_METHOD

# Eolian_Class_Type:
EOLIAN_CLASS_UNKNOWN_TYPE = lib.EOLIAN_CLASS_UNKNOWN_TYPE
EOLIAN_CLASS_REGULAR = lib.EOLIAN_CLASS_REGULAR
EOLIAN_CLASS_ABSTRACT = lib.EOLIAN_CLASS_ABSTRACT
EOLIAN_CLASS_MIXIN = lib.EOLIAN_CLASS_MIXIN
EOLIAN_CLASS_INTERFACE = lib.EOLIAN_CLASS_INTERFACE

# Eolian_Declaration_Type:
EOLIAN_DECL_UNKNOWN = lib.EOLIAN_DECL_UNKNOWN
EOLIAN_DECL_CLASS = lib.EOLIAN_DECL_CLASS
EOLIAN_DECL_ALIAS = lib.EOLIAN_DECL_ALIAS
EOLIAN_DECL_STRUCT = lib.EOLIAN_DECL_STRUCT
EOLIAN_DECL_ENUM = lib.EOLIAN_DECL_ENUM
EOLIAN_DECL_VAR = lib.EOLIAN_DECL_VAR

# Eolian_Parameter_Dir:
EOLIAN_IN_PARAM = lib.EOLIAN_IN_PARAM
EOLIAN_OUT_PARAM = lib.EOLIAN_OUT_PARAM
EOLIAN_INOUT_PARAM = lib.EOLIAN_INOUT_PARAM

# Eolian_Type_Type:
EOLIAN_TYPE_UNKNOWN_TYPE = lib.EOLIAN_TYPE_UNKNOWN_TYPE
EOLIAN_TYPE_VOID = lib.EOLIAN_TYPE_VOID
EOLIAN_TYPE_REGULAR = lib.EOLIAN_TYPE_REGULAR
EOLIAN_TYPE_COMPLEX = lib.EOLIAN_TYPE_COMPLEX
EOLIAN_TYPE_POINTER = lib.EOLIAN_TYPE_POINTER
EOLIAN_TYPE_CLASS = lib.EOLIAN_TYPE_CLASS
EOLIAN_TYPE_UNDEFINED = lib.EOLIAN_TYPE_UNDEFINED

# Eolian_Typedecl_Type:
EOLIAN_TYPEDECL_UNKNOWN = lib.EOLIAN_TYPEDECL_UNKNOWN
EOLIAN_TYPEDECL_STRUCT = lib.EOLIAN_TYPEDECL_STRUCT
EOLIAN_TYPEDECL_STRUCT_OPAQUE = lib.EOLIAN_TYPEDECL_STRUCT_OPAQUE
EOLIAN_TYPEDECL_ENUM = lib.EOLIAN_TYPEDECL_ENUM
EOLIAN_TYPEDECL_ALIAS = lib.EOLIAN_TYPEDECL_ALIAS

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
    def __init__(self, eo_file=None, c_class=None):
        if eo_file:
            eo_file = _pystr_to_bytes(eo_file)
            self._obj = lib.eolian_class_get_by_file(eo_file) # const Eolian_Class *
        elif c_class:
            self._obj = c_class
        else:
            ERR('Invalid Class constructor')
            

    def __repr__(self):
        return "<eolian.Class '{0.full_name}', prefix '{0.eo_prefix}'>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_class_name_get(self._obj))

    @property
    def full_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_class_full_name_get(self._obj))

    @property
    def type(self):
        return lib.eolian_class_type_get(self._obj)
    # Eolian_Class_Type      eolian_class_type_get(const Eolian_Class *klass);
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
    def c_get_function_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_class_c_get_function_name_get(self._obj))

    @property
    def ctor_enable(self):
        return bool(lib.eolian_class_ctor_enable_get(self._obj))

    @property
    def constructors(self):
        return Iterator(_c_eolian_constructor_to_py, lib.eolian_class_constructors_get(self._obj))

    @property
    def events(self):
        return Iterator(_c_eolian_event_to_py, lib.eolian_class_events_get(self._obj))

    @property
    def methods(self):
        return Iterator(_c_eolian_function_to_py, lib.eolian_class_functions_get(self._obj, lib.EOLIAN_METHOD))

    @property
    def properties(self):
        return Iterator(_c_eolian_function_to_py, lib.eolian_class_functions_get(self._obj, lib.EOLIAN_PROPERTY))

    @property
    def getters(self):
        return Iterator(_c_eolian_function_to_py, lib.eolian_class_functions_get(self._obj, lib.EOLIAN_PROP_GET))

    @property
    def setters(self):
        return Iterator(_c_eolian_function_to_py, lib.eolian_class_functions_get(self._obj, lib.EOLIAN_PROP_SET))


class Constructor(object):
    def __init__(self, c_ctor):
        self._obj = c_ctor # const Eolian_Constructor *

    def __repr__(self):
        return "<eolian.Constructor '{0.full_name}', optional: {0.is_optional}>".format(self)

    @property
    def full_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_constructor_full_name_get(self._obj))

    @property
    def function(self):
        return Function(lib.eolian_constructor_function_get(self._obj))

    @property
    def is_optional(self):
        return bool(lib.eolian_constructor_is_optional(self._obj))


class Event(object):
    def __init__(self, c_event):
        self._obj = c_event # const Eolian_Event *

    def __repr__(self):
        return "<eolian.Event '{0.name}', api: '{0.c_name}'>".format(self)

    # @property
    # def type(self):
        # return lib.eolian_function_type_get(self._obj)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_event_name_get(self._obj))

    @property
    def c_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_event_c_name_get(self._obj))


class Function(object):
    def __init__(self, c_func):
        self._obj = c_func # const Eolian_Function *

    def __repr__(self):
        return "<eolian.Function '{0.name}'>".format(self)

    @property
    def type(self):
        return lib.eolian_function_type_get(self._obj)
        
    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_function_name_get(self._obj))

    def full_c_name_get(self, ftype, uselegacy=False):
        return _cstr_to_unicode(ffi, lib.eolian_function_full_c_name_get(self._obj, ftype, uselegacy))

    @property
    def is_constructor(self):
        return lib.eolian_function_is_constructor(self._obj, lib.eolian_function_class_get(self._obj))

    @property
    def is_c_only(self):
        return bool(lib.eolian_function_is_c_only(self._obj))

    def is_legacy_only_get(self, ftype):
        return bool(lib.eolian_function_is_legacy_only(self._obj, ftype))

    @property
    def parameters(self):
        return Iterator(_c_eolian_parameter_to_py, lib.eolian_function_parameters_get(self._obj))

    @property
    def getter_values(self):
        return Iterator(_c_eolian_parameter_to_py, lib.eolian_property_values_get(self._obj, lib.EOLIAN_PROP_GET))

    @property
    def setter_values(self):
        return Iterator(_c_eolian_parameter_to_py, lib.eolian_property_values_get(self._obj, lib.EOLIAN_PROP_SET))

    # @property
    # def return_type(self):
        # t = lib.eolian_function_return_type_get(self._obj, lib.EOLIAN_PROPERTY) ####### WRONG
        # if t != ffi.NULL:
            # return Type(t)

    def return_type_get(self, ftype):
        t = lib.eolian_function_return_type_get(self._obj, ftype)
        if t != ffi.NULL:
            return Type(t)

    def full_c_define_get(self, ftype):
        # TODO: move this code to generator.py
        rtype = self.return_type_get(ftype)
        ret = rtype.c_type if rtype is not None else 'void'

        pars = ['Eo *obj']
        if    ftype == EOLIAN_METHOD:   pars_itr = self.parameters
        elif  ftype == EOLIAN_PROP_GET: pars_itr = self.getter_values
        elif  ftype == EOLIAN_PROP_SET: pars_itr = self.setter_values
        else: raise RuntimeError('Unsupported function type: %d' % ftype)
        for p in pars_itr:
            if ftype == EOLIAN_PROP_GET:
                pars.append('{0.type.c_type} *{0.name}'.format(p))
            else:
                pars.append('{0.type.c_type} {0.name}'.format(p))

        pars = ', '.join(pars)
        return '{0} {1}({2})'.format(ret, self.full_c_name_get(ftype), pars)


class Parameter(object):
    def __init__(self, c_param):
        self._obj = c_param # const Eolian_Parameter *

    def __repr__(self):
        return "<eolian.Parameter '{0.name}', {0.direction_str}, type: {0.type}," \
               "optional: {0.is_optional}, nonull: {0.is_nonull}>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_parameter_name_get(self._obj))

    @property
    def direction(self):
        return lib.eolian_parameter_direction_get(self._obj)

    @property
    def direction_str(self):
        direction = lib.eolian_parameter_direction_get(self._obj)
        if direction == EOLIAN_IN_PARAM: return 'in'
        if direction == EOLIAN_OUT_PARAM: return 'out'
        if direction == EOLIAN_INOUT_PARAM: return 'inout'

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
        self._obj = c_type # const Eolian_Type *

    def __repr__(self):
        return "<eolian.Type '{0.full_name}', type: {0.type}, c_type: '{0.c_type}'>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_type_name_get(self._obj))

    @property
    def name2(self):
        return self.name or self.c_type

    @property
    def full_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_type_full_name_get(self._obj))

    @property
    def type(self):
        return lib.eolian_type_type_get(self._obj)

    @property
    def c_type(self):
        return _cstr_to_unicode(ffi, lib.eolian_type_c_type_get(self._obj))

    @property
    def base_type(self):
        return Type(lib.eolian_type_base_type_get(self._obj))

    @property
    def typedecl(self):
        c_typedecl = lib.eolian_type_typedecl_get(self._obj)
        return Typedecl(c_typedecl) if c_typedecl != ffi.NULL else None

    @property
    def aliased_base(self):
        c_type = lib.eolian_type_aliased_base_get(self._obj)
        return Type(c_type) if c_type != ffi.NULL else None




class Typedecl(object):
    def __init__(self, c_typedecl):
        self._obj = c_typedecl # const Eolian_Typedecl *

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

    @property
    def type(self):
        return lib.eolian_typedecl_type_get(self._obj)


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
        return "<eolian.Declaration '{0.name}', type: {0.type}>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_declaration_name_get(self._obj)) 

    @property
    def type(self):
        return lib.eolian_declaration_type_get(self._obj)

    @property
    def data_type(self):
        return Typedecl(lib.eolian_declaration_data_type_get(self._obj))

    @property
    def variable(self):
        return Variable(lib.eolian_declaration_variable_get(self._obj))

    @property
    def class_(self):
        return Class(c_class=lib.eolian_declaration_class_get(self._obj))


class Variable(object):
    def __init__(self, c_var):
        self._obj = c_var # const Eolian_Variable *

    def __repr__(self):
        return "<eolian.Variable '{0.name}', type: {0.data_type}>".format(self)

    @property
    def name(self):
        return _cstr_to_unicode(ffi, lib.eolian_variable_name_get(self._obj))

    @property
    def full_name(self):
        return _cstr_to_unicode(ffi, lib.eolian_variable_full_name_get(self._obj)) 
