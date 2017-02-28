#! /usr/bin/env python3
# encoding: utf-8


import efl2 as efl
# from efl2 import system
# from efl2 import Object

# print(system("ls -l"))

print("----")

# instance
o = efl.Object()
print(o)


# subclass
class MyEoObject(efl.Object):
   def __init__(self):
      print("__INIT__")

o = MyEoObject()
print(o)
