
#include <Python.h>

#include <Eina.h>
#include <Eo.h>
#include <Efl.h>
#include <Ecore.h>


#define INSIDE_EFL_MODULE
#include "_efl.module.h"
#undef INSIDE_EFL_MODULE


// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);


///////////////////////////////////////////////////////////////////////////////
////  The "efl" namespace MODULE  /////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

static PyObject *
efl_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command))
        return NULL;
    sts = system(command);
    return PyLong_FromLong(sts);
}


/* List of functions defined in the module */
static PyMethodDef ThisModuleMethods[] = {

    {"system",  efl_system, METH_VARARGS, "function doc"},

    {NULL, NULL, 0, NULL}        /* Sentinel */
};


/* The module definition */
static struct PyModuleDef ThisModule = {
   PyModuleDef_HEAD_INIT,
   "_efl",     /* name of module */
   "module doc",  /* module documentation, may be NULL */
   -1,            /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
   ThisModuleMethods
};


/* C API table - always add new things to the end for binary compatibility. */
static PyEfl_CAPI_t PyEfl_CAPI = {
    // exported types
    &PyEfl_ObjectTypeInternal,
    &PyEfl_LoopTypeInternal,
    &PyEfl_Loop_UserTypeInternal,
    &PyEfl_AnimatorTypeInternal,
    &PyEfl_ConfigTypeInternal,
    &PyEfl_PartTypeInternal,
    // exported utility functions
    &pyefl_class_register,
    &pyefl_object_from_instance
};

/* Module init function, func name must match module name! (PyInit_XXX) */
PyMODINIT_FUNC
PyInit__efl(void)
{
    PyObject *m;

    DBG("module import");

    // TODO how can I autogenerate this init call ??
    eina_init(); // TODO check for errors
    ecore_init(); // TODO check for errors

    m = PyModule_Create(&ThisModule);
    if (m == NULL)
        return NULL;


    /* Finalize all the type objects including setting type of the new type
     * object; doing it here is required for portability, too. */
    if (!pyefl_object_object_finalize(m)) return NULL;
    if (!pyefl_loop_object_finalize(m)) return NULL;
    if (!pyefl_loop_user_object_finalize(m)) return NULL;
    if (!pyefl_animator_object_finalize(m)) return NULL;
    if (!pyefl_config_object_finalize(m)) return NULL;
    if (!pyefl_part_object_finalize(m)) return NULL;

    /* Export C API */
    if (PyModule_AddObject(m, "CAPI",
           PyCapsule_New(&PyEfl_CAPI, PyEFL_CAPSULE_NAME, NULL)
                             ) != 0)
        return NULL;

    return m;
}
