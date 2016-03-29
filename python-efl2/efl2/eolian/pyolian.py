###############################################################################
#######                  THIS FILE IS MANUALLY WRITTEN                  #######
###############################################################################

from __future__ import absolute_import, print_function, division

import os
# from eolian import ffi, lib
import eolian


def ERR(*args):
    print('ERROR:' + str(args))
    exit(1)

def DBG(*args):
    print('PYOLIAN    ' + str(args))

def OUT(*args):
    print('PYOLIAN   ' + str(args))

COPYRIGHT="""# Copyright (C) 2007-2016 various contributors (see AUTHORS)
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
"""

def uncapitalize(s):
    return s[0].lower() + s[1:]

def gen_class(eo_fname, fp, hfp):
    klass = eolian.Class(eo_fname)
    OUT("generating class: ", klass.name, klass.full_name)
    print(klass)

    ### Definition
    # change "Eo.Base" to "eo.Base"
    inherits = ', '.join( [ uncapitalize(c) for c in klass.inherits ])

    fp.write("""
class {0.name}({1}):
    def __init__(self):
        pass
    """.format(klass, inherits))

    ### Constructor
    # TO BE DONE

    ### Methods
    hfp.write('\n// {} methods\n'.format(klass.full_name))
    for func in klass.functions:
        if not func.is_constructor:

            
            params = ', '.join( [ p.name for p in func.parameters ] )
            py_params = ('self, ' + params) if params else 'self'
            c_params = ('self._obj, ' + params) if params else 'self._obj'

            for p in func.parameters:
                print(p)

            # py file
            fp.write("""
    def {0.name}({1}):
        return lib.{0.full_c_name}({2})
            """.format(func, py_params, c_params))

            # header file
            hfp.write('{};\n'.format(func.full_c_define))
            print("FUN", func.full_c_define)

    ### Properties
    hfp.write('\n// {} properties\n'.format(klass.full_name))
    for func in klass.properties:
        print(func)

        # py file
        params = ', '.join( [ p.name for p in func.parameters ] )
        py_params = ('self, ' + params) if params else 'self'
        c_params = ('self._obj, ' + params) if params else 'self._obj'
            
        fp.write("""
    @property
    def {0.name}({1}):
        return lib.{0.full_c_name}({2})
        """.format(func, py_params, c_params))

        # header file
        hfp.write('{};\n'.format(func.full_c_define))

        
        # TODO setters...


def gen_enums(eo_fname, fp, hfp):
    # TODO generate "new style" Enums instead
    for enum in eolian.typedecl_enums_get_by_file(eo_fname):
        fp.write('\n# enum: {}\n'.format(enum.name))
        hfp.write('\ntypedef enum {\n')

        for field in enum.enum_fields:
            fp.write('{0} = lib.{0}\n'.format(field.c_name))
            hfp.write('    {},\n'.format(field.c_name))

        hfp.write('    ...,\n')
        hfp.write('}} {};\n'.format(enum.full_name.replace('.', '_')))


def gen_file(eo_fname, fp, hfp):
    print(fp)
    fp.write(COPYRIGHT)
    fp.write("""
###############################################################################
####                  THIS FILE IS GENERATED, do not edit.                 ####
###############################################################################
from ._efl_ffi import ffi, lib
from . import eo
""")

    hfp.write("""
///////////////////////////////////////////////////////////////////////////////
////                  THIS FILE IS GENERATED, do not edit.                 ////
///////////////////////////////////////////////////////////////////////////////
""")

    # what's this for ???
    for d in eolian.declarations_get_by_file(eo_fname):
        print(d)


def generate(eo_fname, out_fname, out_header_fname):
    OUT('generating: "{}"  from: "{}"'.format(out_fname, eo_fname))

    if not eolian.file_parse(eo_fname):
        ERR('Failed parsing file')

    if not eolian.database_validate():
        ERR('Failed validating database.')

    with open(os.path.join(os.path.dirname(__file__), out_header_fname), 'w') as hf:
        with open(os.path.join(os.path.dirname(__file__), out_fname), 'w') as f:
            gen_file(eo_fname, f, hf)
            gen_enums(eo_fname, f, hf)
            gen_class(eo_fname, f, hf)

if __name__ == '__main__':
    OUT('Generator startup')

    OUT('system directory scan')
    if not eolian.system_directory_scan():
        ERR('Failed to scan system directories')

    OUT('parsing all EOT files')
    if not eolian.all_eot_files_parse():
        ERR('Failed to parse EOT files')


    ###
    # generate('elm_button.eo', 'elm_button_GEN.py')
    generate('elm_win.eo', 'elm_win_GEN.py', 'elm_GEN.h')
    generate('ecore_timer.eo', 'ecore_timer_GEN.py', 'ecore_GEN.h')
    # generate('ecore_exe.eo', 'ecore_timer_GEN.py', 'ecore_GEN.h')

    

