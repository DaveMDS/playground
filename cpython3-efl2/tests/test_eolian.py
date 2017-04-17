#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
#
# Just a simple playground for testing eolian functionalities.
#

import eolian


# Parse all known eo files
if not eolian.system_directory_scan():
    raise(RuntimeError('Eolian, failed to scan system directories'))

if not eolian.all_eo_files_parse():
    raise(RuntimeError('Eolian, failed to parse all EO files'))

if not eolian.all_eot_files_parse():
    raise(RuntimeError('Eolian, failed to parse all EOT files'))

if not eolian.database_validate():
    raise(RuntimeError('Eolian, database validation failed'))


# ALL enums
print('# ' * 40)
for typedecl in eolian.typedecl_all_enums_get():
    print(typedecl)
    for field in typedecl.enum_fields:
        print("  " + str(field))

# ALL structs
print('# ' * 40)
for typedecl in eolian.typedecl_all_structs_get():
    print(typedecl)

# ALL aliases
print('# ' * 40)
for typedecl in eolian.typedecl_all_aliases_get():
    print(typedecl)


# A single class
print('# ' * 40)
cls = eolian.Class('Efl.Gfx')
print('Class: %s' % cls)

for func in cls.properties:
    print('  %s' % func)

    for param in func.getter_values:
        print('    %s' % param)
