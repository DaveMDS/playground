#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8

import unittest

import efl2 as efl
import efl2.loop



class TestObject(unittest.TestCase):

    # def setUp(self):
        # print("setUp")
        # self.o = efl.Loop()

    # def tearDown(self):
        # print("tearDown")
        # self.o.delete()

    # Test Object type
    def test_type(self):
        o = efl.Loop()
        self.assertIsInstance(o, efl.Loop)
        self.assertIsInstance(o, efl.Object)
        self.assertEqual(o.__class__.__name__, 'Loop')

        o.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del o

    # Test parent
    def test_parent(self):
        loop = efl.Loop()
        timer = efl.loop.Timer(loop, 1.0)

        self.assertIsInstance(loop, efl.Loop)
        self.assertIsInstance(timer, efl.loop.Timer)
        self.assertIsInstance(timer, efl.Object)

        self.assertEqual(loop.parent, None)
        self.assertEqual(timer.parent, loop)

        # TODO test parent_set

        loop.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del loop
        timer.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del timer
        
    # Test callbacks
    def test_callback_call(self):
        expected_calls = 2

        def _del_cb_no_info_no_kwds(obj, event):
            nonlocal expected_calls

            self.assertIsInstance(obj, efl.Loop)
            self.assertEqual(event, 'del')

            expected_calls -= 1

        def _del_cb_no_info_with_kwds(obj, event, uno, due):
            nonlocal expected_calls

            self.assertIsInstance(obj, efl.Loop)
            self.assertEqual(event, 'del')
            self.assertIsInstance(uno, str)
            self.assertEqual(uno, 'test_uno')
            self.assertIsInstance(due, int)
            self.assertEqual(due, 2)

            expected_calls -= 1

        # TODO test callback with event_info

        o = efl.Loop()
        o.event_callback_add('del', _del_cb_no_info_no_kwds)
        o.event_callback_add('del', _del_cb_no_info_with_kwds,
                             uno="test_uno", due=2)

        o.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del o

        self.assertEqual(expected_calls, 0)
        del expected_calls

    # Test interfaces are not instantiable
    def test_iface_instance(self):
        self.assertRaises(TypeError, efl.Animator)
        self.assertRaises(TypeError, efl.Config)
        self.assertRaises(TypeError, efl.Part)

if __name__ == '__main__':
    unittest.main(verbosity=2)
