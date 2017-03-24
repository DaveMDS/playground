#! /usr/bin/env python3
# encoding: utf-8

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

        self.template_filename = filename
        data = {}  # TODO fill with fixed infos (versions, date, time, etc...)

        pyratemp.Template.__init__(self, filename=filename, encoding=encoding,
                                   data=data, escape=escape,
                                   loader_class=loader_class,
                                   parser_class=parser_class,
                                   renderer_class=renderer_class,
                                   eval_class=eval_class)

    def render(self, filename=None, cls=None, **kargs):

        ctx = {}
        if cls is not None:
            ctx['cls'] = eolian.Class(class_name=cls)

        # render with the augmented context
        output = self(**ctx)

        if filename is not None:
            INF('generating "%s" from template "%s"' % (
                filename, self.template_filename))
            # write to file
            # TODO check dest dir exists, and create if necessary
            with open(filename, "w") as f:
                f.write(output)
        else:
            # or print to stdout
            print(output)
