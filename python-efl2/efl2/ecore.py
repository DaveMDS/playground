from ._ecore import ffi, lib
from .eo import Eo




def main_loop_begin():
    lib.ecore_main_loop_begin()

def main_loop_quit():
    lib.ecore_main_loop_quit()


print("ECORE INIT")
lib.ecore_init()
# TODO: atexit lib.ecore_shutdown()


@ffi.def_extern()
def _timer_cb(x):
    print("ASD")
    self = ffi.from_handle(x)
    if callable(self._priv['cb']):
        self._priv['cb'](*self._priv['cb_args'], **self._priv['cb_kargs'])

    return 0

class Timer(Eo):
    def __init__(self, timeout, callback, *args, **kargs):

        super(Timer, self).__init__()
        print("Timer INIT", timeout)

        userdata = ffi.new_handle(self)
        self._priv['self_h'] = userdata   # must keep this alive!   :/
        self._priv['cb'] = callback
        self._priv['cb_args'] = args
        self._priv['cb_kargs'] = kargs

        self._obj = lib.ecore_timer_add(timeout, lib._timer_cb, userdata)
        if self._obj == ffi.NULL:
            raise MemoryError("Could not create the object")
