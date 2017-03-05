#include <Python.h>


#include <Eo.h>
#include <Efl.h>
#include <Ecore.h> // EFL_LOOP_CLASS is defined here

#include "efl.object.h"


// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);


///////////////////////////////////////////////////////////////////////////////
////  OBJECT  /////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

typedef struct {
    Efl_ObjectObject base_class;
    // PyObject            *x_attr;        /* Attributes dictionary */
} Efl_LoopObject;

// Needed??
static PyTypeObject Efl_LoopType;
// Needed??
#define Efl_Loop_Check(v) (Py_TYPE(v) == Efl_LoopType)


static int
Efl_Loop_init(Efl_LoopObject *self, PyObject *args, PyObject *kwds)
{
    DBG("init()")

    // TODO FIX this should be at class level, not repeated for every instance */
    _eo_event_register((Efl_ObjectObject*)self, EFL_LOOP_EVENT_ARGUMENTS);
    _eo_event_register((Efl_ObjectObject*)self, EFL_LOOP_EVENT_IDLE_ENTER);
    _eo_event_register((Efl_ObjectObject*)self, EFL_LOOP_EVENT_IDLE_EXIT);
    _eo_event_register((Efl_ObjectObject*)self, EFL_LOOP_EVENT_IDLE);

    Eo *o;
    o  = efl_add(EFL_LOOP_CLASS, NULL);
    ((Efl_ObjectObject*)self)->obj = o;

    /* Call the base class __init__ func */
    if (Efl_ObjectType->tp_init((PyObject *)self, args, kwds) < 0)
        return -1;

    return 0;
}

static void
Efl_Loop_dealloc(Efl_LoopObject *self)
{
    DBG("dealloc()")
    // Py_XDECREF(self->x_attr);
    PyObject_Del(self);
}

static PyObject *
Efl_Loop_begin(Efl_LoopObject *self, PyObject *args)
{
    DBG("begin()")

    efl_loop_begin(self->base_class.obj);

    Py_RETURN_NONE;
}

static PyObject *
Efl_Loop_quit(Efl_LoopObject *self, PyObject *args)
{
    unsigned char arg1_exit_code;

    DBG("quit()")
    if (!PyArg_ParseTuple(args, "i:quit", &arg1_exit_code))
        return NULL;

    efl_loop_quit(self->base_class.obj, arg1_exit_code);

    Py_RETURN_NONE;
}

/* List of functions defined in the object */
static PyMethodDef Efl_Loop_methods[] = {
    {"begin",    (PyCFunction)Efl_Loop_begin,  METH_NOARGS, NULL},
    {"quit",     (PyCFunction)Efl_Loop_quit,  METH_VARARGS, NULL},
    {NULL, NULL}           /* sentinel */
};

static PyTypeObject Efl_LoopType = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "_loop._Loop",              /*tp_name*/
    sizeof(Efl_LoopObject),     /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    /* methods */
    (destructor)Efl_Loop_dealloc,    /*tp_dealloc*/
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
    Efl_Loop_methods,           /*tp_methods*/
    0,                          /*tp_members*/
    0,                          /*tp_getset*/
    0, /* setted in init */     /*tp_base*/
    0,                          /*tp_dict*/
    0,                          /*tp_descr_get*/
    0,                          /*tp_descr_set*/
    0,                          /*tp_dictoffset*/
    (initproc)Efl_Loop_init,    /* tp_init */
    0,                          /*tp_alloc*/
    0, /* setted in init */     /*tp_new*/
    0,                          /*tp_free*/
    0,                          /*tp_is_gc*/
};

///////////////////////////////////////////////////////////////////////////////
////  MODULE  /////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

/* List of functions defined in the module */
static PyMethodDef ThisModuleMethods[] = {

    //TODO can we avoid this struct if no methods are present at module level?

    {NULL, NULL, 0, NULL}        /* Sentinel */
};


/* The module definition */
static struct PyModuleDef ThisModule = {
   PyModuleDef_HEAD_INIT,
   "_loop",     /* name of module */
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

    DBG("module import");

    // TODO how can I autogenerate this init call ??
    ecore_init(); // TODO check for errors

    /* Import the Efl namespace C API (_eo_* and others) */
    if (import_efl() < 0)
        return NULL;

    /* Finalize the type object including setting type of the new type
     * object; doing it here is required for portability, too. */
    Efl_LoopType.tp_new = PyType_GenericNew;
    Efl_LoopType.tp_base = Efl_ObjectType;
    if (PyType_Ready(&Efl_LoopType) < 0)
        return NULL;

    m = PyModule_Create(&ThisModule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&Efl_LoopType);
    PyModule_AddObject(m, "_Loop", (PyObject *)&Efl_LoopType);
    _eo_class_register(EFL_LOOP_CLASS, &Efl_LoopType);

    return m;
}

