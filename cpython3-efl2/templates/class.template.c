<!--(include)-->copyright_c.include<!--(end)-->
<!--(include)-->macros.include<!--(end)-->
#include <Python.h>


#include <Eo.h>
#include <Efl.h>
#include <Ecore.h> // EFL_LOOP_TIMER_CLASS is defined here  TODO FIXME


#include "../_efl.module.h"  // TODO FIXME
#include "${cls.full_name.lower()}$.h"

// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);


static int
${CLS_OBJECT}$_init(${CLS_OBJECT}$ *self, PyObject *args, PyObject *kwds)
{
    DBG("init()")
    PyEfl_Object *parent;

<!--(if cls.full_name == 'Efl.Loop.Timer')-->
    /* Timer custom constructor */
    double interval;
    if (!PyArg_ParseTuple(args, "Od:Timer", &parent, &interval))
        return -1;

    Eo *o  = efl_add(EFL_LOOP_TIMER_CLASS, parent->obj,
                     efl_loop_timer_interval_set(efl_added, interval));

<!--(elif cls.full_name ==  'Efl.Ui.Win')-->
    // TODO Win cunstom constuctor
<!--(else)-->
    /* Standard Eo constructor */
    if (!PyArg_ParseTuple(args, "O:${cls.name}$", &parent))
        return -1;

    // TODO check parent is a valid Eo object
    Eo *o = efl_add(${cls.c_name}$, parent->obj, NULL);
<!--(end)-->

    /* Store the Eo object in self._obj */
    ((PyEfl_Object*)self)->obj = o;
    if (!o)
        return -1;

    /* Call the base class __init__ func */
    if (PyEfl_ObjectType->tp_init((PyObject *)self, args, kwds) < 0)
        return -1;

    // TODO FIX this should be at class level, not repeated for every instance */
<!--(for event in cls.events)-->
    pyefl_event_register((PyEfl_Object*)self, ${event.c_name}$);
<!--(end)-->

    return 0;
}

static void
${CLS_OBJECT}$_dealloc(${CLS_OBJECT}$ *self)
{
    DBG("dealloc()")
    // Py_XDECREF(self->x_attr);
    PyObject_Del(self);  //TODO FIXME !!!!
}

#! // PARAM_IN(param, obj)
<!--(macro PARAM_IN)-->
    <!--(if param.type.name == 'double')-->
double ${param.name}$ = PyFloat_AsDouble(${obj}$);
    <!--(elif param.type.name == 'int')-->
int ${param.name}$ = (int)PyLong_AsLong(${obj}$);
    <!--(else)-->
// ERROR: UNSUPPORTED IN PARAM TYPE: ${param.type}$
    <!--(end)-->
<!--(end)-->

#! // TYPE_OUT(type, obj)
<!--(macro TYPE_OUT)-->
    <!--(if type.name == 'double')-->
PyFloat_FromDouble(${obj}$);
    <!--(elif type.name == 'int')-->
PyLong_FromLong(${obj}$);
    <!--(else)-->
// ERROR: UNSUPPORTED OUT TYPE: ${type}$
    <!--(end)-->
<!--(end)-->

/* Class methods */
<!--(for func in cls.methods)-->
static PyObject *  // ${cls.full_name}$.${func.name}$()
${CLS_OBJECT}$_${func.name}$(${CLS_OBJECT}$ *self, PyObject *args)
{
    DBG("${func.name}$()")

    // input params
    <!--(if len(list(func.parameters)) == 1)-->
        <!--(for param in func.parameters)-->
    ${PARAM_IN(param=param, obj='args')}$
        <!--(end)-->
    <!--(elif len(list(func.parameters)) > 1)-->

    <!--(end)-->

    // c function call
    <!--(if len(list(func.parameters)) == 0)-->
    ${func.full_c_method_name}$(((PyEfl_Object *)(self))->obj);
    <!--(else)-->
    ${func.full_c_method_name}$(((PyEfl_Object *)(self))->obj
        <!--(for param in func.parameters)-->,${param.name}$<!--(end)-->
    );
    <!--(end)-->

    // return
    <!--(if func.method_return_type)-->

    <!--(else)-->
    Py_RETURN_NONE;
    <!--(end)-->
}
<!--(end)-->

/* Class methods table */
static PyMethodDef ${CLS_OBJECT}$_methods[] = {
    <!--(for func in cls.methods)-->
    {"${func.name}$", (PyCFunction)${CLS_OBJECT}$_${func.name}$,
        <!--(if len(list(func.parameters)) == 0)-->
        METH_NOARGS, NULL},
        <!--(elif len(list(func.parameters)) == 1)-->
        METH_O, NULL},
        <!--(else)-->
        METH_VARARGS, NULL},
        <!--(end)-->
    <!--(end)-->
    {NULL, NULL, 0, NULL}  /* sentinel */
};


