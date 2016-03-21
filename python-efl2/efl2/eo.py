from ._eo import ffi, lib



# 
# def main_loop_begin():
    # lib.ecore_main_loop_begin()
# 
# def main_loop_quit():
    # lib.ecore_main_loop_quit()


print("EO INIT")
lib.eo_init()



class Eo(object):
    def __init__(self):
        print("Eo obstract")
        self._obj = None
        self._priv = dict()

