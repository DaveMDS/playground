#!/usr/bin/env python
# encoding: utf-8

import platform

import efl2 as efl

from efl2 import eo
# from efl2 import evas
from efl2 import ecore
# from efl2.ecore import Timer
from efl2 import elementary as elm, __version__



# def mycb(*args, **kargs):
    # print(args, kargs)
    # print(" \o/ " * 60)
    # ecore.main_loop_quit()
    # return ecore.ECORE_CALLBACK_CANCEL
#


def my_timer_cb():
    global lb
    print("t")
    if lb:
        print("TIMER")
        lb.delete()
        lb = None
    return ecore.ECORE_CALLBACK_RENEW


# t = Timer(5.0, mycb, 567, asd='AsD')
t2 = efl.ecore.Timer(3.0, my_timer_cb)

# ecore.main_loop_begin()

# ml = ecore.Mainloop()

def mycb3(*args):
    print("CB!!!!!!!!!!!!" + str(args))
    return eo.EO_CALLBACK_STOP

def mycb4(*args):
    print("... and click !" + str(args))
    return eo.EO_CALLBACK_CONTINUE

if __name__ == '__main__':
    title = 'Python EFL version %s (on python: %s)' % (
             __version__, platform.python_version())

    # win = elm.Win('pyefl-test', elm.ELM_WIN_BASIC)
    win = elm.Win_Standard(None, title='pyefl-test')
    win.title = "asdasd àèìòù ね の は " * 3
    # print("** " + win.title)
    # print("** " + str(type(win.title)))

    # box
    box = elm.Box(win, visible=True)
    win.resize_object_add(box)

    # label
    lb = elm.Label(win, visible=True, text=win.title)
    lb.on('del', mycb3)
    box.pack_end(lb)

    # button
    bt = elm.Button(win, visible=True, text=lb.text)
    bt.on('clicked', mycb4)
    box.pack_end(bt)


    #
    win.visible = True
    elm.run()

    print("DONE")
    # win.delete()
    """ ORIGINAL TO MIMIC:
    win = StandardWindow("test", title)
    win.callback_delete_request_add(destroy, "test1", "test2",
                                    str3="test3", str4="test4")
    win.resize(480, 480)
    win.show()
    elementary.run()
    """
