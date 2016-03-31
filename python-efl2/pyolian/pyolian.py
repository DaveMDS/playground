###############################################################################
#######                  THIS FILE IS MANUALLY WRITTEN                  #######
###############################################################################

from __future__ import absolute_import, print_function, division

import os
import datetime

from . import eolian




verbose = False

def ERR(*args):
    print(*(('PYOLIAN    ERROR:', ) + args))
    exit(1)

def WRN(*args):
    print(*(('PYOLIAN    WARNING:', ) + args))

def DBG(*args):
    if verbose:
        print(*(('PYOLIAN   ', ) + args))

def INF(*args):
    print(*(('PYOLIAN   ', ) + args))


def uncapitalize(s):
    return s[0].lower() + s[1:]

COPYRIGHT="""# Copyright (C) 2007-{} various contributors (see AUTHORS)
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
""".format(datetime.datetime.now().year)


def generate_all(package_dir, headers_dir, be_verbose=True):
    INF('generator startup')

    global verbose
    verbose = be_verbose

    INF('system directory scan')
    if not eolian.system_directory_scan():
        ERR('Failed to scan system directories')

    INF('parsing all EOT files')
    if not eolian.all_eot_files_parse():
        ERR('Failed to parse EOT files')


    ###
    # generate('elm_button.eo', 'elm_button_GEN.py')
    generate(package_dir, headers_dir, 'elm_win.eo', 'elementary.py.GEN', 'elementary.h.GEN',
             excludes=['elm_obj_win_keygrab_set', 'elm_obj_win_keygrab_get'])
    # generate(package_dir, headers_dir, 'elm_label.eo', 'elementary.py.GEN', 'elementary.h.GEN')
    # generate(package_dir, headers_dir, 'ecore_timer.eo', 'ecore.py.GEN', 'ecore.h.GEN')
    # generate(package_dir, headers_dir, 'ecore_exe.eo', 'ecore.py.GEN', 'ecore.h.GEN')
    # generate('ecore_exe.eo', 'ecore_timer.py.GEN', 'ecore.h.GEN')

    return 0 # success

already_started_py_files = set()
already_started_header_files = set()

def generate(package_dir, headers_dir, eo_fname, out_fname, out_header_fname, excludes=[]):

    out_fname = os.path.join(package_dir, out_fname)
    out_header_fname = os.path.join(headers_dir, out_header_fname)
    INF('generating: "{}"  from: "{}"'.format(out_fname, eo_fname))

    if not eolian.file_parse(eo_fname):
        ERR('Failed parsing file')

    if not eolian.database_validate():
        ERR('Failed validating database.')

    mode = 'a' if out_header_fname in already_started_header_files else 'w'
    with open(out_header_fname, mode) as hf:
        mode = 'a' if out_fname in already_started_py_files else 'w'
        with open(out_fname, mode) as f:
            gen_file(eo_fname, f, hf)
            gen_enums(eo_fname, f, hf)
            gen_typedefs(eo_fname, f, hf)
            gen_class(eo_fname, f, hf, excludes)

    already_started_header_files.add(out_header_fname)
    already_started_py_files.add(out_fname)

def gen_file(eo_fname, fp, hfp):
    # py file
    
    fp.write(COPYRIGHT)
    fp.write("""
###############################################################################
####                  THIS FILE IS GENERATED, do not edit.                 ####
###############################################################################
from ._efl_ffi import ffi, lib
from . import eo
""")

    # header file
    already_started_header_files.add(eo_fname)
    hfp.write("""
///////////////////////////////////////////////////////////////////////////////
////                  THIS FILE IS GENERATED, do not edit.                 ////
///////////////////////////////////////////////////////////////////////////////
""")

def gen_enums(eo_fname, fp, hfp):
    # TODO generate "new style" Enums instead
    for enum in eolian.typedecl_enums_get_by_file(eo_fname):
        c_name = enum.full_name.replace('.', '_')
        DBG('generating enum: ', enum.full_name)
        fp.write('\n# enum: {0}\n'.format(enum.name))
        hfp.write('\nenum _{0}{{\n'.format(c_name))

        for field in enum.enum_fields:
            fp.write('{0} = lib.{0}\n'.format(field.c_name))
            hfp.write('    {0},\n'.format(field.c_name))

        hfp.write('    ...\n')
        hfp.write('}};\n'.format(c_name))

def gen_typedefs(eo_fname, fp, hfp):
    for d in eolian.declarations_get_by_file(eo_fname):
        DBG('generating typedef: ', d.name)
        t = d.type
        c_name = d.name.replace('.', '_')

        if t == eolian.EOLIAN_DECL_CLASS:
            hfp.write("""
// {0} class
typedef Eo {1};
const Eo_Class {2}_class_get(void);
static Eo_Class *const {3}_CLASS;
            """.format(d.name, c_name, c_name.lower(), c_name.upper()))

        elif t == eolian.EOLIAN_DECL_ENUM:
            hfp.write('typedef enum _{0} {0};\n'.format(c_name))

        else:
            WRN('Unknow typedef type: ', t)

def gen_class(eo_fname, fp, hfp, excludes):
    klass = eolian.Class(eo_fname)
    DBG('generating class: ', klass.full_name)
    DBG(klass)

    ### Class definition (change "Eo.Base" to "eo.Base")
    inherits = ', '.join( [ uncapitalize(c) for c in klass.inherits ])
    fp.write("""
@eo._class_register('{0.full_name}')
class {0.name}({1}):
    " TODO EVENTS "
    def __init__(self):
        pass
    """.format(klass, inherits))

    ### Constructor
    # TO BE DONE

    ### Methods
    hfp.write('\n// {} methods\n'.format(klass.full_name))
    for func in sorted(klass.functions, key=lambda f: f.name):
        if func.full_c_name in excludes:
            DBG('SKIPPED', func)
            continue
        if func.is_constructor:
            continue
        gen_method(klass, func, fp, hfp)

    ### Properties
    hfp.write('\n// {} properties\n'.format(klass.full_name))
    for func in sorted(klass.properties, key=lambda p: p.name):
        if func.full_c_name in excludes:
            DBG('SKIPPED', func)
            continue
        DBG('generating property: {}.{} {}'.format(klass.full_name, func.name, func.type))

        ftype = func.type
        if ftype == eolian.EOLIAN_PROPERTY or ftype == eolian.EOLIAN_PROP_GET:
            gen_getter(klass, func, fp, hfp)
        if ftype == eolian.EOLIAN_PROPERTY or ftype == eolian.EOLIAN_PROP_SET:
            gen_setter(klass, func, fp, hfp)

        continue # REMOVE 
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

def gen_method(klass, func, fp, hfp):
    DBG('generating method: {}.{}(self, ...)'.format(klass.full_name, func.name))
    params = ', '.join( [ p.name for p in func.parameters ] )
    py_params = ('self, ' + params) if params else 'self'
    c_params = ('self._obj, ' + params) if params else 'self._obj'

    # py file
    fp.write("""
    def {0.name}({1}):
        return lib.{0.full_c_name}({2})
    """.format(func, py_params, c_params))

    # header file
    hfp.write('{};\n'.format(func.full_c_define))

def gen_getter(klass, func, fp, hfp):
    DBG('generating      get: ', func.full_c_name)

    # py file
    fp.write("""
    @property
    def {}({}):
        return 'x'
    """.format(func.name, ', '.join(('self', '...'))))
    
def gen_setter(klass, func, fp, hfp):
    DBG('generating      set: ', func.full_c_name)
    
    

if __name__ == '__main__':

    print('Usage: "python setup.py generate" from the package root dir.')


