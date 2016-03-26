#!/usr/bin/env python
# encoding: utf-8

import platform

from efl2 import eo
from efl2 import evas
from efl2 import ecore
from efl2.ecore import Timer
from efl2 import elementary as elm, __version__



# def mycb(*args, **kargs):
    # print(args, kargs)
    # print(" \o/ " * 60)
    # ecore.main_loop_quit()
    # return ecore.ECORE_CALLBACK_CANCEL
#


lb = None

def mycb2():
    global lb
    print("t")
    if lb:
        print("TIMER")
        lb.delete()
        lb = None
    return ecore.ECORE_CALLBACK_RENEW


# t = Timer(5.0, mycb, 567, asd='AsD')
t2 = Timer(3.0, mycb2)

# ecore.main_loop_begin()

# ml = ecore.Mainloop()

def mycb3(self, *args):
    print("CB!!!!!!!!!!!!" + str(args))

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
    global lb
    lb = elm.Label(win)
    lb.text = win.title
    box.pack_end(lb)
    lb.visible = True
    lb.event_callback_add(eo.EO_BASE_EVENT_DEL, mycb3)
    lb.event_callback_add2('del', mycb3)

    # button
    bt = elm.Button(win)
    bt.text = lb.text
    box.pack_end(bt)
    bt.visible = True
    # bt.event_callback_priority_add(0, eo.EO_BASE_EVENT_DEL, mycb3)
    bt.event_callback_add3(evas.EVAS_CLICKABLE_INTERFACE_EVENT_CLICKED, mycb3)
    # bt.delete()
    

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
