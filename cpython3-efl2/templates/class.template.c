<!--(include)-->copyright_c.include<!--(end)-->
<!--(include)-->macros.include<!--(end)-->
#include <Python.h>


#include <Efl.h>
#include <Eina.h>
#include <Eo.h>
#include <Ecore.h>
#include <Evas.h>
#include <Elementary.h>


<!--(if len(list(cls.namespaces)) == 1)-->
#include "eo_utils.h"
#include "efl.object.h"
<!--(elif len(list(cls.namespaces)) > 1)-->
#include "../_efl.module.h"
<!--(end)-->
#include "${cls.full_name.lower()}$.h"

// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);

///////////////////////////////////////////////////////////////////////////////
<!--(if cls.type == Eolian_Class_Type.REGULAR)-->
//  The ${cls.full_name}$ Class
<!--(elif cls.type == Eolian_Class_Type.INTERFACE)-->
//  The ${cls.full_name}$ Interface
<!--(else)-->
//  ${cls.full_name}$  -- UNKNOW CLS TYPE
<!--(end)-->
///////////////////////////////////////////////////////////////////////////////

/* Class __init__ method (constructor) */
static int
${CLS_OBJECT}$_init(${CLS_OBJECT}$ *self, PyObject *args, PyObject *kwds)
{
<!--(if cls.type == Eolian_Class_Type.INTERFACE)-->
    PyErr_SetString(PyExc_TypeError, "Interfaces cannot be instantiated");
    return -1;
<!--(elif cls.type == Eolian_Class_Type.MIXIN)-->
    PyErr_SetString(PyExc_TypeError, "Mixins cannot be instantiated");
    return -1;
<!--(else)-->
    DBG("init()")
    PyEfl_Object *parent = NULL;

  <!--(if cls.full_name == 'Efl.Loop.Timer')-->
    /* Timer custom constructor */
    double interval;
    if (!PyArg_ParseTuple(args, "Od:Timer", &parent, &interval))
        return -1;

    Eo *o  = efl_add(EFL_LOOP_TIMER_CLASS, parent->obj,
                     efl_loop_timer_interval_set(efl_added, interval));

  <!--(elif cls.full_name ==  'Efl.Ui.Win')-->
    // TODO Win custom constuctor
  <!--(else)-->
    /* Standard Eo constructor */
    if (!PyArg_ParseTuple(args, "|O:${cls.name}$", &parent))
        return -1;

    // TODO check parent is a valid Eo object
    Eo *o = efl_add(${cls.c_name}$, parent ? parent->obj : NULL, NULL);
  <!--(end)-->

    /* Store the Eo object in self._obj */
    ((PyEfl_Object*)self)->obj = o;
    if (!o)
        return -1;

    /* Call the base class __init__ func */
    if (PyEfl_ObjectType->tp_init((PyObject *)self, args, kwds) < 0)
        return -1;

    return 0;
<!--(end)-->
}
#!
#! // TYPE_IN_FUNC(type)
<!--(macro TYPE_IN_FUNC)-->
    <!--(if type.type == Eolian_Type_Type.CLASS)-->
        <!--(if type.full_name == 'Efl.Class')-->
pyefl_type_to_class#!
        <!--(else)-->
pyefl_object_to_pointer#!
        <!--(end)-->
    <!--(elif type.type == Eolian_Type_Type.REGULAR)-->
        <!--(if type.full_name == 'string')-->
PyUnicode_AsUTF8#!
        <!--(elif type.full_name == 'void_ptr')-->
void_func#!
        <!--(elif type.full_name == 'double')-->
PyFloat_AsDouble#!
        <!--(elif type.full_name in ('int','bool','short'))-->
(${type.c_type}$)PyLong_AsLong#!
        <!--(elif type.full_name in ('uint','ubyte'))-->
(${type.c_type}$)PyLong_AsUnsignedLong#!
        <!--(elif type.typedecl.type == Eolian_Typedecl_Type.STRUCT)-->
