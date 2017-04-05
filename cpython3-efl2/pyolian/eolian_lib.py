#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

from ctypes import CDLL, c_uint, c_char_p, c_void_p
from ctypes.util import find_library


lib = CDLL(find_library('eolian'))


### Generic ###

# EAPI Eina_Bool eolian_directory_scan(const char *dir)
lib.eolian_directory_scan.argtypes = [c_char_p,]

# EAPI Eina_Bool eolian_file_parse(const char *filepath)
lib.eolian_file_parse.argtypes = [c_char_p,]


### Eolian_Class ###

# EAPI const Eolian_Class *eolian_class_get_by_file(const char *file_name)
lib.eolian_class_get_by_file.argtypes = [c_char_p,]

# EAPI const Eolian_Class *eolian_class_get_by_name(const char *class_name)
lib.eolian_class_get_by_name.argtypes = [c_char_p,]

# EAPI Eina_Iterator *eolian_class_functions_get(const Eolian_Class *klass, Eolian_Function_Type func_type)
lib.eolian_class_functions_get.argtypes = [c_void_p, c_uint]

# EAPI const Eolian_Event *eolian_class_event_get_by_name(const Eolian_Class *klass, const char *event_name)
lib.eolian_class_event_get_by_name.argtypes = [c_void_p, c_char_p]


# All of the following just return a stringshare (THAT NEED TO BE FREED)
lib.eolian_event_c_name_get.restype = c_void_p
lib.eolian_class_c_name_get.restype = c_void_p
lib.eolian_class_c_get_function_name_get.restype = c_void_p
lib.eolian_class_c_data_type_get.restype = c_void_p
lib.eolian_function_full_c_name_get.restype = c_void_p


# All of the following just return a string
lib.eolian_parameter_name_get.restype = c_char_p
lib.eolian_class_name_get.restype = c_char_p
lib.eolian_class_full_name_get.restype = c_char_p


lib.eolian_class_legacy_prefix_get.restype = c_char_p
lib.eolian_class_eo_prefix_get.restype = c_char_p
lib.eolian_class_data_type_get.restype = c_char_p
lib.eolian_constructor_full_name_get.restype = c_char_p
lib.eolian_event_name_get.restype = c_char_p
lib.eolian_function_name_get.restype = c_char_p

lib.eolian_function_legacy_get.restype = c_char_p
lib.eolian_type_name_get.restype = c_char_p
lib.eolian_type_full_name_get.restype = c_char_p
lib.eolian_type_free_func_get.restype = c_char_p
lib.eolian_type_file_get.restype = c_char_p
lib.eolian_type_c_type_get.restype = c_char_p
lib.eolian_typedecl_name_get.restype = c_char_p
lib.eolian_typedecl_full_name_get.restype = c_char_p
lib.eolian_typedecl_file_get.restype = c_char_p
lib.eolian_typedecl_c_type_get.restype = c_char_p
lib.eolian_typedecl_free_func_get.restype = c_char_p
lib.eolian_typedecl_enum_legacy_prefix_get.restype = c_char_p

