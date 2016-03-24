#!/usr/bin/env python
# encoding: utf-8

import platform

from efl2 import ecore
from efl2.ecore import Timer
from efl2 import elementary as elm, __version__



# def mycb(*args, **kargs):
    # print(args, kargs)
    # print(" \o/ " * 60)
    # ecore.main_loop_quit()
    # return ecore.ECORE_CALLBACK_CANCEL
# 
def mycb2():
    print("t")
    return ecore.ECORE_CALLBACK_RENEW


# t = Timer(5.0, mycb, 567, asd='AsD')
t2 = Timer(3.0, mycb2)

# ecore.main_loop_begin()

# ml = ecore.Mainloop()


if __name__ == '__main__':
    title = 'Python EFL version %s (on python: %s)' % (
             __version__, platform.python_version())

    # win = elm.Win('pyefl-test', elm.ELM_WIN_BASIC)
    win = elm.Win_Standard('pyefl-test')
    win.title = "asdasd àèìòù ね の は "
    print("** " + win.title)
    print("** " + str(type(win.title)))

    # box
    box = elm.Box(win)
    win.resize_object_add(box)
    box.visible = True

    # label
    lb = elm.Label(win)
    lb.text = win.title
    box.pack_end(lb)
    lb.visible = True

    # button
    bt = elm.Button(win)
    bt.text = 'press me'
    box.pack_end(bt)
    bt.visible = True

    #
    win.visible = True
    elm.run()

    """ ORIGINAL TO MIMIC:
    win = StandardWindow("test", title)
    win.callback_delete_request_add(destroy, "test1", "test2",
                                    str3="test3", str4="test4")
    win.resize(480, 480)
    win.show()
    elementary.run()
    """
