#include <Python.h>


#include <Eo.h>
#include <Efl.h>
#include <Ecore.h> // EFL_LOOP_TIMER_CLASS is defined here

#include "../_efl.module.h"
#include "efl.loop.timer.h"
#include "efl.loop.fd.h"

// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);


///////////////////////////////////////////////////////////////////////////////
////  The "efl.loop" namespace MODULE  ////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

/* List of functions defined in the module */
static PyMethodDef ThisModuleMethods[] = {
    
    //TODO can we avoid this struct if no methods are present at module level?
    
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


/* The module definition */
static struct PyModuleDef ThisModule = {
   PyModuleDef_HEAD_INIT,
   "efl._loop",      /* name of module */
   "module doc",  /* module documentation, may be NULL */
   -1,            /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
   ThisModuleMethods
};

/* Module init function, func name must match module name! (PyInit_XXX) */
PyMODINIT_FUNC
PyInit__loop(void)
{
    PyObject *m;

    // TODO how can I autogenerate this init call ??
    ecore_init(); // TODO check for errors

    /* Import the Efl namespace C API (pyefl_* and types in the efl namespace) */
    if (import_efl() < 0)
        return NULL;

    m = PyModule_Create(&ThisModule);
    if (m == NULL)
        return NULL;

    /* Finalize all the type objects including setting type of the new type
     * object; doing it here is required for portability, too. */
    if (!pyefl_loop_timer_object_finalize(m)) return NULL;
    if (!pyefl_loop_fd_object_finalize(m)) return NULL;

    return m;
}

