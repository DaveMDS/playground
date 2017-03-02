#include <Python.h>

#include <Eo.h>
#include "efl.object.h"


#define DBG(x) printf("Efl.Object: "x);printf("\n");

///////////////////////////////////////////////////////////////////////////////
////  The Efl.Object OBJECT  //////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

// Needed??
static PyTypeObject Efl_ObjectType;
// Needed??
#define Efl_Object_Check(v) (Py_TYPE(v) == Efl_ObjectType)


static void
Efl_Object_dealloc(Efl_ObjectObject *self)
{
    DBG("dealloc()")
    Py_XDECREF(self->x_attr);
    PyObject_Del(self);
}

static int
Efl_Object_traverse(Efl_ObjectObject *self, visitproc visit, void *arg)
{
    DBG("traverse()")
    Py_VISIT(self->x_attr);
    return 0;
}

static int
Efl_Object_init(Efl_ObjectObject *self, PyObject *args, PyObject *kwds)
{
    DBG("init()")
    // if (PyList_Type.tp_init((PyObject *)self, args, kwds) < 0)
        // return -1;
    // self->state = 0;
    return 0;
}


// static int
// Efl_Object_finalize(Efl_ObjectObject *self)
// {
    // Py_CLEAR(self->x_attr);
    // return 0;
// }


static PyObject *
Efl_Object_parent_get(Efl_ObjectObject *self, PyObject *args)
{
    DBG("PARENT 1")
    if (!PyArg_ParseTuple(args, ":parent_get"))
        return NULL;

    DBG("PARENT 2")
    Py_INCREF(Py_None);
    return Py_None;
}

/* List of functions defined in the object */
static PyMethodDef Efl_Object_methods[] = {
    {"parent_get",    (PyCFunction)Efl_Object_parent_get,  METH_VARARGS,
        PyDoc_STR("demo() -> None")},
    {NULL, NULL}           /* sentinel */
};

static PyTypeObject Efl_ObjectType = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "_object._Object",          /*tp_name*/
    sizeof(Efl_ObjectObject),  /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    /* methods */
    (destructor)Efl_Object_dealloc,    /*tp_dealloc*/
    0,                          /*tp_print*/
    (getattrfunc)0,             /*tp_getattr*/
    // (setattrfunc)Xxo_setattr,   /*tp_setattr*/
    0,                             /*tp_setattr*/
    0,                          /*tp_reserved*/
    0,                          /*tp_repr*/
    0,                          /*tp_as_number*/
    0,                          /*tp_as_sequence*/
    0,                          /*tp_as_mapping*/
    0,                          /*tp_hash*/
    0,                          /*tp_call*/
    0,                          /*tp_str*/
    // (getattrofunc)Xxo_getattro, /*tp_getattro*/
    0,                             /*tp_getattro*/
    0,                          /*tp_setattro*/
    0,                          /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_BASETYPE,    /*tp_flags*/
    0,                          /*tp_doc*/
    (traverseproc)Efl_Object_traverse,        /*tp_traverse*/
    0,                          /*tp_clear*/
    0,                          /*tp_richcompare*/
    0,                          /*tp_weaklistoffset*/
    0,                          /*tp_iter*/
    0,                          /*tp_iternext*/
    Efl_Object_methods,         /*tp_methods*/
    0,                          /*tp_members*/
    0,                          /*tp_getset*/
    0,                          /*tp_base*/
    0,                          /*tp_dict*/
    0,                          /*tp_descr_get*/
    0,                          /*tp_descr_set*/
    0,                          /*tp_dictoffset*/
    (initproc)Efl_Object_init,  /* tp_init */
    0,                          /*tp_alloc*/
    0,                          /*tp_new*/
    0,                          /*tp_free*/
    0,                          /*tp_is_gc*/
};

///////////////////////////////////////////////////////////////////////////////
////  The efl._object MODULE  /////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

static PyObject *
efl_object_system(PyObject *self, PyObject *args)
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
    
    {"system",  efl_object_system, METH_VARARGS, "function doc"},
    
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


/* The module definition */
static struct PyModuleDef ThisModule = {
   PyModuleDef_HEAD_INIT,
   "_object",     /* name of module */
   "module doc",  /* module documentation, may be NULL */
   -1,            /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
   ThisModuleMethods
};


/* C API table - always add new things to the end for binary
   compatibility. */
static
EflObject_CAPIObject EflObjectCAPI =
{
    &Efl_ObjectType//,
    // NULL,
    // NULL
};

/* Module init function, func name must match module name! (PyInit_XXX) */
PyMODINIT_FUNC
PyInit__object(void)
{
    PyObject *m;

    /* Finalize the type object including setting type of the new type
     * object; doing it here is required for portability, too. */
    Efl_ObjectType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&Efl_ObjectType) < 0)
        return NULL;

    m = PyModule_Create(&ThisModule);
    if (m == NULL)
        return NULL;
    
    Py_INCREF(&Efl_ObjectType);
    PyModule_AddObject(m, "_Object", (PyObject *)&Efl_ObjectType);

    /* Export C API */
    if (PyModule_AddObject(m, EflObject_CAPI_NAME,
           PyCapsule_New(&EflObjectCAPI, EflObject_CAPSULE_NAME, NULL)
                             ) != 0)
        return NULL;

    return m;
}
