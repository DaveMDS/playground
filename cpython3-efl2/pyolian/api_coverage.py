#!/usr/bin/env python3
# encoding: utf-8

import sys
import re

"""

Check eolian API coverage

just for development purpose

...adjust the following path as your needs

"""
EOLIAN_HEADER = '/home/dave/e/core/efl/src/lib/eolian/Eolian.h'

flags = re.S | re.M
DEFINED_RE = re.compile('^EAPI[\w\n *]*(eolian_\w*)\([\w *,]*\);', flags)
USED_RE = re.compile('lib\.(eolian_[\w]*)\(', flags)


if __name__ == '__main__':

    # Extract all EAPI functions from the header
    defined_funcs = []
    with open(EOLIAN_HEADER, 'r') as fh:
        header = fh.read()
        for match in re.finditer(DEFINED_RE, header):
            func_name = match.group(1)
            defined_funcs.append(func_name)
    defined_funcs = set(defined_funcs)

    # Extract all called functions in eolian.py "lib.*("
    used_funcs = []
    with open('eolian.py', 'r') as fh:
        source = fh.read()
        for match in re.finditer(USED_RE, source):
            func_name = match.group(1)
            used_funcs.append(func_name)
    used_funcs = set(used_funcs)

    # Show general info
    num_def = len(defined_funcs)
    num_usd = len(used_funcs)
    print('Found %d functions defined in Eolian.h (%s)' % (num_def, EOLIAN_HEADER))
    print('Found %d functions used in eolian.py (hopefully not commented out)' % num_usd)
    print('Total API coverage %.1f%%' % (num_usd / num_def * 100))
    print('')

    # Show usage
    if len(sys.argv) < 2:
        print('Usage:')
        print('  --list      To list all missing functions')
        print('  --list-all  To list all functions found in Eolian.h')
        print('')
        exit(0)

    # List all missing functions
    if '--list' in sys.argv:
        print('Missing functions in eolian.py:')
        print('===============================')
        for func_name in sorted(defined_funcs - used_funcs):
            print(func_name)
        print('===============================')

    # List all functions find in Eolian.h
    if '--list-all' in sys.argv:
        print('All the functions in Eolian.h:')
        print('===============================')
        for i, func_name in enumerate(sorted(defined_funcs), 1):
            print('{:03d}. {}'.format(i, func_name))
        print('===============================')
