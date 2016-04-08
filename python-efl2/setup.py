#!/usr/bin/env python

from __future__ import absolute_import, print_function, division

import os
import sys

from setuptools import setup, find_packages, Command
from setuptools.command.build_py import build_py
from efl2 import __version__, __version_info__


PATH = os.path.dirname(os.path.realpath(__file__))


class Generate(Command):
    """ run the eolian generator """
    description = "generate the source code from eo descriptions"
    user_options = [('svg', 'v', 'Super Verbose Generation')]

    def initialize_options(self):
        self.svg = False

    def finalize_options(self):
        pass

    def run(self):
        print('-'*60)
        print('generating bindings source code using pyolian')
        from pyolian.generator import Generator
        
        if not Generator(main_py_path=os.path.join(PATH, 'efl2/'),
                         headers_path=os.path.join(PATH, 'efl2/cffi/'),
                         verbose=self.svg).generate_all():
            print('\nSomething goes wrong, generation aborted.\n')
            exit(1)

        print('-'*60)


class BuildPy(build_py):
    def run(self):
        self.run_command("generate")
        build_py.run(self)


setup(
    name = 'python-efl2',
    version = __version__,
    fullname = 'Python bindings for Enlightenment Foundation Libraries',
    description = 'Python bindings for Enlightenment Foundation Libraries',
    long_description = open('README.rst', 'rt').read(),
    author = 'Davide Andreoli, Kai Huuhko, and others',
    author_email = 'dave@gurumeditation.it, kai.huuhko@gmail.com',
    contact = 'Enlightenment developer mailing list',
    contact_email = 'enlightenment-devel@lists.sourceforge.net',
    url = 'http://www.enlightenment.org',
    license = 'GNU Lesser General Public License (LGPL)',
    keywords = 'efl wrapper binding enlightenment eo evas ecore edje emotion elementary ethumb',
    classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: X11 Applications',
        'Environment :: Console :: Framebuffer',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
        'Operating System :: POSIX',
        'Programming Language :: C',
        'Programming Language :: cffi',  # TODO is this right ??
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: Software Development :: Widget Sets',
    ],

    install_requires = ["cffi>=1.4.0"],
    setup_requires = ["cffi>=1.4.0"],

    packages = ['efl2'],
    zip_safe = False, # zipped the egg is slower to start?
    cmdclass = {
        'generate': Generate,
        'build_py': BuildPy,
    },
    cffi_modules = [
        "./efl2/cffi/build_efl.py:ffi",
    ],

)


# --disable-cxx-bindings --disable-doc
