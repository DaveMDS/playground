from cffi import FFI
import os


ffi = FFI()

ffi.set_source(
    'efl2._eina_ffi',
    libraries=['efl', 'eina'],
    define_macros=[
        ('EFL_BETA_API_SUPPORT', 1),
        ('EFL_EO_API_SUPPORT', 1),
    ],
    include_dirs=[
        '/usr/local/include/efl-1',
        '/usr/local/include/eina-1',
        '/usr/local/include/eina-1/eina',
        ], # TODO FIXME !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    source="""
    #include <Eina.h>

    // Here you can write C glue code if needed   <--

    """
)

for header in "eina_cdef.h", :
    with open(os.path.join(os.path.dirname(__file__), header)) as f:
        ffi.cdef(f.read())


if __name__ == "__main__":
    ffi.compile()