/* Class Getters */
<!--(for func in cls.properties)-->
    <!--(if func.prop_readable)-->
static PyObject *  // ${cls.full_name}$.${func.name}$  (getter)
${CLS_OBJECT}$_${func.name}$_get(${CLS_OBJECT}$ *self, void *closure)
{
        <!--(if func.getter_return_type)-->
    ${func.getter_return_type.c_type}$ val;
        <!--(else)-->
    // TODO FIX for multiple vals !
            <!--(for val in func.setter_values)-->
    ${val.type.c_type}$ val;
            <!--(end)-->
        <!--(end)-->

    val = ${func.full_c_getter_name}$(((PyEfl_Object *)(self))->obj);

        <!--(if func.getter_return_type)-->
    return ${TYPE_OUT(type=func.getter_return_type, obj='val')}$
        <!--(else)-->
    // TODO FIX for multiple vals !
            <!--(for val in func.getter_values)-->
    return ${TYPE_OUT(type=val.type, obj='val')}$
            <!--(end)-->
        <!--(end)-->
}
    <!--(end)-->
<!--(end)-->

/* Class Setters */
<!--(for func in cls.properties)-->
    <!--(if func.prop_writable)-->
static PyObject *  // ${cls.full_name}$.${func.name}$  (setter)
${CLS_OBJECT}$_${func.name}$_set(${CLS_OBJECT}$ *self, PyObject *value, void *closure)
{
    // TODO FIX for multiple vals !
        <!--(for param in func.setter_values)-->
    ${PARAM_IN(param=param, obj='value')}$
        <!--(end)-->

    ${func.full_c_setter_name}$(((PyEfl_Object *)(self))->obj, ${val.name}$);
    return 0; // TODO is 0 correct ??
}
    <!--(end)-->
<!--(end)-->

/* Class getsetter table */
static PyGetSetDef ${CLS_OBJECT}$_getsetters[] = {
    <!--(for func in cls.properties)-->
    {"${func.name}$",
        <!--(if func.prop_readable)-->
        (getter)${CLS_OBJECT}$_${func.name}$_get,
        <!--(else)-->
        NULL, /* writeonly */
        <!--(end)-->
        <!--(if func.prop_writable)-->
        (setter)${CLS_OBJECT}$_${func.name}$_set,
        <!--(else)-->
        NULL, /* readonly */
        <!--(end)-->
        NULL, NULL},
    <!--(end)-->
    {NULL, 0, 0, NULL, NULL}  /* sentinel */
};

PyTypeObject ${CLS_OBJECT_TYPE}$ = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "${CLS_TP_NAME}$",          /*tp_name*/
    sizeof(${CLS_OBJECT}$),     /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    (destructor)${CLS_OBJECT}$_dealloc,
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
    ${CLS_OBJECT}$_methods,     /*tp_methods*/
    0,                          /*tp_members*/
    ${CLS_OBJECT}$_getsetters,  /*tp_getset*/
    0, /* setted in init */     /*tp_base*/
    0,                          /*tp_dict*/
    0,                          /*tp_descr_get*/
    0,                          /*tp_descr_set*/
    0,                          /*tp_dictoffset*/
    (initproc)${CLS_OBJECT}$_init,
    0,                          /*tp_alloc*/
    0, /* setted in init */     /*tp_new*/
    0,                          /*tp_free*/
    0,                          /*tp_is_gc*/
};


Eina_Bool
${OBJECT_FINALIZE_FUNC}$(PyObject *module)
{
    DBG("finalize");

    /* Import the Efl namespace C API (pyefl_* and types in the efl namespace) */
    if (import_efl() < 0)
        return EINA_FALSE;

    /* Finalize the object type */
    ${CLS_OBJECT_TYPE}$.tp_new = PyType_GenericNew;
    ${CLS_OBJECT_TYPE}$.tp_base = ${CLS_BASE_OBJECT}$Type;
    if (PyType_Ready(&${CLS_OBJECT_TYPE}$) < 0)
        return EINA_FALSE;

    /* Put the object in the calling module namespace */
    PyModule_AddObject(module, "_${cls.name}$", (PyObject *)&${CLS_OBJECT_TYPE}$);
    Py_INCREF(&${CLS_OBJECT_TYPE}$);

    /* Link the EO class with the python type object */
    pyefl_class_register(${CLS_EO_NAME}$, &${CLS_OBJECT_TYPE}$);

    return EINA_TRUE;
}
