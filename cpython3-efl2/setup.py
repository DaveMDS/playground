#! /usr/bin/env python3
# encoding: utf-8

import os
import sys
import shutil
import platform
import subprocess
from distutils.core import setup, Command, Extension
from distutils.version import StrictVersion, LooseVersion
from distutils.command.build import build
# from efl2 import __version__, __version_info__ as vers


script_path = os.path.dirname(os.path.abspath(__file__))

# python-efl version (change in efl/__init__.py)
# RELEASE = __version__
RELEASE = "2.0.0-test1"
# VERSION = "%d.%d" % (vers[0], vers[1] if vers[2] < 99 else vers[1] + 1)

# dependencies
# EFL_MIN_VER = RELEASE
EFL_MIN_VER = "1.19.0"


# === Check for python ===
sys.stdout.write("Checking for Python: ")
py_ver = sys.version_info
py_ver = "%s.%s.%s" % (py_ver[0], py_ver[1], py_ver[2])
if sys.hexversion < 0x030400f0:
    raise SystemExit("too old. Found: %s  Need at least 3.4.0" % py_ver)
else:
    sys.stdout.write("OK, found %s\n" % py_ver)


# === pkg-config ===
def pkg_config(name, require, min_vers=None):
    try:
        sys.stdout.write("Checking for " + name + ": ")

        call = subprocess.Popen(["pkg-config", "--modversion", require],
                                stdout=subprocess.PIPE)
        out, err = call.communicate()
        if call.returncode != 0:
            raise SystemExit("Did not find " + name + " with 'pkg-config'.")

        ver = out.decode("utf-8").strip()
        if min_vers is not None:
            assert (LooseVersion(ver) >= LooseVersion(min_vers)) is True

        call = subprocess.Popen(["pkg-config", "--cflags", require],
                                stdout=subprocess.PIPE)
        out, err = call.communicate()
        cflags = out.decode("utf-8").split()

        call = subprocess.Popen(["pkg-config", "--libs", require],
                                stdout=subprocess.PIPE)
        out, err = call.communicate()
        libs = out.decode("utf-8").split()

        sys.stdout.write("OK, found " + ver + "\n")

        cflags = list(set(cflags))

        return (cflags, libs)
    except (OSError, subprocess.CalledProcessError):
        raise SystemExit("Did not find " + name + " with 'pkg-config'.")
    except (AssertionError):
        raise SystemExit("%s version mismatch. Found: %s  Needed %s" % (
                         name, ver, min_vers))

# === Run all tests (setup.py test) ===
class Test(Command):
    description = 'Run all the available unit tests using efl in build/'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import unittest

        sys.path.insert(0, "build/lib.%s-%s-%d.%d" % (
                            platform.system().lower(), platform.machine(),
                            sys.version_info[0], sys.version_info[1]))
        if "efl2" in sys.modules:
            del sys.modules["efl2"]

        loader = unittest.TestLoader()
        suite = loader.discover('./tests')
        runner = unittest.TextTestRunner(verbosity=1, buffer=True)
        result = runner.run(suite)


# === Aggressive clean command (setup.py clean) ===
class CleanALL(Command):
    description = 'Aggressive clean command, try to remove EVERYTHING'
    user_options = []

    MAGIC = 'PYOLIAN AUTOGENERATED FILE (never change this line)'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        # clean *.pyc and __pycache__ in the while tree
        for root, dirs, files in os.walk(script_path, topdown=False):
            for f in files:
                full_path = os.path.join(root, f)
                if f.endswith('.pyc') or self.is_generated(full_path):
                    self.remove_f(full_path)
            for d in dirs:
                full_path = os.path.join(root, d)
                if d == '__pycache__':
                    self.remove_t(full_path)
                # if not os.listdir(full_path): # empty dir ?
                    # self.remove_d(full_path)

        # clean root folder
        self.remove_t(os.path.join(script_path, 'build'))
        self.remove_t(os.path.join(script_path, 'dist'))

    def is_generated(self, full_path):
        if not full_path.endswith(('.h', '.c')):
            return False
        with open(full_path, 'r') as f:
            first_line = f.readline()
            if self.MAGIC in first_line:
                return True
        return False

    def remove_f(self, full_path):
        print('removing file: %s' % os.path.relpath(full_path))
        os.remove(full_path)

    def remove_d(self, full_path):
        print("removing empty dir: %s/" % os.path.relpath(full_path))
        os.rmdir(full_path)

    def remove_t(self, full_path):
        if os.path.isdir(full_path):
            print("pruning dir: %s/" % os.path.relpath(full_path))
            shutil.rmtree(full_path)


# === pyolian generator (setup.py generate) ===
class Generate(Command):
    description = 'Pyolian generator'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print('generating bindings source code using pyolian')
        from pyolian.generator import Template

        cls_c_tmpl = Template('templates/class.template.c')
        cls_h_tmpl = Template('templates/class.template.h')
        
        cls_c_tmpl.render('efl2/loop/efl.loop.timer.c', cls='Efl.Loop.Timer')
        cls_h_tmpl.render('efl2/loop/efl.loop.timer.h', cls='Efl.Loop.Timer')

        cls_c_tmpl.render('efl2/loop/efl.loop.fd.c', cls='Efl.Loop.Fd')
        cls_h_tmpl.render('efl2/loop/efl.loop.fd.h', cls='Efl.Loop.Fd')


# === augmented build command ===
class Build(build):
    def run(self):
        self.run_command("generate")
        build.run(self)


cflags, libs = pkg_config('EFL', 'eina elementary', EFL_MIN_VER)

ext_modules = []
packages = ["efl2", "efl2.loop"]

def efl_module(name, sources):
    mod = Extension(name,
            define_macros = [('EFL_BETA_API_SUPPORT', 1),
                             ('EFL_EO_API_SUPPORT', 1),
                             ('EFL_NOLEGACY_API_SUPPORT', 1)],
            # include_dirs = ['/usr/local/include'],
            # libraries = ['tcl83'],
            # library_dirs = ['/usr/local/lib'],
            # extra_compile_args = cflags + common_cflags,
            # extra_link_args = libs + eina_libs
            extra_compile_args = cflags,
            extra_link_args = libs,
            sources = sources)
    ext_modules.append(mod)


# efl namespace module
efl_module('efl2._efl', [
    'efl2/eo_utils.c',
    'efl2/_efl.module.c',
    'efl2/efl.object.c',
    'efl2/efl.loop.c',
    'efl2/efl.loop_user.c',
])

# efl.loop namespace module
efl_module('efl2.loop._loop', [
    'efl2/loop/_loop.module.c',
    'efl2/loop/efl.loop.timer.c',
    'efl2/loop/efl.loop.fd.c',
])


setup(
    name="python-efl2",
    version = '0.0.0',
    description = 'This is a demo package',
    author = 'davemds',
    author_email = 'dave@gurumeditation.it',
    url = 'https://www.enlightenment.org',
    long_description = ''' This is really just a demo package.''',
    packages = packages,
    # ext_package = "efl2",
    ext_modules = ext_modules,
    cmdclass = {
        'clean': CleanALL,
        'generate': Generate,
        'build': Build,
        'test': Test, 'tests': Test,
    },
)
