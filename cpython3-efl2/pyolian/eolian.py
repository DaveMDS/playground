#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

from enum import IntEnum as Enum
from ctypes import cast, byref, c_uint, c_char_p, c_void_p

# Temporary import hack to be importable from tests/*.py
try:
    from .eolian_lib import lib
except:
    from eolian_lib import lib


### pyolian version ###########################################################
__version__ = "0.99.0"
__version_info__ = ( 0, 99, 0 )


###  enums  ###################################################################

class Eolian_Function_Type(Enum):
    UNRESOLVED = 0
    PROPERTY = 1
    PROP_SET = 2
    PROP_GET = 3
    METHOD = 4

class Eolian_Parameter_Dir(Enum):
    UNKNOWN = 0
    IN = 1
    OUT = 2
    INOUT = 3

class Eolian_Class_Type(Enum):
    UNKNOWN_TYPE = 0
    REGULAR = 1
    ABSTRACT = 2
    MIXIN = 3
    INTERFACE = 4

class Eolian_Object_Scope(Enum):
    UNKNOWN = 0
    PUBLIC = 1
    PRIVATE = 2
    PROTECTED = 3

class Eolian_Typedecl_Type(Enum):
    UNKNOWN = 0
    STRUCT = 1
    STRUCT_OPAQUE = 2
    ENUM = 3
    ALIA = 4

class Eolian_Type_Type(Enum):
    UNKNOWN_TYPE = 0
    VOID = 1
    REGULAR = 2
    COMPLEX = 3
    CLASS = 4
    STATIC_ARRAY = 5
    TERMINATED_ARRAY = 6
    UNDEFINED = 7

class Eolian_Expression_Type(Enum):
    UNKNOWN = 0
    INT = 1
    UINT = 2
    LONG = 3
    ULONG = 4
    LLONG = 5
    ULLONG = 6
    FLOAT = 7
    DOUBLE = 8
    STRING = 9
    CHAR = 10
    NULL = 11
    BOOL = 12
    NAME = 13
    UNARY = 14
    BINAR = 15

class Eolian_Expression_Mask(Enum):
    SINT   = 1 << 0
    UINT   = 1 << 1
    INT    = SINT | UINT
    FLOAT  = 1 << 2
    BOOL   = 1 << 3
    STRING = 1 << 4
    CHAR   = 1 << 5
    NULL   = 1 << 6
    SIGNED = SINT | FLOAT
    NUMBER = INT | FLOAT
    ALL    = NUMBER | BOOL | STRING | CHAR | NULL

class Eolian_Variable_Type(Enum):
    UNKNOWN = 0
    CONSTANT = 1
    GLOBAL = 2

class Eolian_Binary_Operator(Enum):
    INVALID = 0
    ADD = 1  # + int, float
    SUB = 2  # - int, float
    MUL = 3  # * int, float
    DIV = 4  # / int, float
    MOD = 5  # % int
    EQ = 6  # == all types
    NQ = 7  # != all types
    GT = 8  # >  int, float
    LT = 9  # <  int, float
    GE = 10  # >= int, float
    LE = 11  # <= int, float
    AND = 12  # && all types
    OR =  13  # || all types
    BAND = 14  # &  int
    BOR =  15  # |  int
    BXOR = 16  # ^  int
    LSH =  17  # << int
    RSH =  18  # >> int

class Eolian_Unary_Operator(Enum):
    INVALID = 0
    UNM = 1  # - sint
    UNP = 2  # + sint
    NOT = 3   # ! int, float, bool
    BNOT = 4  # ~ int

class Eolian_Declaration_Type(Enum):
    UNKNOWN = 0
    CLASS = 1
    ALIAS = 2
    STRUCT = 3
    ENUM = 4
    VAR = 5

class Eolian_Doc_Token_Type(Enum):
    UNKNOWN = 0
    TEXT = 1
    REF = 2
    MARK_NOTE = 3
    MARK_WARNING = 4
    MARK_REMARK = 5
    MARK_TODO = 6
    MARKUP_MONOSPACE = 7

class Eolian_Doc_Ref_Type(Enum):
    INVALID = 0
    CLASS = 1
    FUNC = 2
    EVENT = 3
    ALIAS = 4
    STRUCT = 5
    STRUCT_FIELD = 6
    ENUM = 7
    ENUM_FIELD = 8
    VAR = 9





