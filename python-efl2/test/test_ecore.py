import pytest

from efl2 import ecore


print("starting ecore ml :)")

def mycb(*args, **kargs):
    print(args, kargs)
    print(" \o/ " * 60)
    ecore.main_loop_quit()


t = ecore.Timer(1.0, mycb, 567, asd='AsD')

ecore.main_loop_begin()
