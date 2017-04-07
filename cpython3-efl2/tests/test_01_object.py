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

    # Test interfaces are not instantiable
    def test_iface_instance(self):
        self.assertRaises(TypeError, efl.Animator)
        self.assertRaises(TypeError, efl.Config)
        self.assertRaises(TypeError, efl.Part)

    # Test Object type
    def test_type(self):
        obj = efl.Loop()
        self.assertIsInstance(obj, efl.Loop)
        self.assertIsInstance(obj, efl.Object)
        self.assertEqual(obj.__class__.__name__, 'Loop')

        obj.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del obj

    # Test parent
    def test_parent(self):
        loop1 = efl.Loop()
        loop2 = efl.Loop()
        obj = efl.loop.Fd(loop1)

        # test parent_get
        self.assertIsInstance(loop1, efl.Loop)
        self.assertIsInstance(loop2, efl.Loop)
        self.assertIsInstance(obj, efl.loop.Fd)
        self.assertIsInstance(obj, efl.Object)
        # ARGHHHH !!! this is wrong!...and I don't know how to fix...atm...
        self.assertIsInstance(obj, efl._Loop_User)

        self.assertIsNone(loop1.parent)
        self.assertIsNone(loop2.parent)
        self.assertEqual(obj.parent, loop1)

        # test parent_set
        obj.parent = loop2
        self.assertEqual(obj.parent, loop2)
        # TODO FIXME: the folooowing make the test suite crash on exit
        # obj.parent = loop1
        # self.assertEqual(obj.parent, loop1)
        obj.parent = None
        self.assertIsNone(obj.parent)

        # test wrong types
        with self.assertRaises(TypeError):
            obj.parent = 1
        with self.assertRaises(TypeError):
            obj.parent = 3.14
        with self.assertRaises(TypeError):
            obj.parent = 'this must fail'

        obj.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del obj
        loop1.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del loop1
        loop2.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del loop2


    # Test name
    def test_name(self):
        loop = efl.Loop()
        obj = efl.loop.Fd(loop)

        # test get/set
        self.assertIsNone(obj.name)
        obj.name = 'my funky name'
        self.assertEqual(obj.name, 'my funky name')
        obj.name = 'another one'
        self.assertEqual(obj.name, 'another one')
        obj.name = None
        self.assertIsNone(obj.name)

        # test wrong types
        with self.assertRaises(TypeError):
            obj.name = 1
        with self.assertRaises(TypeError):
            obj.name = 3.14
        with self.assertRaises(TypeError):
            obj.name = b'Really we dont want to accept bytes objects?'
        with self.assertRaises(TypeError):
            obj.name = lambda p: print("asd")

        # test name_find
        obj.name = 'find me!'
        self.assertEqual(loop.name_find('find me!'), obj)
        self.assertIsNone(loop.name_find('fail'))
        self.assertIsNone(loop.name_find(''))
        with self.assertRaises(TypeError):
            loop.name_find(None)
        with self.assertRaises(TypeError):
            loop.name_find(3.14)

        # test comment
        self.assertIsNone(obj.comment)
        obj.comment = 'my funky comment'
        self.assertEqual(obj.comment, 'my funky comment')
        obj.comment = None
        self.assertIsNone(obj.comment)
        with self.assertRaises(TypeError):
            obj.comment = 3.14

        obj.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del obj
        loop.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del loop

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

    def test_event_freeze(self):
        o = efl.Loop()

        self.assertEqual(o.event_freeze_count, 0)
        self.assertEqual(o.event_global_freeze_count, 0)

        o.event_freeze()
        o.event_freeze()
        o.event_global_freeze()
        o.event_global_freeze()
        o.event_global_freeze()
        self.assertEqual(o.event_freeze_count, 2)
        self.assertEqual(o.event_global_freeze_count, 3)

        o.event_thaw()
        o.event_thaw()
        o.event_global_thaw()
        o.event_global_thaw()
        o.event_global_thaw()
        self.assertEqual(o.event_freeze_count, 0)
        self.assertEqual(o.event_global_freeze_count, 0)

        o.delete()  # TODO this shoudn't be needed (intercept "del self.o")
        del o


if __name__ == '__main__':
    unittest.main(verbosity=2)
