#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

import unittest


loader = unittest.TestLoader()
suite = loader.discover('.')
runner = unittest.TextTestRunner(verbosity=2, buffer=True)
result = runner.run(suite)
