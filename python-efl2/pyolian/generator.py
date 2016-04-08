###############################################################################
#######                  THIS FILE IS MANUALLY WRITTEN                  #######
###############################################################################

from __future__ import absolute_import, print_function, division

import os
from os.path import relpath as REL
import datetime

from . import eolian

# logging utils
be_verbose = False
def ERR(*args): print(*(('PYOLIAN    ERROR:', ) + args))
def WRN(*args): print(*(('PYOLIAN    WARNING:', ) + args))
def VRB(*args): print(*(('PYOLIAN   ', ) + args)) if be_verbose else None
def INF(*args): print(*(('PYOLIAN   ', ) + args))


def uncapitalize(s):
    return s[0].lower() + s[1:]


###  Templates  ###

COPYRIGHT = """{0} Copyright (C) 2007-%d various contributors (see AUTHORS)
{0}
{0} This file is part of Python-EFL.
{0}
{0} Python-EFL is free software; you can redistribute it and/or
{0} modify it under the terms of the GNU Lesser General Public
{0} License as published by the Free Software Foundation; either
{0} version 3 of the License, or (at your option) any later version.
{0}
{0} Python-EFL is distributed in the hope that it will be useful,
{0} but WITHOUT ANY WARRANTY; without even the implied warranty of
{0} MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
{0} Lesser General Public License for more details.
{0}
{0} You should have received a copy of the GNU Lesser General Public License
{0} along with this Python-EFL.  If not, see <http://www.gnu.org/licenses/>.

{0} {0}                                                {0} {0}
{0} {0}         File automatically generated           {0} {0}
{0} {0}             !!! DO NOT EDIT !!!                {0} {0}
{0} {0}                                                {0} {0}
""" % datetime.datetime.now().year

PY_HEAD = """
from efl2._efl_ffi import ffi, lib
from efl2 import eo
"""

INIT_HEAD = """

"""

CLASS_TYPEDEF = """
// {0} class
typedef Eo {1};
const Eo_Class *{2}(void);
"""

CLASS_DEF = """
@eo._class_register('{0}')
class {1}({2}):
"""

CLASS_CTOR_DEFAULT = """
    def __init__(self, parent=None, **kargs):
        eo.Base.__init__(self, lib.{}(), parent, **kargs)
"""

CLASS_METHOD_RET = """
    def {0}({1}):
        \""" {2} \"""
        return {3}
"""

CLASS_METHOD_NORET = """
    def {0}({1}):
        \""" {2} \"""
        lib.{3}({4})
"""

CLASS_METHOD = """
    def {0}({1}):
        \""" {2} \"""
"""

CLASS_GETTER = """
    def {0}_get(self):
        \""" {1} \"""
"""

CLASS_SETTER = """
    def {0}_set(self, {1}):
        \""" {2} \"""
"""

MANUAL_CONSTRUCTORS = {
'Elm.Win':   """
    def __init__(self, name, type, *args, **kargs):
        # custom constructor
        eo.Base.__init__(self, lib.ELM_WIN_CLASS, ffi.NULL, False)
        lib.elm_obj_win_type_set(self._obj, type)
        lib.elm_obj_win_name_set(self._obj, _to_bytes(name))
        eo.Base.__init__end__(self, **kargs)

        print("Win INIT")
""",
'Ecore.Timer': """
    TODO XXX
""",
}

MANUAL_EXCLUDES = [
'ecore_mainloop_select_func_get', # type @extern Ecore_Select_Function: __undefined_type;
# 'elm_obj_widget_event_callback_del', # return void *
# 'elm_obj_win_illume_command_send', # eolian.Type 'Elm.Illume_Command'
# 'evas_obj_clipees_get', # return Eina_List *
# 'evas_obj_smart_data_get', # return void *
# 'evas_obj_map_get', # const Evas_Map *
]

