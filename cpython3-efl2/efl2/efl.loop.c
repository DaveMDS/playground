#include <Python.h>


#include <Eo.h>
#include <Efl.h>
#include <Ecore.h> // EFL_LOOP_CLASS is defined here

#include "eo_utils.h"
#include "efl.object.h"
#include "efl.loop.h"


// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);


///////////////////////////////////////////////////////////////////////////////
////  OBJECT  /////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

static int
Efl_Loop_init(PyEfl_Loop *self, PyObject *args, PyObject *kwds)
{
    DBG("init()")

    // TODO FIX this should be at class level, not repeated for every instance */
    pyefl_event_register((PyEfl_Object*)self, EFL_LOOP_EVENT_ARGUMENTS);
    pyefl_event_register((PyEfl_Object*)self, EFL_LOOP_EVENT_IDLE_ENTER);
    pyefl_event_register((PyEfl_Object*)self, EFL_LOOP_EVENT_IDLE_EXIT);
    pyefl_event_register((PyEfl_Object*)self, EFL_LOOP_EVENT_IDLE);

    Eo *o;
    o  = efl_add(EFL_LOOP_CLASS, NULL);
    ((PyEfl_Object*)self)->obj = o;

    /* Call the base class __init__ func */
    if (PyEfl_ObjectType.tp_init((PyObject *)self, args, kwds) < 0)
        return -1;

    return 0;
}

static void
Efl_Loop_dealloc(PyEfl_Loop *self)
{
    DBG("dealloc()")
    // Py_XDECREF(self->x_attr);
    PyObject_Del(self);
}

static PyObject *
Efl_Loop_begin(PyEfl_Loop *self, PyObject *args)
{
    DBG("begin()")

    efl_loop_begin(self->base.obj);

    Py_RETURN_NONE;
}

static PyObject *
Efl_Loop_quit(PyEfl_Loop *self, PyObject *args)
{
    unsigned char arg1_exit_code;

    DBG("quit()")
    if (!PyArg_ParseTuple(args, "i:quit", &arg1_exit_code))
        return NULL;

    efl_loop_quit(self->base.obj, arg1_exit_code);

    Py_RETURN_NONE;
}

/* List of functions defined in the object */
static PyMethodDef Efl_Loop_methods[] = {
    {"begin",    (PyCFunction)Efl_Loop_begin,  METH_NOARGS, NULL},
    {"quit",     (PyCFunction)Efl_Loop_quit,  METH_VARARGS, NULL},
    {NULL, NULL}           /* sentinel */
};

PyTypeObject PyEfl_LoopType = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "_loop._Loop",              /*tp_name*/
    sizeof(PyEfl_Loop),         /*tp_basicsize*/
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


Eina_Bool
pyefl_loop_object_finalize(PyObject *module)
{
    DBG("pyefl_init");

    PyEfl_LoopType.tp_new = PyType_GenericNew;
    PyEfl_LoopType.tp_base = &PyEfl_ObjectType;
    if (PyType_Ready(&PyEfl_LoopType) < 0)
        return EINA_FALSE;
        
    PyModule_AddObject(module, "_Loop", (PyObject *)&PyEfl_LoopType);
    Py_INCREF(&PyEfl_LoopType);

    pyefl_class_register(EFL_LOOP_CLASS, &PyEfl_LoopType);

    return EINA_TRUE;
}
