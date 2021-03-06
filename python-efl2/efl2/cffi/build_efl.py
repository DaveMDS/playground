###################################
## THIS FILE IS MANUALLY WRITTEN ##
###################################

from cffi import FFI
import os


ffi = FFI()

ffi.set_source(
    'efl2._efl_ffi',
    libraries=['efl', 'eina', 'eo', 'evas', 'ecore', 'elementary'],
    define_macros=[
        ('EFL_BETA_API_SUPPORT', 1),
        ('EFL_EO_API_SUPPORT', 1),
    ],

    include_dirs=[
        '/usr/local/include/efl-1',
        '/usr/local/include/eina-1',
        '/usr/local/include/eina-1/eina',
        '/usr/local/include/eo-1',
        '/usr/local/include/ecore-1',
        '/usr/local/include/eet-1',
        '/usr/local/include/emile-1',
        '/usr/local/include/evas-1',
        '/usr/local/include/ecore-evas-1',
        '/usr/local/include/ecore-file-1',
        '/usr/local/include/ecore-input-1',
        '/usr/local/include/ecore-imf-1',
        '/usr/local/include/ecore-con-1',
        '/usr/local/include/edje-1',
        '/usr/local/include/eldbus-1',
        '/usr/local/include/efreet-1',
        '/usr/local/include/ethumb-client-1',
        '/usr/local/include/ethumb-1',
        '/usr/local/include/elocation-1',
        '/usr/local/include/elementary-1',
    ], # TODO FIXME

    source="""
    #include <Eina.h>
    #include <Eo.h>
    #include <Efl.h>
    #include <Evas.h>
    #include <Ecore.h>
    #include <Elementary.h>
    """
)


# TODO: read all the *.h files instead !!!
# for header in 'eina.h', 'eo.h', 'efl.h', 'evas.h', 'ecore.h', 'elementary.h':
for header in 'eina.h', 'eo.h', 'ecore_mainloop.h':
    with open(os.path.join(os.path.dirname(__file__), header)) as f:
        ffi.cdef(f.read())



if __name__ == '__main__':
    ffi.compile()