// ERROR: TODO struct ${type}$ ${type.typedecl}$ //
        <!--(else)-->
// ERROR: UNSUPPORTED IN PARAM TYPE: ${type}$ ${type.type}$ //
        <!--(end)-->
    <!--(else)-->
// ERROR: UNSUPPORTED IN PARAM TYPE.TYPE: ${type}$ ${type.type}$ //
    <!--(end)-->
<!--(end)-->
#!
#! // TYPE_OUT_FUNC(type)
<!--(macro TYPE_OUT_FUNC)-->
    <!--(if type.type == Eolian_Type_Type.CLASS)-->
        <!--(if type.full_name == 'Efl.Class')-->
TODO #!
        <!--(else)-->
pyefl_object_from_instance#!
        <!--(end)-->
    <!--(elif type.type == Eolian_Type_Type.REGULAR)-->
        <!--(if type.full_name == 'double')-->
PyFloat_FromDouble#!
        <!--(elif type.full_name in ('int','short'))-->
PyLong_FromLong#!
        <!--(elif type.full_name in ('uint','ubyte'))-->
PyLong_FromUnsignedLong#!
        <!--(elif type.full_name == 'bool')-->
PyBool_FromLong#!
        <!--(elif type.full_name in ('string','stringshare'))-->
PyUnicode_FromString#!
        <!--(elif type.typedecl.type == Eolian_Typedecl_Type.STRUCT)-->
// ERROR: TODO struct ${type}$ ${type.typedecl}$ //
        <!--(else)-->
// ERROR: UNSUPPORTED OUT TYPE: ${type}$ ${type.type}$ //
        <!--(end)-->
    <!--(else)-->
// ERROR: UNSUPPORTED IN PARAM TYPE.TYPE: ${type}$ ${type.type}$ //
    <!--(end)-->
<!--(end)-->

/* Class methods */
<!--(for func in cls.methods)-->
  <!--(if func.method_scope != Eolian_Object_Scope.PROTECTED and not func.full_c_method_name in excludes)-->
${setvar("num_params", "len(list(func.parameters))")}$#!
static PyObject *  // ${cls.full_name}$ ${func.name}$()
${CLS_OBJECT}$_${func.name}$(PyEfl_Object *self, PyObject *arg<!--(if num_params > 1)-->s<!--(end)-->)
{
    DBG("${func.name}$()")

    <!--(if num_params == 1)-->
    // single param
        <!--(for param in func.parameters)-->
    ${param.type.c_type}$ prm1_${param.name}$ = ${TYPE_IN_FUNC(type=param.type)}$(arg);
        <!--(end)-->
    <!--(elif num_params > 1)-->
    // multiple params
    if (!PyTuple_Check(args))
    {
        PyErr_SetString(PyExc_TypeError, "${func.name}$ called with wrong args");
        return NULL;
    }
    if (PyTuple_GET_SIZE(args) != ${num_params}$)
    {
        PyErr_SetString(PyExc_TypeError, "${func.name}$ called with wrong args num, ${num_params}$ expected");
        return NULL;
    }
        <!--(for i, param in enumerate(func.parameters))-->
    ${param.type.c_type}$ prm${i+1}$_${param.name}$ = ${TYPE_IN_FUNC(type=param.type)}$(PyTuple_GetItem(args, ${i}$));
        <!--(end)-->
    <!--(end)-->

    // c function call
    <!--(if func.method_return_type)-->
    ${func.method_return_type.c_type}$ ret =
    <!--(end)-->
    <!--(if num_params == 0)-->
    ${func.full_c_method_name}$(self->obj);
    <!--(else)-->
    ${func.full_c_method_name}$(self->obj
        <!--(for i, param in enumerate(func.parameters))-->
        ,prm${i+1}$_${param.name}$
        <!--(end)-->
    );
    <!--(end)-->

    // return
    <!--(if func.method_return_type)-->
    return ${TYPE_OUT_FUNC(type=func.method_return_type)}$(ret);
    <!--(else)-->
    Py_RETURN_NONE;
    <!--(end)-->
}

  <!--(end)-->
