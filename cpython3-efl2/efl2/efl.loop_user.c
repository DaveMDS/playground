#include <Python.h>


#include <Eo.h>
#include <Efl.h>
#include <Ecore.h> // EFL_LOOP_USER_CLASS is defined here

#include "efl.object.h"


// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);

///////////////////////////////////////////////////////////////////////////////
////  OBJECT  /////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

typedef struct {
    Efl_ObjectObject base;
    // PyObject            *x_attr;        /* Attributes dictionary */
} Efl_Loop_UserObject;

// Needed??
static PyTypeObject Efl_Loop_UserType;
// Needed??
#define Efl_Loop_User_Check(v) (Py_TYPE(v) == Efl_Loop_UserType)


static int
Efl_Loop_User_init(Efl_Loop_UserObject *self, PyObject *args, PyObject *kwds)
{
    DBG("init()")

    Eo *o;
    o  = efl_add(EFL_LOOP_USER_CLASS, NULL);
    ((Efl_ObjectObject*)self)->obj = o;

    /* Call the base class __init__ func */
    if (Efl_ObjectType->tp_init((PyObject *)self, args, kwds) < 0)
        return -1;

    return 0;
}

static void
Efl_Loop_User_dealloc(Efl_Loop_UserObject *self)
{
    DBG("dealloc()")
    // Py_XDECREF(self->x_attr);
    PyObject_Del(self);
}

static PyObject *  // Efl.Loop_User.loop (getter)
Efl_Loop_User_loop_get(Efl_Loop_UserObject *self, void *closure)
{
    Efl_Loop *loop;
    loop = efl_loop_get(self->base.obj);
    return _eo_object_from_instance(loop);
}

/* Functions table for Efl.Loop_User class */
static PyMethodDef Efl_Loop_User_methods[] = {
    {NULL, NULL, 0, NULL}  /* sentinel */
};

/* Properties table for Efl.Loop_User class */
static PyGetSetDef EFL_Loop_Timer_getsetters[] = {
    {"loop",
        (getter)Efl_Loop_User_loop_get,
        NULL, /* readonly */
        NULL, NULL},
    {NULL, 0, 0, NULL, NULL}  /* sentinel */
};

static PyTypeObject Efl_Loop_UserType = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "_loop_user._Loop_User",    /*tp_name*/
    sizeof(Efl_Loop_UserObject),/*tp_basicsize*/
    0,                          /*tp_itemsize*/
    /* methods */
    (destructor)Efl_Loop_User_dealloc,    /*tp_dealloc*/
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
    0,                          /*tp_traverse*/
    0,                          /*tp_clear*/
    0,                          /*tp_richcompare*/
    0,                          /*tp_weaklistoffset*/
    0,                          /*tp_iter*/
    0,                          /*tp_iternext*/
    Efl_Loop_User_methods,           /*tp_methods*/
    0,                          /*tp_members*/
    0,                          /*tp_getset*/
    0, /* setted in init */     /*tp_base*/
    0,                          /*tp_dict*/
    0,                          /*tp_descr_get*/
    0,                          /*tp_descr_set*/
    0,                          /*tp_dictoffset*/
    (initproc)Efl_Loop_User_init,    /* tp_init */
    0,                          /*tp_alloc*/
    0, /* setted in init */     /*tp_new*/
    0,                          /*tp_free*/
    0,                          /*tp_is_gc*/
};

///////////////////////////////////////////////////////////////////////////////
////  MODULE  /////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

// static PyObject *
// efl_loop_system(PyObject *self, PyObject *args)
// {
    // const char *command;
    // int sts;

    // if (!PyArg_ParseTuple(args, "s", &command))
        // return NULL;
    // sts = system(command);
    // return PyLong_FromLong(sts);
// }


/* List of functions defined in the module */
static PyMethodDef ThisModuleMethods[] = {
    
    // {"system",  efl_loop_system, METH_VARARGS, "function doc"},
    
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


/* The module definition */
static struct PyModuleDef ThisModule = {
   PyModuleDef_HEAD_INIT,
   "_loop_user",  /* name of module */
   "module doc",  /* module documentation, may be NULL */
   -1,            /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
   ThisModuleMethods
};

/* Module init function, func name must match module name! (PyInit_XXX) */
PyMODINIT_FUNC
PyInit__loop_user(void)
{
    PyObject *m;

    // TODO how can I autogenerate this init call ??
    ecore_init(); // TODO check for errors

    /* Import the Efl namespace C API (_eo_* and others) */
    if (import_efl() < 0)
        return NULL;

    /* Finalize the type object including setting type of the new type
     * object; doing it here is required for portability, too. */
    Efl_Loop_UserType.tp_new = PyType_GenericNew;
    Efl_Loop_UserType.tp_base = Efl_ObjectType;
    if (PyType_Ready(&Efl_Loop_UserType) < 0)
        return NULL;

    m = PyModule_Create(&ThisModule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&Efl_Loop_UserType);
    PyModule_AddObject(m, "_Loop_User", (PyObject *)&Efl_Loop_UserType);
    _eo_class_register(EFL_LOOP_USER_CLASS, &Efl_Loop_UserType);

    return m;
}

