import os

from cffi import FFI

ffi = FFI()

ffi.set_source(
    'efl2._eo',
    libraries=['efl', 'eina', 'eo'],
    include_dirs=[
        '/usr/local/include/efl-1',
        '/usr/local/include/eina-1',
        '/usr/local/include/eina-1/eina',
        '/usr/local/include/eo-1',
        ], # TODO FIXME

    source="""
    #include <Eo.h>
    """
)


ffi.cdef("""


int eo_init(void);
int eo_shutdown(void);


""")

if __name__ == "__main__":
    ffi.compile()