<!--(end)-->

/* Class methods table */
static PyMethodDef ${CLS_OBJECT}$_methods[] = {
    <!--(for func in cls.methods)-->
      <!--(if func.method_scope != Eolian_Object_Scope.PROTECTED and not func.full_c_method_name in excludes)-->
    {"${func.name}$", (PyCFunction)${CLS_OBJECT}$_${func.name}$,
        <!--(if len(list(func.parameters)) == 0)-->
        METH_NOARGS, NULL},
        <!--(elif len(list(func.parameters)) == 1)-->
        METH_O, NULL},
        <!--(else)-->
        METH_VARARGS, NULL},
        <!--(end)-->
      <!--(end)-->
    <!--(end)-->
    {NULL, NULL, 0, NULL}  /* sentinel */
};


/* Class Getters */
<!--(for func in cls.properties)-->
    <!--(if func.prop_readable and func.full_c_getter_name not in excludes)-->
${setvar("num_values", "len(list(func.getter_values))")}$#!
static PyObject *  // ${cls.full_name}$ ${func.name}$  (getter)
${CLS_OBJECT}$_${func.name}$_get(PyEfl_Object *self, void *closure)
{
        <!--(if func.getter_return_type)-->
    // single (returned) return_type
    ${func.getter_return_type.c_type}$ val;
    val = ${func.full_c_getter_name}$(self->obj);
    return ${TYPE_OUT_FUNC(type=func.getter_return_type)}$(val);
        <!--(elif num_values == 1)-->
    // single (returned) value
            <!--(for val in func.getter_values)-->
    ${val.type.c_type}$ val;
    val = ${func.full_c_getter_name}$(self->obj);
    return ${TYPE_OUT_FUNC(type=val.type)}$(val);
            <!--(end)-->
        <!--(else)-->
    // multiple values (by ref)
    PyObject* ret;
            <!--(for i, val in enumerate(func.getter_values, 1))-->
    ${val.type.c_type}$ val${i}$_${val.name}$;
            <!--(end)-->

    ${func.full_c_getter_name}$(self->obj
            <!--(for i, val in enumerate(func.getter_values, 1))-->
        ,&val${i}$_${val.name}$
            <!--(end)-->
    );

    // return a named tuple (StructSequence type lazy inited)
    static PyTypeObject ResultType = {0};
    static PyStructSequence_Field namedtuple_fields[] = {
            <!--(for val in func.getter_values)-->
        {"${val.name}$", NULL},
            <!--(end)-->
        {NULL}
    };
    static PyStructSequence_Desc namedtuple_desc = {
        "return type", NULL, namedtuple_fields, ${num_values}$
    };
    if (ResultType.tp_name == 0)
        PyStructSequence_InitType(&ResultType, &namedtuple_desc);

    ret = PyStructSequence_New(&ResultType);
            <!--(for i, val in enumerate(func.getter_values, 1))-->
    PyStructSequence_SetItem(ret, ${i-1}$, ${TYPE_OUT_FUNC(type=val.type)}$(val${i}$_${val.name}$));
            <!--(end)-->
    return ret;
        <!--(end)-->
}

    <!--(end)-->
<!--(end)-->

/* Class Setters */
<!--(for func in cls.properties)-->
    <!--(if func.prop_writable and func.full_c_setter_name not in excludes)-->
