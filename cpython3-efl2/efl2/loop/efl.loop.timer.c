#include <Python.h>


#include <Eo.h>
#include <Efl.h>
#include <Ecore.h> // EFL_LOOP_TIMER_CLASS is defined here


#include "../_efl.module.h"
#include "efl.loop.timer.h"

// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);


static int
Efl_Loop_Timer_init(PyEfl_Loop_Timer *self, PyObject *args, PyObject *kwds)
{
    DBG("init()")
    double interval;
    PyEfl_Object *parent;

    // TODO FIX this should be at class level, not repeated for every instance */
    pyefl_event_register((PyEfl_Object*)self, EFL_LOOP_TIMER_EVENT_TICK);


    if (!PyArg_ParseTuple(args, "Od:Timer", &parent, &interval))
        return -1;

    // TODO check parent is a valid Eo object

    Eo *o;
    o  = efl_add(EFL_LOOP_TIMER_CLASS, parent->obj,
            efl_loop_timer_interval_set(efl_added, interval));
    ((PyEfl_Object*)self)->obj = o;
    if (!o)
        return -1;

    /* Call the base class __init__ func */
    if (PyEfl_ObjectType->tp_init((PyObject *)self, args, kwds) < 0)
        return -1;

    return 0;
}

static void
Efl_Loop_Timer_dealloc(PyEfl_Loop_Timer *self)
{
    DBG("dealloc()")
    // Py_XDECREF(self->x_attr);
    PyObject_Del(self);  //TODO FIXME !!!!
}


static PyObject *  // Efl.Loop.Timer.delay()
Efl_Loop_Timer_delay(PyEfl_Loop_Timer *self, PyObject *args)
{
    DBG("delay()")

    // Fetch python args (double add)
    double arg1_add;
    if (!PyArg_ParseTuple(args, "d:delay", &arg1_add))
        return NULL;

    efl_loop_timer_delay(((PyEfl_Object *)(self))->obj, arg1_add);

    Py_RETURN_NONE;
}

static PyObject *  // Efl.Loop.Timer.loop_reset()
Efl_Loop_Timer_loop_reset(PyEfl_Loop_Timer *self, PyObject *args)
{
    DBG("loop_reset()")
    efl_loop_timer_loop_reset(((PyEfl_Object *)(self))->obj);
    Py_RETURN_NONE;
}

static PyObject *  // Efl.Loop.Timer.reset()
Efl_Loop_Timer_reset(PyEfl_Loop_Timer *self, PyObject *args)
{
    DBG("reset()")
    efl_loop_timer_reset(((PyEfl_Object *)(self))->obj);
    Py_RETURN_NONE;
}

static PyObject *  // Efl.Loop.Timer.interval (getter)
Efl_Loop_Timer_interval_get(PyEfl_Loop_Timer *self, void *closure)
{
    double in;
    in = efl_loop_timer_interval_get(((PyEfl_Object *)(self))->obj);
    return Py_BuildValue("d", in);
}

static int  // Efl.Loop.Timer.interval (setter)
Efl_Loop_Timer_interval_set(PyEfl_Loop_Timer *self, PyObject *value, void *closure)
{
    DBG("interval_set()")
    double val = PyFloat_AsDouble(value);
    efl_loop_timer_interval_set(((PyEfl_Object *)(self))->obj, val);
    return 0;
}

static PyObject *  // Efl.Loop.Timer.pending (getter)
Efl_Loop_Timer_pending_get(PyEfl_Loop_Timer *self, void *closure)
{
    double val;
    val = efl_loop_timer_pending_get(((PyEfl_Object *)(self))->obj);
    return Py_BuildValue("d", val);
}

/* Functions table for Efl.Loop.Timer class */
static PyMethodDef Efl_Loop_Timer_methods[] = {
    {"delay", (PyCFunction)Efl_Loop_Timer_delay,
        METH_VARARGS, NULL},
    {"loop_reset", (PyCFunction)Efl_Loop_Timer_loop_reset,
        METH_NOARGS, NULL},
    {"reset", (PyCFunction)Efl_Loop_Timer_reset,
        METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}  /* sentinel */
};

/* Properties table for Efl.Loop.Timer class */
static PyGetSetDef EFL_Loop_Timer_getsetters[] = {
    {"interval",
        (getter)Efl_Loop_Timer_interval_get,
        (setter)Efl_Loop_Timer_interval_set,
        NULL, NULL},
    {"pending",
        (getter)Efl_Loop_Timer_pending_get,
        NULL, /* readonly */
        NULL, NULL},
    {NULL, 0, 0, NULL, NULL}  
};

PyTypeObject PyEfl_Loop_TimerType = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "_timer._Timer",    /*tp_name*/
    sizeof(PyEfl_Loop_Timer),   /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    /* methods */
    (destructor)Efl_Loop_Timer_dealloc,    /*tp_dealloc*/
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
    Efl_Loop_Timer_methods,     /*tp_methods*/
    0,                          /*tp_members*/
    EFL_Loop_Timer_getsetters,  /*tp_getset*/
    0, /* setted in init */     /*tp_base*/
    0,                          /*tp_dict*/
    0,                          /*tp_descr_get*/
    0,                          /*tp_descr_set*/
    0,                          /*tp_dictoffset*/
    (initproc)Efl_Loop_Timer_init,    /* tp_init */
    0,                          /*tp_alloc*/
    0, /* setted in init */     /*tp_new*/
    0,                          /*tp_free*/
    0,                          /*tp_is_gc*/
};


Eina_Bool
pyefl_loop_timer_object_finalize(PyObject *module)
{
    DBG("pyefl_init");

    /* Import the Efl namespace C API (pyefl_* and types in the efl namespace) */
    if (import_efl() < 0)
        return EINA_FALSE;

    PyEfl_Loop_TimerType.tp_new = PyType_GenericNew;
    PyEfl_Loop_TimerType.tp_base = PyEfl_Loop_UserType;
    if (PyType_Ready(&PyEfl_Loop_TimerType) < 0)
        return EINA_FALSE;
        
    PyModule_AddObject(module, "_Timer", (PyObject *)&PyEfl_Loop_TimerType);
    Py_INCREF(&PyEfl_Loop_TimerType);

    pyefl_class_register(EFL_LOOP_TIMER_CLASS, &PyEfl_Loop_TimerType);

    return EINA_TRUE;
}
