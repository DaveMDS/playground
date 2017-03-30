#! /usr/bin/env python3
# encoding: utf-8

import os
import datetime

from . import eolian
from . import pyratemp


# logging utils
be_verbose = True
def ERR(*args): print(*(('PYOLIANGEN    ERROR:', ) + args))
def WRN(*args): print(*(('PYOLIANGEN    WARNING:', ) + args))
def INF(*args): print(*(('PYOLIANGEN   ', ) + args))


# load the whole eolian db
INF('system directory scan')
if not eolian.system_directory_scan():
    raise(RuntimeError('Eolian, failed to scan system directories'))

INF('parsing all EO files')
if not eolian.all_eo_files_parse():
    raise(RuntimeError('Eolian, failed to parse all EO files'))

INF('parsing all EOT files')
if not eolian.all_eot_files_parse():
    raise(RuntimeError('Eolian, failed to parse all EOT files'))

INF('validate database')
if not eolian.database_validate():
    raise(RuntimeError('Eolian, database validation failed'))


class Template(pyratemp.Template):
    """
        TODO: doc !!!
    """
    def __init__(self, filename, encoding='utf-8', data=None, escape=None,
                       loader_class=pyratemp.LoaderFile,
                       parser_class=pyratemp.Parser,
                       renderer_class=pyratemp.Renderer,
                       eval_class=pyratemp.EvalPseudoSandbox):

        # Build the global context for the template
        global_ctx = {}
        # user provided context (low pri)
        if data:
            global_ctx.update(data)
        # standard names (not overwritables)
        global_ctx.update({
            'date': datetime.datetime.now(),
            'eolian_version': eolian.__version__,
            'eolian_version_info': eolian.__version_info__,
            'template_file': os.path.basename(filename),
        })
        

        # Call the parent __init__ func
        self.template_filename = filename
        pyratemp.Template.__init__(self, filename=filename, encoding=encoding,
                                   data=global_ctx, escape=escape,
                                   loader_class=loader_class,
                                   parser_class=parser_class,
                                   renderer_class=renderer_class,
                                   eval_class=eval_class)

    def render(self, filename=None, cls=None, ns=None, **kargs):

        # Build the context for the template
        ctx = {}
        if kargs:
            ctx.update(data)
        if cls:
            ctx['cls'] = eolian.Class(cls)
        if ns:
            ctx['namespace'] = ns
            ctx['namespaces'] = ns.split('.')
            ctx['classes'] = [ c for c in eolian.all_classes_get()
                                if c.full_name.startswith(ns + '.') ]

        # render with the augmented context
        output = self(**ctx)

        if filename is not None:
            INF('generating "%s" from template "%s"' % (
                filename, self.template_filename))
            # create directory tree if needed
            folder = os.path.dirname(filename)
            if not os.path.isdir(folder):
                os.makedirs(folder)
            # write to file
            with open(filename, "w") as f:
                f.write(output)
        else:
            # or print to stdout
            print(output)
