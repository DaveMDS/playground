#!/usr/bin/env python3

import unittest


loader = unittest.TestLoader()
suite = loader.discover('.')
runner = unittest.TextTestRunner(verbosity=1, buffer=True)
result = runner.run(suite)
