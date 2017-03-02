#! /usr/bin/env python3
# encoding: utf-8


import efl2
import efl2.loop
import efl2 as efl

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


print("\n---- Test: Efl.Loop")
ml = efl.Loop()

#####
print("\n---- Test: Efl.Loop.Timer")
t = efl2.loop.Timer(ml, 1.0)
print(t)
# ml.parent_get()
ml.begin()



# print("\n---- Test: Efl.Loop")
# ml = efl.Loop()
# print(ml)
# ml.parent_get()
# ml.begin()


