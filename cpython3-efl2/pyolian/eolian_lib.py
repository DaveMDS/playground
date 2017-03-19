#! /usr/bin/env python3
# encoding: utf-8

from ctypes import CDLL, c_uint, c_char_p, c_void_p


lib = CDLL('libeolian.so')


### Generic ###

# EAPI Eina_Bool eolian_directory_scan(const char *dir)
lib.eolian_directory_scan.argtypes = [c_char_p,]

# EAPI Eina_Bool eolian_system_directory_scan(void)

# EAPI Eina_Bool eolian_all_eo_files_parse(void)

# EAPI Eina_Bool eolian_all_eot_files_parse(void)

# EAPI Eina_Bool eolian_database_validate()

# EAPI Eina_Bool eolian_file_parse(const char *filepath)
lib.eolian_file_parse.argtypes = [c_char_p,]


### Eolian_Class ###

# EAPI const Eolian_Class *eolian_class_get_by_file(const char *file_name)
lib.eolian_class_get_by_file.argtypes = [c_char_p,]

# EAPI const Eolian_Class *eolian_class_get_by_name(const char *class_name)
lib.eolian_class_get_by_name.argtypes = [c_char_p,]

# EAPI Eina_Stringshare *eolian_class_name_get(const Eolian_Class *klass)
lib.eolian_class_name_get.restype = c_char_p

# EAPI Eina_Stringshare *eolian_class_full_name_get(const Eolian_Class *klass)
lib.eolian_class_full_name_get.restype = c_char_p

# EAPI Eina_Stringshare *eolian_class_legacy_prefix_get(const Eolian_Class *klass)
lib.eolian_class_legacy_prefix_get.restype = c_char_p

# EAPI Eina_Stringshare* eolian_class_eo_prefix_get(const Eolian_Class *klass)
lib.eolian_class_eo_prefix_get.restype = c_char_p

# EAPI Eina_Stringshare *eolian_class_data_type_get(const Eolian_Class *klass)
lib.eolian_class_data_type_get.restype = c_char_p

# EAPI Eina_Stringshare *eolian_class_c_get_function_name_get(const Eolian_Class *klass)
lib.eolian_class_c_get_function_name_get.restype = c_char_p

# EAPI Eina_Stringshare *eolian_class_file_get(const Eolian_Class *klass);
lib.eolian_class_file_get.restype = c_char_p

