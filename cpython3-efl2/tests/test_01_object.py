#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

import unittest

import efl2 as efl



class TestObject(unittest.TestCase):

    def setUp(self):
        self.o = efl.Object()

    def tearDown(self):
        self.o.delete()

    def testType(self):
        self.assertEqual(type(self.o), efl.Object)


if __name__ == '__main__':
    unittest.main(verbosity=2)