${setvar("num_values", "len(list(func.setter_values))")}$#!
static int  // ${cls.full_name}$ ${func.name}$  (setter)
${CLS_OBJECT}$_${func.name}$_set(PyEfl_Object *self, PyObject *value, void *closure)
{
        <!--(if num_values == 1)-->
            <!--(for param in func.setter_values)-->
    ${param.type.c_type}$ val1_${param.name}$ = ${TYPE_IN_FUNC(type=param.type)}$(value);
            <!--(end)-->
        <!--(else)-->
    if (!PyTuple_Check(value))
    {
        PyErr_SetString(PyExc_TypeError, "property value must be a tuple");
        return -1;
    }
    if (PyTuple_GET_SIZE(value) != ${num_values}$)
    {
        PyErr_SetString(PyExc_TypeError, "property value must be a ${num_values}$ items tuple");
        return -1;
    }
            <!--(for i, param in enumerate(func.setter_values))-->
    ${param.type.c_type}$ val${i+1}$_${param.name}$ = ${TYPE_IN_FUNC(type=param.type)}$(PyTuple_GET_ITEM(value, ${i}$));
            <!--(end)-->
        <!--(end)-->

    ${func.full_c_setter_name}$(self->obj
            <!--(for i, param in enumerate(func.setter_values))-->
        ,val${i+1}$_${param.name}$
            <!--(end)-->
    );

    return 0;
}

    <!--(end)-->
<!--(end)-->

/* Class getsetter table */
static PyGetSetDef ${CLS_OBJECT}$_getsetters[] = {
    <!--(for func in cls.properties)-->
    {"${func.name}$",
        <!--(if func.prop_readable and func.full_c_getter_name not in excludes)-->
        (getter)${CLS_OBJECT}$_${func.name}$_get,
        <!--(else)-->
        NULL, /* writeonly */
        <!--(end)-->
        <!--(if func.prop_writable and func.full_c_setter_name not in excludes)-->
        (setter)${CLS_OBJECT}$_${func.name}$_set,
        <!--(else)-->
        NULL, /* readonly */
        <!--(end)-->
        NULL, NULL},
    <!--(end)-->
    {NULL, 0, 0, NULL, NULL}  /* sentinel */
};


/* Object Type definition */
PyTypeObject ${CLS_OBJECT_TYPE}$Internal = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "${CLS_TP_NAME}$",          /*tp_name*/
    sizeof(${CLS_OBJECT}$),     /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    // (destructor)${CLS_OBJECT}$_dealloc,
    0, /* only efl.Object */    /*tp_dealloc*/ 

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
PyTypeObject *${CLS_OBJECT_TYPE}$ = &${CLS_OBJECT_TYPE}$Internal;


/* Class events (including inherited ones) */
const Efl_Event_Description *${CLS_OBJECT}$Events[] = {
<!--(for event in cls.events)-->
    ${event.c_name}$,
<!--(end)-->
<!--(for cls2 in cls.inherits_full)-->
    <!--(for event in cls2.events)-->
    /* from ${cls2.full_name}$ */ ${event.c_name}$,
    <!--(end)-->
<!--(end)-->
    NULL  /* sentinel */
};


Eina_Bool
${OBJECT_FINALIZE_FUNC}$(PyObject *module)
{
    DBG("finalize");

<!--(if len(list(cls.namespaces)) != 1)-->
    /* Import the Efl namespace C API (pyefl_* and types in the efl namespace) */
    if (import_efl() < 0)
        return EINA_FALSE;
    /* TODO: import the namespace of the parent class */
<!--(end)-->

    /* Finalize the object type */
    ${CLS_OBJECT_TYPE}$->tp_new = PyType_GenericNew;
    ${CLS_OBJECT_TYPE}$->tp_base = ${CLS_BASE_OBJECT}$Type;
    if (PyType_Ready(${CLS_OBJECT_TYPE}$) < 0)
        return EINA_FALSE;

    /* Put the object in the calling module namespace */
    PyModule_AddObject(module, "_${cls.name}$", (PyObject *)${CLS_OBJECT_TYPE}$);
    Py_INCREF(${CLS_OBJECT_TYPE}$);

<!--(if cls.type == Eolian_Class_Type.REGULAR)-->
    /* Link the EO class with the python type object */
    pyefl_class_register(${CLS_EO_NAME}$,
                         ${CLS_OBJECT_TYPE}$,
                         ${CLS_OBJECT}$Events);
<!--(end)-->

    return EINA_TRUE;
}

