#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
#
# Just a simple playground for testing eolian functionalities.
#

import eolian


if not eolian.system_directory_scan():
    raise(RuntimeError('Eolian, failed to scan system directories'))

if not eolian.all_eo_files_parse():
    raise(RuntimeError('Eolian, failed to parse all EO files'))

if not eolian.all_eot_files_parse():
    raise(RuntimeError('Eolian, failed to parse all EOT files'))

if not eolian.database_validate():
    raise(RuntimeError('Eolian, database validation failed'))



cls = eolian.Class('Efl.Gfx')
print('Class: %s' % cls)


for func in cls.properties:
    print('  %s' % func)

    for param in func.getter_values:
        print('    %s' % param)