class Generator(object):
    def __init__(self, main_py_path, headers_path, verbose=False):
        global be_verbose
        be_verbose = verbose
        self.main_py_path = main_py_path
        self.headers_path = headers_path

        INF('generator startup')
        INF('path for python files:', self.main_py_path)
        INF('path for cffi headers:', self.headers_path)

        self.already_started_py_files = set()
        self.already_started_header_files = set()
        self.already_started_init_files = set()

    def generate_all(self):
        INF('system directory scan')
        if not eolian.system_directory_scan():
            ERR('Failed to scan system directories')
            return False

        INF('parsing all EOT files')
        if not eolian.all_eot_files_parse():
            ERR('Failed to parse EOT files')
            return False

        ret = self.generate_eo_file('ecore_mainloop.eo', 'ecore') # should be efl/gfx
        # ret = self.generate_eo_file('efl_gfx_base.eo', 'gfx') # should be efl/gfx
        # ret = self.generate_eo_file('evas_object.eo', 'evas')
        # ret = self.generate_eo_file('elm_widget.eo', 'elm')
        # ret = self.generate_eo_file('elm_win.eo', 'elm')
        # ret = self.generate_eo_file('elm_label.eo', 'elm')

        INF('generation complete')
        return ret

    def generate_eo_file(self, eo_fname, py_pkg):
        VRB('=' * 79)
        INF('generating from: ', eo_fname)

        if not eolian.file_parse(eo_fname):
            ERR('Failed parsing file')
            return False

        if not eolian.database_validate():
            ERR('Failed validating database.')
            return False

        # header file
        header_fname = os.path.join(self.headers_path, eo_fname.replace('.eo', '.h'))
        VRB('to header:  ', REL(header_fname))

        # package __init__.py file
        py_pkg = os.path.join(self.main_py_path, py_pkg)
        if not os.path.exists(py_pkg):
            VRB('creating python package:', REL(py_pkg))
            os.makedirs(py_pkg)
        init_fname = os.path.join(py_pkg, '__init__.py')
        VRB('to package: ', REL(init_fname))

        # python file
        py_fname = os.path.join(py_pkg, eo_fname.replace('.eo', '.py'))
        VRB('to python:  ', REL(py_fname))


        # open initf
        mode = 'a' if init_fname in self.already_started_init_files else 'w'
        with open(init_fname, mode) as initf:
            if mode == 'w':
                initf.write(COPYRIGHT.format('#'))
                initf.write(INIT_HEAD)

            # open headerf
            mode = 'a' if header_fname in self.already_started_header_files else 'w'
            with open(header_fname, mode) as headerf:
                if mode == 'w':
                    headerf.write(COPYRIGHT.format('//'))

                # open pythonf (f)
                mode = 'a' if py_fname in self.already_started_py_files else 'w'
                with open(py_fname, mode) as f:
                    if mode == 'w':
                        f.write(COPYRIGHT.format('#'))
                        f.write(PY_HEAD.format('#'))

                    ### generate all ###
                    self.emit_enums(eo_fname, f, headerf, initf)
                    self.emit_typedefs(eo_fname, f, headerf, initf)
                    self.emit_class(eo_fname, f, headerf, initf)#, excludes)

                    initf.write('from .{} import *\n'.format(eo_fname.replace('.eo', '')))

        self.already_started_py_files.add(py_fname)
        self.already_started_header_files.add(header_fname)
        self.already_started_init_files.add(init_fname)

        return True

    def emit_enums(self, eo_fname, f, headerf, initf):
        # TODO generate "new style" Enums instead
        for enum in eolian.typedecl_enums_get_by_file(eo_fname):
            c_name = enum.full_name.replace('.', '_')
            VRB('gen enum:', enum.full_name)
            f.write('\n# enum: {0}\n'.format(enum.full_name))
            headerf.write('\ntypedef enum {\n')
            for field in enum.enum_fields:
                headerf.write('    {0},\n'.format(field.c_name))
                f.write('{0} = lib.{0}\n'.format(field.c_name))
            headerf.write('    ...\n')
            headerf.write('}} {0};\n'.format(c_name))

    def emit_typedefs(self, eo_fname, f, headerf, initf):
        for d in eolian.declarations_get_by_file(eo_fname):
            t = d.type
            c_name = d.name.replace('.', '_')

            if t == eolian.EOLIAN_DECL_CLASS:
                VRB('gen class typedef:', d.name)
                headerf.write(CLASS_TYPEDEF.format(d.name, c_name, d.class_.c_get_function_name))

            elif t == eolian.EOLIAN_DECL_ENUM:
                # headerf.write('typedef enum _{0} {0};\n'.format(c_name))
                pass

            else:
                WRN('Unknow typedef type: ', t)

    def emit_class(self, eo_fname, f, headerf, initf):
        klass = eolian.Class(eo_fname)
        VRB('gen class:', klass.full_name)

        ### Class definition (change "Efl.Gfx.Base" to "efl.gfx.Base")
        # TODO: fix to lowercase ALL the names (except the last)
        inherits = ', '.join( [ uncapitalize(c) for c in klass.inherits ]) or 'object'
        f.write(CLASS_DEF.format(klass.full_name, klass.name, inherits))

        ### Events
        py_code, h_code = '', ''
        for ev in klass.events:
            VRB('gen   event:', ev.c_name)
            py_code += "        '{0.name}': lib.{0.c_name},\n".format(ev)
            h_code += 'extern static Eo_Event_Description *const {};\n'.format(ev.c_name)

        if py_code != '':
            f.write('    __events = {{\n{}    }}\n'.format(py_code))
            headerf.write('\n// {} events\n{}\n'.format(klass.full_name, h_code))

        ### Constructor
        if klass.type == eolian.EOLIAN_CLASS_REGULAR:
            self.emit_constructor(klass, f, headerf)

        ### Methods
        f.write('\n    # methods\n')
        headerf.write('// {} methods\n'.format(klass.full_name))
        for func in sorted(klass.methods, key=lambda f: f.name):

            if func.is_c_only:
                print('C only - ' * 7) # TODO REMOVE ME
                continue

            if func.full_c_name_get(eolian.EOLIAN_METHOD) in MANUAL_EXCLUDES:
                VRB('SKIPPED', func.full_c_name_get(eolian.EOLIAN_METHOD))
                continue

            if func.is_constructor:
                continue

            self.emit_function(klass, func, eolian.EOLIAN_METHOD, f, headerf)

            # header file
            # headerf.write('{};\n'.format(func.full_c_define_get(eolian.EOLIAN_METHOD)))

        ### Properties
        f.write('\n    # properties\n')
        headerf.write('\n// {} properties\n'.format(klass.full_name))
        for func in sorted(klass.properties, key=lambda f: f.name):

            if func.is_c_only:
                print('C only - ' * 7) # TODO REMOVE ME
                continue

            if func.full_c_name_get(eolian.EOLIAN_PROPERTY) in MANUAL_EXCLUDES:
                VRB('SKIPPED', func.full_c_name_get(eolian.EOLIAN_PROPERTY))
                continue


            ftype = func.type
            can_read = ftype in (eolian.EOLIAN_PROPERTY, eolian.EOLIAN_PROP_GET)
            can_write = ftype in (eolian.EOLIAN_PROPERTY, eolian.EOLIAN_PROP_SET)
            if can_read:
                self.emit_getter(klass, func, f, headerf)
            if can_write:
                self.emit_setter(klass, func, f, headerf)
                # self.emit_function(klass, func, eolian.EOLIAN_PROP_SET, f, headerf)

            f.write('\n    {0} = property({1}, {2})\n'.format(
                     func.name,
                     func.name + '_get' if can_read else 'None',
                     func.name + '_set' if can_write else 'None'))

            # header file
            # headerf.write('{};\n'.format(func.full_c_define_get(eolian.EOLIAN_PROP_GET)))
            
            
    def emit_constructor(self, klass, f, headerf):
        std = True
        ctors_py_code = ''
        for ctor in klass.constructors:
            std = False

            func = ctor.function
            ctors_py_code += '        lib.{}(...)\n'.format(func.full_c_name_get(eolian.EOLIAN_METHOD))

        # print(klass.ctor_enable)

        # standard
        if std:
            VRB('generating   standard constructor for class:', klass.full_name)
            f.write(CLASS_CTOR_DEFAULT.format(klass.c_get_function_name))

        # custom constructor,  ...manually written for the moment
        elif klass.full_name in MANUAL_CONSTRUCTORS:
            f.write(MANUAL_CONSTRUCTORS[klass.full_name])
        else:
            ERR('cannot find manual constructor for class', klass.full_name)

    def emit_function(self, klass, func, ftype, f, headerf):
        # header file
        headerf.write('{};\n'.format(func.full_c_define_get(ftype)))

        # function name (for setter and getters)
        if ftype == eolian.EOLIAN_PROP_GET:
            name = func.name + '_get'
            name2 = 'prop get'
        elif ftype == eolian.EOLIAN_PROP_SET:
            name = func.name + '_set'
            name2 = 'prop set'
        else:
            name = func.name
            name2 = 'method'

        VRB('gen   {}: {}.{}()'.format(name2, klass.full_name, name))

        # split in and out params in 2 lists
        in_pars = ['self']
        out_pars = []
        if ftype == eolian.EOLIAN_PROP_GET:
            for v in func.getter_values:
                out_pars.append(_type_conv(v.type, v.name, False))
        elif ftype == eolian.EOLIAN_PROP_SET:
            for v in func.setter_values:
                in_pars.append(v.name)
        else:
            for p in func.parameters:
                if p.direction == eolian.EOLIAN_IN_PARAM:
                    in_pars.append(p.name)
                elif p.direction == eolian.EOLIAN_OUT_PARAM:
                    out_pars.append(_type_conv(p.type, p.name, False))

        # function definition (+ docs)
        in_pars = ', '.join(in_pars)
        docs = 'TODO ' + func.full_c_define_get(ftype) # TODO
        f.write(CLASS_METHOD.format(name, in_pars, docs))

        # c function call (+ allocs)
        self.emit_c_function_call(func, ftype, f)

        # return a tuple with all the out args
        if len(out_pars) > 1:
            out_pars = ', '.join(out_pars)
            f.write('        return tuple({})\n'.format(out_pars))
            return

        # or return the single out arg
        if len(out_pars) == 1:
            f.write('        return {}\n'.format(out_pars[0]))
            return

        # or return the value returned from the c call (converted)
        rtype = func.return_type_get(ftype)
        if rtype is not None:
            f.write('        return {}\n'.format(_type_conv(rtype, 'ret', False)))

    def emit_getter(self, klass, func, f, headerf):
        VRB('gen   prop get: {}.{}_get()'.format(klass.full_name, func.name))
        vals = list(func.getter_values)
        
        ### header file
        headerf.write('{};\n'.format(func.full_c_define_get(eolian.EOLIAN_PROP_GET)))

        ### function definition (+ docs)
        docs = 'TODO ' + func.full_c_define_get(eolian.EOLIAN_PROP_GET) # TODO
        f.write(CLASS_GETTER.format(func.name, docs))

        ### c function call (+ allocs)
        params = ['self._obj']
        for p in vals:
            params.append(p.name)
            if len(vals) > 1:
                f.write('        {0} = ffi.new("{1}[1]")\n'.format(p.name, p.type.c_type))

        # c function call
        rtype = func.return_type_get(eolian.EOLIAN_PROP_GET)
        ret = '_ret_ = ' if rtype is not None else ''
        f.write('        {}lib.{}({})\n'.format(ret,
                    func.full_c_name_get(eolian.EOLIAN_PROP_GET),
                    ', '.join(params)))

        # return a tuple of all the values
        if len(vals) > 1:
            vals = ', '.join([ _type_conv(v.type, v.name, False) for v in vals ])
            # out_pars = ', '.join(out_pars)
            f.write('        return tuple({})\n'.format(vals))

        # or return the single value
        elif len(vals) == 1:
            f.write('        return {}\n'.format(_type_conv(vals[0].type, vals[0].name, False)))

        # or return the value returned by the c function
        elif rtype:
            f.write('        return {}\n'.format(_type_conv(rtype, '_ret_', False)))

    def emit_setter(self, klass, func, f, headerf):

        if func.name.startswith('smart_clipped_clipper'):
            print("**********************  SET")
            print(list(func.parameters))
            print(list(func.setter_values))
            print(func.return_type_get(eolian.EOLIAN_PROP_SET))
            
        VRB('gen   prop get: {}.{}_get()'.format(klass.full_name, func.name))
        vals = list(func.setter_values)

        ### header file
        headerf.write('{};\n'.format(func.full_c_define_get(eolian.EOLIAN_PROP_SET)))

        ### function definition (+ docs)
        docs = 'TODO ' + func.full_c_define_get(eolian.EOLIAN_PROP_SET) # TODO
        if len(vals) > 1:
            val_name = '_val_'
        elif len(vals) == 1:
            val_name = vals[0].name
        else:
            raise RuntimeError('ASDASDASDASDASDASDASDASDASDASDASDASDASDASDASD')
        f.write(CLASS_SETTER.format(func.name, val_name,docs))

        ### unpack the tuple _val_
        if len(vals) > 1:
            vs = ', '.join([ v.name for v in vals])
            f.write('        {} = _val_\n'.format(vs))
            
        ### c function call
        params = ['self._obj']
        for p in func.setter_values:
            params.append(_type_conv(p.type, p.name, True))

        # c function call
        rtype = func.return_type_get(eolian.EOLIAN_PROP_SET)
        ret = '_ret_ = ' if rtype is not None else ''
        f.write('        {}lib.{}({})\n'.format(ret,
                    func.full_c_name_get(eolian.EOLIAN_PROP_SET),
                    ', '.join(params)))

        # or return the value returned by the c function
        if rtype:
            f.write('        return {}\n'.format(_type_conv(rtype, '_ret_', False)))

    def emit_c_function_call(self, func, ftype, f, indent=8):
        indent = ' ' * indent
        params = ['self._obj']
        allocs = []

        ###################################################################
        ###################################################################
        #  SIAMO QUI
        # sistemare i parametri per i getter e setter
        ###################################################################
        ###################################################################
        if    ftype == eolian.EOLIAN_METHOD:   pars = func.parameters
        elif  ftype == eolian.EOLIAN_PROP_GET: pars = func.getter_values
        elif  ftype == eolian.EOLIAN_PROP_SET: pars = func.setter_values
        else: raise RuntimeError('Unsupported function type: %d' % ftype)

        for p in pars:
            direction = p.direction
            ptype = p.type
            if direction == eolian.EOLIAN_IN_PARAM:
                params.append(_type_conv(ptype, p.name, True))
            elif direction == eolian.EOLIAN_OUT_PARAM:
                allocs.append('{0} = ffi.new("{1}")'.format(p.name, ptype.c_type))
                params.append('&' + p.name)
            else:
                WRN('Unsupported INOUT param direction')

        for a in allocs:
            f.write(indent + a + '\n')

        params = ', '.join(params)
        ret = ''
        if func.return_type_get(ftype):# or ftype == eolian.EOLIAN_PROP_GET:
            ret = 'ret = '
            
        f.write(indent + '{}lib.{}({})\n'.format(ret, func.full_c_name_get(ftype), params))