###  type converters  #########################################################

def _str_to_bytes(s):
    return s.encode('utf-8')

def _str_to_py(s):
    if s:
        if isinstance(s, bytes):
            return s.decode('utf-8')
        if isinstance(s, c_char_p):
            print("WARNING char* !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return s.value.decode('utf-8')
        if isinstance(s, c_void_p):
            print("WARNING void* !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return cast(s, c_char_p).value.decode('utf-8')
        if isinstance(s, int):
            print("WARNING int !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            return cast(s, c_char_p).value.decode('utf-8')
        print('WARNING !!!!!!!!! Unknown type: %s' % type(s))

def _c_str_to_class(class_name):
    return Class(_str_to_py(class_name))

def _c_eolian_class_to_py(cls):
    return Class(cls)

def _c_eolian_function_to_py(func):
    return Function(func)

def _c_eolian_parameter_to_py(param):
    return Parameter(param)

def _c_eolian_event_to_py(event):
    return Event(event)

def _c_eolian_constructor_to_py(ctor):
    return Constructor(ctor)


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

class Iterator(object):
    """ Generic eina iterator wrapper """
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
    """ TODO DOC """
    def __init__(self, cls):
        if isinstance(cls, c_void_p):
            self._obj = c_void_p(cls.value)  # const Eolian_Class *
        elif isinstance(cls, str) and cls.startswith('Efl.'):
            self._obj = lib.eolian_class_get_by_name(_str_to_bytes(cls))
        elif isinstance(cls, str):
            self._obj = lib.eolian_class_get_by_file(_str_to_bytes(cls))
        else:
            raise TypeError('Invalid Class constructor of type: %s ' % type(cls))

    def __repr__(self):
        return "<eolian.Class '{0.full_name}', prefix '{0.eo_prefix}'>".format(self)

    @property
    def name(self):
        return _str_to_py(lib.eolian_class_name_get(self._obj))

    @property
    def full_name(self):
        return _str_to_py(lib.eolian_class_full_name_get(self._obj))

    @property
    def c_name(self):
        s = lib.eolian_class_c_name_get(self._obj)
        ret = _str_to_py(s)
        lib.eina_stringshare_del(s)
        return ret

    @property
    def c_get_function_name(self):
        s = lib.eolian_class_c_get_function_name_get(self._obj)
        ret = _str_to_py(s)
        lib.eina_stringshare_del(s)
        return ret

    @property
    def c_data_type(self):
        s = lib.eolian_class_c_data_type_get(self._obj)
        ret = _str_to_py(s)
        lib.eina_stringshare_del(s)
        return ret

    @property
    def legacy_prefix(self):
        return _str_to_py(lib.eolian_class_legacy_prefix_get(self._obj))

    @property
    def eo_prefix(self):
        return _str_to_py(lib.eolian_class_eo_prefix_get(self._obj))

    @property
    def type(self):
        return Eolian_Class_Type(lib.eolian_class_type_get(self._obj))
    
    @property
    def data_type(self):
        return _str_to_py(lib.eolian_class_data_type_get(self._obj))

    @property
    def constructors(self):
        return Iterator(_c_eolian_constructor_to_py,
                        lib.eolian_class_constructors_get(self._obj))

    @property
    def events(self):
        return Iterator(_c_eolian_event_to_py,
                        lib.eolian_class_events_get(self._obj))

    def event_get_by_name(self, event_name):
        c_event = lib.eolian_class_event_get_by_name(self._obj, event_name)
        return Event(c_event) if c_event else None

    @property
    def inherits(self):
        return Iterator(_c_str_to_class,
                        lib.eolian_class_inherits_get(self._obj))

    @property
    def inherits_full(self):
        L = []
        def do_class_recursive(cls):
            for other in cls.inherits:
                if not other in L:
                    L.append(other)
                do_class_recursive(other)

        do_class_recursive(self)
        return L

    @property
    def base_class(self):
        inherits = list(self.inherits)
        if len(inherits) > 0:
            return inherits[0]

    @property
    def namespaces(self):
        return Iterator(_str_to_py,
                        lib.eolian_class_namespaces_get(self._obj))

    @property
    def file(self):
        return _str_to_py(lib.eolian_class_file_get(self._obj))

    @property
    def ctor_enable(self):
        return bool(lib.eolian_class_ctor_enable_get(self._obj))

    @property
    def dtor_enable(self):
        return bool(lib.eolian_class_dtor_enable_get(self._obj))

    def function_get_by_name(self, func_name, ftype):
        f = lib.eolian_class_function_get_by_name(self._obj, func_name, ftype)
        return Function(f)

    def functions_get(self, ftype):
        return Iterator(_c_eolian_function_to_py,
                        lib.eolian_class_functions_get(self._obj, ftype))

    @property
    def methods(self):
        return self.functions_get(Eolian_Function_Type.METHOD)

    @property
    def properties(self):
        return self.functions_get(Eolian_Function_Type.PROPERTY)

    @property
    def getters(self):
        return self.functions_get(Eolian_Function_Type.PROP_GET)

    @property
    def setters(self):
        return self.functions_get(Eolian_Function_Type.PROP_SET)


class Constructor(object):
    """ TODO DOC """
    def __init__(self, c_ctor):
        if isinstance(c_ctor, c_void_p):
            self._obj = c_void_p(c_ctor.value) # const Eolian_Constructor *
        else:
            raise TypeError('Invalid Class constructor')

    def __repr__(self):
        return "<eolian.Constructor '{0.full_name}', optional: {0.is_optional}>".format(self)

    @property
    def full_name(self):
        return _str_to_py(lib.eolian_constructor_full_name_get(self._obj))

    @property
    def function(self):
        return Function(lib.eolian_constructor_function_get(self._obj))

    @property
    def is_optional(self):
        return bool(lib.eolian_constructor_is_optional(self._obj))

    @property
    def class_(self):
        return Class(lib.eolian_constructor_class_get(self._obj))


class Event(object):
    """ TODO DOC """
    def __init__(self, c_event):
        if isinstance(c_event, c_void_p):
            self._obj = c_void_p(c_event.value) # const Eolian_Event *
        else:
            raise TypeError('Invalid Class constructor')

    def __repr__(self):
        return "<eolian.Event '{0.name}', c_name: '{0.c_name}'>".format(self)

    @property
    def name(self):
        return _str_to_py(lib.eolian_event_name_get(self._obj))

    @property
    def c_name(self):
        s = lib.eolian_event_c_name_get(self._obj)
        ret = _str_to_py(s)
        lib.eina_stringshare_del(s)
        return ret

    @property
    def type(self):
        c_type = lib.eolian_event_type_get(self._obj)
        return Type(c_type) if c_type else None

    @property
    def documentation(self):
        c_doc = lib.eolian_event_documentation_get(self._obj)
        return Documentation(c_doc) if c_doc else None

    @property
    def scope(self):
        return Eolian_Object_Scope(lib.eolian_event_scope_get(self._obj))

    @property
    def is_beta(self):
        return bool(lib.eolian_event_is_beta(self._obj))

    @property
    def is_hot(self):
        return bool(lib.eolian_event_is_hot(self._obj))

    @property
    def is_restart(self):
        return bool(lib.eolian_event_is_restart(self._obj))



class Function(object):
    """ TODO DOC """
    def __init__(self, c_func):
        if isinstance(c_func, c_void_p):
            self._obj = c_void_p(c_func.value)  # const Eolian_Function *
        else:
            raise TypeError('Invalid Class constructor')

    def __repr__(self):
        return "<eolian.Function '{0.name}'>".format(self)

    @property
    def name(self):
        return _str_to_py(lib.eolian_function_name_get(self._obj))

    def full_c_name_get(self, ftype, use_legacy=False):
        s = lib.eolian_function_full_c_name_get(self._obj, ftype, use_legacy)
        ret = _str_to_py(s)
        lib.eina_stringshare_del(s)
        return ret

    @property
    def full_c_method_name(self):
        return self.full_c_name_get(Eolian_Function_Type.METHOD)

    @property
    def full_c_getter_name(self):
        return self.full_c_name_get(Eolian_Function_Type.PROP_GET)
    
    @property
    def full_c_setter_name(self):
        return self.full_c_name_get(Eolian_Function_Type.PROP_SET)
    
    @property
    def type(self):
        return Eolian_Function_Type(lib.eolian_function_type_get(self._obj))

    def scope_get(self, ftype):
        return Eolian_Object_Scope(lib.eolian_function_scope_get(self._obj, ftype))

    @property
    def method_scope(self):
        return self.scope_get(Eolian_Function_Type.METHOD)

    @property
    def getter_scope(self):
        return self.scope_get(Eolian_Function_Type.PROP_GET)

    @property
    def setter_scope(self):
        return self.scope_get(Eolian_Function_Type.PROP_SET)

    def legacy_get(self, ftype):
        return _str_to_py(lib.eolian_function_legacy_get(self._obj, ftype))
    
    def is_legacy_only(self, ftype):
        return bool(lib.eolian_function_is_legacy_only(self._obj, ftype))

    @property
    def is_class(self):
        return bool(lib.eolian_function_is_class(self._obj))

    @property
    def is_c_only(self):
        return bool(lib.eolian_function_is_c_only(self._obj))

    @property
    def is_beta(self):
        return bool(lib.eolian_function_is_beta(self._obj))

    @property
    def object_is_const(self):
        return bool(lib.eolian_function_object_is_const(self._obj))

    @property
    def class_(self):
        c_cls = lib.eolian_type_class_get(self._obj)
        return Class(c_cls) if c_cls else None
    
    def is_constructor(self, klass):
        return bool(lib.eolian_function_is_constructor(self._obj, klass._obj))

    @property
    def parameters(self):
        return Iterator(_c_eolian_parameter_to_py,
                        lib.eolian_function_parameters_get(self._obj))

    def values_get(self, ftype):
        return Iterator(_c_eolian_parameter_to_py,
                        lib.eolian_property_values_get(self._obj, ftype))

    @property
    def getter_values(self):
        return self.values_get(Eolian_Function_Type.PROP_GET)

    @property
    def setter_values(self):
        return self.values_get(Eolian_Function_Type.PROP_SET)

    def return_type_get(self, ftype):
        t = lib.eolian_function_return_type_get(self._obj, ftype)
        return Type(t) if t else None

    @property
    def method_return_type(self):
        return self.return_type_get(Eolian_Function_Type.METHOD)

    @property
    def getter_return_type(self):
        return self.return_type_get(Eolian_Function_Type.PROP_GET)

    @property
    def setter_return_type(self):
        return self.return_type_get(Eolian_Function_Type.PROP_SET)
    
    @property
    def prop_readable(self):
        # TODO: maybe there is a better way to do this...
        ftype = Eolian_Function_Type.PROP_GET
        scope = lib.eolian_function_scope_get(self._obj, ftype)
        return True if scope != Eolian_Object_Scope.UNKNOWN else False

    @property
    def prop_writable(self):
        # TODO: maybe there is a better way to do this...
        ftype = Eolian_Function_Type.PROP_SET
        scope = lib.eolian_function_scope_get(self._obj, ftype)
        return True if scope != Eolian_Object_Scope.UNKNOWN else False

    

class Parameter(object):
    """ TODO DOC """
    def __init__(self, c_param):
        if isinstance(c_param, c_void_p):
            self._obj = c_void_p(c_param.value)  # const Eolian_Parameter *
        else:
            raise TypeError('Invalid Class constructor')

    def __repr__(self):
        return "<eolian.Parameter '{0.name}', type: {0.type}," \
               " optional: {0.is_optional}, nonull: {0.is_nonull}>".format(self)

    @property
    def name(self):
        return _str_to_py(lib.eolian_parameter_name_get(self._obj))

    # @property
    # def name_fixed(self):
        # name = _str_to_py(lib.eolian_parameter_name_get(self._obj))
        # if name in PY_KW:
            # return name + '_'
        # return name

    # name = name_fixed

    @property
    def direction(self):
        return Eolian_Parameter_Dir(lib.eolian_parameter_direction_get(self._obj))

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
        c_type = lib.eolian_parameter_type_get(self._obj)
        return Type(c_type) if c_type else None 


class Type(object):
    """ TODO DOC """
    def __init__(self, c_type):
        # const Eolian_Type *
        if isinstance(c_type, c_void_p):
            self._obj = c_void_p(c_type.value)
        elif isinstance(c_type, int):
            self._obj = c_void_p(c_type)
        else:
            raise TypeError('Invalid Class constructor')

    def __repr__(self):
        return "<eolian.Type '{0.full_name}', type: {0.type}, c_type: '{0.c_type}'>".format(self)

    @property
    def name(self):
        return _str_to_py(lib.eolian_type_name_get(self._obj))

    @property
    def full_name(self):
        return _str_to_py(lib.eolian_type_full_name_get(self._obj))

    @property
    def namespaces(self):
        return Iterator(_str_to_py,
                        lib.eolian_type_namespaces_get(self._obj))

    @property
    def free_func(self):
        return _str_to_py(lib.eolian_type_free_func_get(self._obj))

    @property
    def type(self):
        return Eolian_Type_Type(lib.eolian_type_type_get(self._obj))

    @property
    def base_type(sel):
        c_type = lib.eolian_type_base_type_get(self._obj)
        return Type(c_type) if c_type else None 

    @property
    def next_type(sel):
        c_type = lib.eolian_type_next_type_get(self._obj)
        return Type(c_type) if c_type else None 

    @property
    def aliased_base(sel):
        c_type = lib.eolian_type_aliased_base_get(self._obj)
        return Type(c_type) if c_type else None 

    @property
    def class_(self):
        c_cls = lib.eolian_type_class_get(self._obj)
        return Class(c_cls) if c_cls else None

    @property
    def file(self):
        return _str_to_py(lib.eolian_type_file_get(self._obj))
    
    @property
    def array_size(self):
        return lib.eolian_type_array_size_get(self._obj)

    @property
    def is_own(self):
        return bool(lib.eolian_type_is_own(self._obj))

    @property
    def is_const(self):
        return bool(lib.eolian_type_is_const(self._obj))

    @property
    def is_ptr(self):
        return bool(lib.eolian_type_is_ptr(self._obj))

    @property
    def c_type(self):
        return _str_to_py(lib.eolian_type_c_type_get(self._obj))


class Typedecl(object):
    """ TODO DOC """
    def __init__(self, c_typedecl):
        if isinstance(c_typedecl, c_void_p):
            self._obj = c_void_p(c_typedecl.value)  # const Eolian_Typedecl *
        else:
            raise TypeError('Invalid Class constructor')

    def __repr__(self):
        return "<eolian.Typedecl '{0.name}'>".format(self)

    @property
    def name(self):
        return _str_to_py(lib.eolian_typedecl_name_get(self._obj))

    @property
    def full_name(self):
        return _str_to_py(lib.eolian_typedecl_full_name_get(self._obj))

    @property
    def file(self):
        return _str_to_py(lib.eolian_typedecl_file_get(self._obj))

    @property
    def type(self):
        return Eolian_Typedecl_Type(lib.eolian_typedecl_type_get(self._obj))

    @property
    def c_type(self):
        return _str_to_py(lib.eolian_typedecl_c_type_get(self._obj))

    @property
    def namespaces(self):
        return Iterator(_str_to_py,
                        lib.eolian_typedecl_namespaces_get(self._obj))

    @property
    def free_func(self):
        return _str_to_py(lib.eolian_typedecl_free_func_get(self._obj))

    @property
    def is_extern(self):
        return bool(lib.eolian_typedecl_is_extern(self._obj))

    # @property
    # def enum_fields(self):
        # return Iterator(_c_eolian_enum_field_to_py,
                        # lib.eolian_typedecl_enum_fields_get(self._obj))

    @property
    def base_type(self):
        c_type = lib.eolian_typedecl_base_type_get(self._obj)
        return Type(c_type) if c_type else None

    @property
    def aliased_base(self):
        c_type = lib.eolian_typedecl_aliased_base_get(self._obj)
        return Type(c_type) if c_type else None

    @property
    def documentation(self):
        c_doc = lib.eolian_typedecl_documentation_get(self._obj)
        return Documentation(c_doc) if c_doc else None

    @property
    def enum_legacy_prefix(self):
        return _str_to_py(lib.eolian_typedecl_enum_legacy_prefix_get(self._obj))
    
    

class Documentation(object):
    """ TODO DOC """
    def __init__(self, c_doc):
        if isinstance(c_doc, c_void_p):
            self._obj = c_void_p(c_doc.value)  # const Eolian_Documentation *
        else:
            raise TypeError('Invalid Class constructor')

    # def __repr__(self):
        # return "<eolian.Typedecl '{0.name}'>".format(self)

