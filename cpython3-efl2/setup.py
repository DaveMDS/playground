#! /usr/bin/env python3
# encoding: utf-8

import sys
import subprocess
from distutils.core import setup, Extension
from distutils.version import StrictVersion, LooseVersion
# from efl2 import __version__, __version_info__ as vers

# python-efl version (change in efl/__init__.py)
# RELEASE = __version__
RELEASE = "2.0.0-test1"
# VERSION = "%d.%d" % (vers[0], vers[1] if vers[2] < 99 else vers[1] + 1)

# dependencies
# EFL_MIN_VER = RELEASE
EFL_MIN_VER = "1.19.0"


# === Python ===
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


# if set(("build", "build_ext", "install", "bdist", "sdist")) & set(sys.argv):
    # sys.stdout.write("Python-EFL: %s\n" % RELEASE)




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


# namespace: efl
efl_module('efl2._object', ['efl2/efl.object.c'])
efl_module('efl2._loop', ['efl2/efl.loop.c'])
efl_module('efl2._loop_user', ['efl2/efl.loop_user.c'])
# namespace: efl.loop
efl_module('efl2.loop._timer', ['efl2/loop/efl.loop.timer.c'])


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
)