def _type_conv(ty, expr, isin):

    # c->py or py->c
    conv_dict = CONVERSIONS_FROM_PY if isin else CONVERSIONS_FROM_C
    
    # use the base type (ex: Evas.Coord -> int)
    ty = ty.aliased_base

    # an eo object instance ?
    if ty.type == eolian.EOLIAN_TYPE_POINTER:
        if ty.base_type.type == eolian.EOLIAN_TYPE_CLASS:
            return conv_dict['eo_objects'].format(expr)

    # an enum ?
    try:
        if ty.typedecl.type == eolian.EOLIAN_TYPEDECL_ENUM:
            return conv_dict['enums'].format(expr)
    except AttributeError:
        pass

    # or just use the mapping dict
    tname = ty.name2
    try:
        fmt = conv_dict[tname]
    except:
        raise RuntimeError('Unsupported conversion for type: %s' % ty)
        # ERR('Unsupported conversion for type:\n', ty)
        return 'XXXXXX(%s)' % tname #######################################################
    else:
        return fmt.format(expr)

def _type_conv_py2c(ty, expr, isin):

    # use the base type (ex: Evas.Coord -> int)
    ty = ty.aliased_base

    # an eo object instance ?
    if ty.type == eolian.EOLIAN_TYPE_POINTER:
        if ty.base_type.type == eolian.EOLIAN_TYPE_CLASS:
            return CONVERSIONS_FROM_PY['eo_objects'].format(expr)

    # an enum ?
    try:
        if ty.typedecl.type == eolian.EOLIAN_TYPEDECL_ENUM:
            return CONVERSIONS_FROM_PY['enums'].format(expr)
    except AttributeError:
        pass

    # or just use the mapping dict
    tname = ty.name2
    try:
        fmt = CONVERSIONS_FROM_PY[tname]
    except:
        # raise RuntimeError('Unsupported conversion from py to c for type: %s' % ty)
        ERR('Unsupported conversion from py to c for type:\n', ty)
        return 'XXXXXX(%s)' % tname #######################################################
    else:
        return fmt.format(expr)
    
# how to convert a python type to a c type (that can be passed to c functions)
CONVERSIONS_FROM_PY = {
    # default types (as reported by type.name2)
    'int':    'int({0})',    #just to typecheck
    'ullong': 'int({0})',
    'double': 'float({0})',
    'bool': 'bool({0})',  #just to typecheck
    'const char *': '_to_bytes({0})',
    # special "types"
    'eo_objects': '{0}._obj',
    'enums': '{0}',
}

# how to convert a C type to a python object
CONVERSIONS_FROM_C = {
    # default types (as reported by type.name2)
    'int': 'int({0})',
    'uint': 'int({0})',
    'double': 'float({0})',
    'bool': 'bool({0})',
    'const char *': '_to_unicode(ffi, {0})',

    # special "types"
    'eo_objects': '_object_from_instance({0})', # TODO rename and implement _object_from_instance
    'enums': '{0}',
    
    # 'char': '{0}.decode("utf-8")',
    # "Elm_Object_Item": 'object_item_to_python({0})',
    # "Evas_Object": 'object_from_instance({0})',
    # "Eo": 'object_from_instance({0})',
}


if __name__ == '__main__':

    print('Usage: "python setup.py generate" from the package root dir.')


