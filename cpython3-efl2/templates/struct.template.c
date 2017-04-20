<!--(include)-->copyright_c.include<!--(end)-->
<!--(include)-->macros.include<!--(end)-->
#!  fake cls name to reuse some class macro
${setvar("cls", "struct")}$ #!

#include <Python.h>


#include <Efl.h>
#include <Eina.h>
#include <Eo.h>
#include <Ecore.h>
#include <Evas.h>
#include <Elementary.h>


#include "${cls.full_name.lower()}$.h"

// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);

///////////////////////////////////////////////////////////////////////////////
//  The ${cls.full_name}$ Struct
///////////////////////////////////////////////////////////////////////////////

/* Class __init__ method (constructor) */
static int
${CLS_OBJECT}$_init(${CLS_OBJECT}$ *self, PyObject *args, PyObject *kwds)
{
    self->obj = NULL;
    return 0;

}

static void
${CLS_OBJECT}$_dealloc(${CLS_OBJECT}$ *self)
{
    DBG("dealloc()")
    // Py_XDECREF(self->x_attr);  // TODO REMOVE ME
    // Py_TYPE(self)->tp_free((PyObject*)self);
}
/* Struct Fields Getters */
<!--(for field in struct.struct_fields)-->
static PyObject *  // ${struct.full_name}$ ${field.name}$  (getter)
${CLS_OBJECT}$_${field.name}$_get(${CLS_OBJECT}$ *self, void *closure)
{
    return ${TYPE_OUT_FUNC(type=field.type)}$(self->obj->${field.name}$);
}

<!--(end)-->

/* Struct Fields Setters */
<!--(for field in struct.struct_fields)-->
static PyObject *  // ${struct.full_name}$ ${field.name}$  (setter)
${CLS_OBJECT}$_${field.name}$_set(${CLS_OBJECT}$ *self, PyObject *value, void *closure)
{
    self->obj->${field.name}$ = ${TYPE_IN_FUNC(type=field.type)}$(value);
    return 0;
}

<!--(end)-->


/* Class getsetter table */
static PyGetSetDef ${CLS_OBJECT}$_getsetters[] = {
    <!--(for field in struct.struct_fields)-->
    {"${field.name}$",
        (getter)${CLS_OBJECT}$_${field.name}$_get,
        (setter)${CLS_OBJECT}$_${field.name}$_set,
        NULL, NULL},
    <!--(end)-->
    {NULL, 0, 0, NULL, NULL}  /* sentinel */
};

/* Object Type definition */
PyTypeObject ${CLS_OBJECT_TYPE}$Internal = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "${STRUCT_TP_NAME}$",       /*tp_name*/
    sizeof(${CLS_OBJECT}$),     /*tp_basicsize*/
    0,                          /*tp_itemsize*/
    (destructor)${CLS_OBJECT}$_dealloc,
    0, /* only efl.Object */    /*tp_dealloc*/ 

    0,                          /*tp_print*/
    0,                          /*tp_getattr*/
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
    Py_TPFLAGS_DEFAULT          /*tp_flags*/
    0,                          /*tp_doc*/
    0,                          /*tp_traverse*/
    0,                          /*tp_clear*/
    0,                          /*tp_richcompare*/
    0,                          /*tp_weaklistoffset*/
    0,                          /*tp_iter*/
    0,                          /*tp_iternext*/
    // ${CLS_OBJECT}$_methods,     /*tp_methods*/
    0,                          /*tp_methods*/
    0,                          /*tp_members*/
    ${CLS_OBJECT}$_getsetters,  /*tp_getset*/
    0,                          /*tp_base*/
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


Eina_Bool
${OBJECT_FINALIZE_FUNC}$(PyObject *module)
{
    DBG("finalize");

    /* Finalize the object type */
    ${CLS_OBJECT_TYPE}$->tp_new = PyType_GenericNew;
    if (PyType_Ready(${CLS_OBJECT_TYPE}$) < 0)
        return EINA_FALSE;

    /* Put the object in the calling module namespace */
    PyModule_AddObject(module, "${cls.name}$", (PyObject *)${CLS_OBJECT_TYPE}$);
    Py_INCREF(${CLS_OBJECT_TYPE}$);

    return EINA_TRUE;
}
