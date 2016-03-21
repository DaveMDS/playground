from cffi import FFI

ffi = FFI()


    # Since we are calling fnmatch directly no custom source is necessary. We
    # need to #include <fnmatch.h>, though, because behind the scenes cffi
    # generates a .c file which contains a Python-friendly wrapper around
    # ``fnmatch``:
    #    static PyObject *
    #    _cffi_f_fnmatch(PyObject *self, PyObject *args) {
    #        ... setup ...
    #        result = fnmatch(...);
    #        return PyInt_FromLong(result);
    #    }


ffi.set_source(
    'efl2._ecore',
    libraries=['efl', 'eina', 'eo', 'ecore'],
    include_dirs=[
        '/usr/local/include/efl-1',
        '/usr/local/include/eina-1',
        '/usr/local/include/eina-1/eina',
        '/usr/local/include/eo-1',
        '/usr/local/include/ecore-1',
        ], # TODO FIXME

    # include_dirs=['/usr/include/SDL', '/usr/local/include/SDL'],

    source="""
    #include <Ecore.h>
    """
)


ffi.cdef("""


int ecore_init(void);
int ecore_shutdown(void);

void ecore_main_loop_begin(void);
void ecore_main_loop_quit(void);


typedef int Eina_Bool; /*FIXME*/

typedef void Ecore_Timer; /*FIXME*/

typedef Eina_Bool(*Ecore_Task_Cb) (void *data);


Ecore_Timer *ecore_timer_add(double in, Ecore_Task_Cb func, const void *data);


extern "Python" Eina_Bool _timer_cb(void *data);

""")

if __name__ == "__main__":
    ffi.compile()
