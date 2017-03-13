#! /usr/bin/env python3
# encoding: utf-8


import efl2 as efl
import efl2.loop


# from efl2 import system
# from efl2 import Object

# print(system("ls -l"))


# print("\n---- Test: direct instance")
# o = efl.Object()
# print(o)
# o.parent_get()


# print("\n---- Test: subclass")
# class MyEoObject(efl.Object):
   # def __init__(self):
      # print("__INIT__")

# o = MyEoObject()
# print(o)


def idle_cb(*args):
   print("IDLE")

print("\n---- Test: Efl.Loop")
ml = efl.Loop()
# ml.event_callback_add("idle", idle_cb)
# ml.event_callback_add("idle,enter", idle_cb)



#####
# """
obj = None
t1 = None
t2 = None

def timer_cb(obj, event, info, **kargs):
   print("tick1 \\o/", event, info, kargs)

   print("loop", obj.loop)
   print("pending", obj.pending)

   itv = obj.interval
   print("interval", itv)
   obj.interval = itv + 0.2
   
   # ml.quit(0)
   # t1.event_callback_del("tick", timer_cb, asd=4, pippo="pippo")
   # obj.delete()

def timer_cb2(*args, **kargs):
   print("tick2 \\o/")
   # print(args, kargs)

   print("QUIT 2")
   t2.event_callback_del("tick", timer_cb2)


print("\n---- Test: Efl.Loop.Timer")
t1 = efl.loop.Timer(ml, 1.0)
t1.event_callback_add("tick", timer_cb, asd=4, pippo="pippo")
# t1.event_callback_add("tick", timer_cb, asd=4, pippo="pippo2")
print("PARENT:", t1.parent_get())

# t2 = efl2.loop.Timer(ml, 2.0)
# t2.event_callback_add("tick", timer_cb2)


# ml.parent_get()
ml.begin()
# """


# print("\n---- Test: Efl.Loop")
# ml = efl.Loop()
# print(ml)
# ml.parent_get()
# ml.begin()


