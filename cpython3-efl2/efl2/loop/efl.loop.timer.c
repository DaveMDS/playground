#include <Python.h>


#include <Eo.h>
#include <Efl.h>
#include <Ecore.h> // EFL_LOOP_TIMER_CLASS is defined here

#include "../efl.object.h"
#include "../efl.loop_user.h"

// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);

///////////////////////////////////////////////////////////////////////////////
////  OBJECT  /////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

typedef struct {
    Efl_Loop_UserObject base;
} Efl_Loop_TimerObject;


static PyTypeObject Efl_Loop_TimerType;

#define Efl_Loop_Timer_Check(v) (Py_TYPE(v) == Efl_Loop_TimerType)


static int
Efl_Loop_Timer_init(Efl_Loop_TimerObject *self, PyObject *args, PyObject *kwds)
{
    DBG("init()")
    double interval;
    Efl_ObjectObject *parent;

    // TODO FIX this should be at class level, not repeated for every instance */
    _eo_event_register((Efl_ObjectObject*)self, EFL_LOOP_TIMER_EVENT_TICK);


    if (!PyArg_ParseTuple(args, "Od:Timer", &parent, &interval))
        return -1;

    // TODO check parent is a valid Eo object

    Eo *o;
    o  = efl_add(EFL_LOOP_TIMER_CLASS, parent->obj,
            efl_loop_timer_interval_set(efl_added, interval));
    ((Efl_ObjectObject*)self)->obj = o;
    if (!o)
        return -1;

    /* Call the base class __init__ func */
    if (Efl_ObjectType->tp_init((PyObject *)self, args, kwds) < 0)
        return -1;

    return 0;
}

static void
Efl_Loop_Timer_dealloc(Efl_Loop_TimerObject *self)
{
    DBG("dealloc()")
    // Py_XDECREF(self->x_attr);
    PyObject_Del(self);  //TODO FIXME !!!!
}


static PyObject *  // Efl.Loop.Timer.delay()
Efl_Loop_Timer_delay(Efl_Loop_TimerObject *self, PyObject *args)
{
    DBG("delay()")

    // Fetch python args (double add)
    double arg1_add;
    if (!PyArg_ParseTuple(args, "d:delay", &arg1_add))
        return NULL;

    efl_loop_timer_delay(((Efl_ObjectObject *)(self))->obj, arg1_add);

    Py_RETURN_NONE;
}

static PyObject *  // Efl.Loop.Timer.loop_reset()
Efl_Loop_Timer_loop_reset(Efl_Loop_TimerObject *self, PyObject *args)
{
    DBG("loop_reset()")
    efl_loop_timer_loop_reset(((Efl_ObjectObject *)(self))->obj);
    Py_RETURN_NONE;
}

static PyObject *  // Efl.Loop.Timer.reset()
Efl_Loop_Timer_reset(Efl_Loop_TimerObject *self, PyObject *args)
{
    DBG("reset()")
    efl_loop_timer_reset(((Efl_ObjectObject *)(self))->obj);
    Py_RETURN_NONE;
}

static PyObject *  // Efl.Loop.Timer.interval (getter)
Efl_Loop_Timer_interval_get(Efl_Loop_TimerObject *self, void *closure)
{
    double in;
    in = efl_loop_timer_interval_get(((Efl_ObjectObject *)(self))->obj);
    return Py_BuildValue("d", in);
}

static int  // Efl.Loop.Timer.interval (setter)
Efl_Loop_Timer_interval_set(Efl_Loop_TimerObject *self, PyObject *value, void *closure)
{
    DBG("interval_set()")
    double val = PyFloat_AsDouble(value);
    efl_loop_timer_interval_set(((Efl_ObjectObject *)(self))->obj, val);
    return 0;
}

static PyObject *  // Efl.Loop.Timer.pending (getter)
Efl_Loop_Timer_pending_get(Efl_Loop_TimerObject *self, void *closure)
{
    double val;
    val = efl_loop_timer_pending_get(((Efl_ObjectObject *)(self))->obj);
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

static PyTypeObject Efl_Loop_TimerType = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "_timer._Timer",    /*tp_name*/
    sizeof(Efl_Loop_TimerObject),/*tp_basicsize*/
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
   "_timer",      /* name of module */
   "module doc",  /* module documentation, may be NULL */
   -1,            /* size of per-interpreter state of the module,
                     or -1 if the module keeps state in global variables. */
   ThisModuleMethods
};

/* Module init function, func name must match module name! (PyInit_XXX) */
PyMODINIT_FUNC
PyInit__timer(void)
{
    PyObject *m;

    // TODO how can I autogenerate this init call ??
    ecore_init(); // TODO check for errors

    /* Import the Efl namespace C API (_eo_* and others) */
    if (import_efl() < 0)
        return NULL;

    /* Import the base class namespace C API */
    if (import_efl_loop_user() < 0)
        return NULL;

    /* Finalize the type object including setting type of the new type
     * object; doing it here is required for portability, too. */
    Efl_Loop_TimerType.tp_new = PyType_GenericNew;
    Efl_Loop_TimerType.tp_base = Efl_Loop_UserType;
    if (PyType_Ready(&Efl_Loop_TimerType) < 0)
        return NULL;

    m = PyModule_Create(&ThisModule);
    if (m == NULL)
        return NULL;

    Py_INCREF(&Efl_Loop_TimerType);
    PyModule_AddObject(m, "_Timer", (PyObject *)&Efl_Loop_TimerType);
    _eo_class_register(EFL_LOOP_TIMER_CLASS, &Efl_Loop_TimerType);

    return m;
}

