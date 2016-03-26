#!/usr/bin/env python

import os
import sys

from setuptools import setup, find_packages
from efl import __version__, __version_info__

# os.chdir(os.path.dirname(sys.argv[0]) or ".")

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

    install_requires = ["cffi>=1.0.0"],
    setup_requires = ["cffi>=1.0.0"],

    zip_safe = False, # zipped the egg is slower to start?
    packages = find_packages(),
    cffi_modules = [
        "./efl2/cffi/build_efl.py:ffi",
    ],
)

