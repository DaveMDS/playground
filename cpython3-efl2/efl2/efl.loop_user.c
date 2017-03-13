#include <Python.h>


#include <Eo.h>
#include <Efl.h>
#include <Ecore.h> // EFL_LOOP_USER_CLASS is defined here

#include "eo_utils.h"
#include "efl.object.h"
#include "efl.loop_user.h"


// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);


static int
Efl_Loop_User_init(PyEfl_Loop_User *self, PyObject *args, PyObject *kwds)
{
    DBG("init()")

    Eo *o;
    o  = efl_add(EFL_LOOP_USER_CLASS, NULL);
    ((PyEfl_Object*)self)->obj = o;

    /* Call the base class __init__ func */
    if (PyEfl_ObjectType.tp_init((PyObject *)self, args, kwds) < 0)
        return -1;

    return 0;
}

static void
Efl_Loop_User_dealloc(PyEfl_Loop_User *self)
{
    DBG("dealloc()")
    // Py_XDECREF(self->x_attr);
    PyObject_Del(self);
}

static PyObject *  // Efl.Loop_User.loop (getter)
Efl_Loop_User_loop_get(PyEfl_Loop_User *self, void *closure)
{
    Efl_Loop *loop;
    loop = efl_loop_get(self->base.obj);
    return pyefl_object_from_instance(loop);
}

/* Functions table for Efl.Loop_User class */
static PyMethodDef Efl_Loop_User_methods[] = {
    {NULL, NULL, 0, NULL}  /* sentinel */
};

/* Properties table for Efl.Loop_User class */
static PyGetSetDef EFL_Loop_User_getsetters[] = {
    {"loop",
        (getter)Efl_Loop_User_loop_get,
        NULL, /* readonly */
        NULL, NULL},
    {NULL, 0, 0, NULL, NULL}  /* sentinel */
};

PyTypeObject PyEfl_Loop_UserType = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "_loop_user._Loop_User",    /*tp_name*/
    sizeof(PyEfl_Loop_User),    /*tp_basicsize*/
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
    Efl_Loop_User_methods,      /*tp_methods*/
    0,                          /*tp_members*/
    EFL_Loop_User_getsetters,   /*tp_getset*/
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

Eina_Bool
pyefl_loop_user_object_finalize(PyObject *module)
{
    DBG("pyefl_init");

    PyEfl_Loop_UserType.tp_new = PyType_GenericNew;
    PyEfl_Loop_UserType.tp_base = &PyEfl_ObjectType;
    if (PyType_Ready(&PyEfl_Loop_UserType) < 0)
        return EINA_FALSE;
        
    PyModule_AddObject(module, "_Loop_User", (PyObject *)&PyEfl_Loop_UserType);
    Py_INCREF(&PyEfl_Loop_UserType);

    pyefl_class_register(EFL_LOOP_USER_CLASS, &PyEfl_Loop_UserType);

    return EINA_TRUE;
}

