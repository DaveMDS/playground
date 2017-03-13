#include <Python.h>

#include <Eina.h>
#include <Eo.h>
#include <Efl.h>
#include <Ecore.h>

#include "eo_utils.h"
#include "efl.object.h"

// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);


///////////////////////////////////////////////////////////////////////////////
////  Conversion functions  ///////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
// static void
// _eo_class_register(const Efl_Class *cls, const PyTypeObject *type)
// {
    // DBG("register class: '%s'%p with type: %s", efl_class_name_get(cls),cls, type->tp_name);
    // if (!eina_hash_direct_add(_eo_class_map, efl_class_name_get(cls), type))
        // DBG("ERROR: cannot register class");
// }




///////////////////////////////////////////////////////////////////////////////
////  Event callbacks and cbdata handling  ////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

struct cb_data_t {
    PyObject *cb;    // The user callback
    PyObject *kargs; // User kargs to pass back in cb
};

static struct cb_data_t *
_eo_cbdata_new(PyObject *cb, PyObject *kargs)
{
    struct cb_data_t *cbdata;

    cbdata = malloc(sizeof(struct cb_data_t));
    if (!cbdata || !cb) return NULL;

    cbdata->cb = cb; 
    cbdata->kargs = kargs; 

    Py_INCREF(cb);
    Py_XINCREF(kargs);

    return cbdata;
}

static void
_eo_cbdata_free(struct cb_data_t *cbdata)
{
    Py_DECREF(cbdata->cb);
    Py_XDECREF(cbdata->kargs);
    free(cbdata);
}

static void /* with GIL (NOT SURE) */
_eo_callback_dispatcher(void *data, const Efl_Event *event)
{
    struct cb_data_t *cbdata = data;

    /* Acquire the GIL */
    PyGILState_STATE _gil_state = PyGILState_Ensure();

    DBG("_callback_dispatcher for event: '%s'", event->desc->name)

    PyObject *obj;
    obj = pyefl_object_from_instance(event->object);
    
    // Build python args for the callback
    // FIXME: callback signature: (obj, event_name, event_info, **kargs)
    PyObject *arglist;
    arglist = Py_BuildValue("(OsO)", obj, event->desc->name, Py_None);

    // Call the user python callback
    PyObject *result;
    result = PyObject_Call(cbdata->cb, arglist, cbdata->kargs);
    Py_DECREF(arglist);
    Py_XDECREF(result);

    /* Propagate exceptions raised inside the callback */
    if (PyErr_Occurred()) {
        PyErr_PrintEx(0);
    }

    /* Release the GIL */
    PyGILState_Release(_gil_state);
}

// static void
// _eo_event_register(PyEfl_Object *self, const Efl_Event_Description *desc)
// {
    // DBG("register event: %s", desc->name);
    // self->events = eina_list_append(self->events, desc);
// }

static const Efl_Event_Description *
_eo_event_find_by_name(PyEfl_Object *self, const char *event_name)
{
    const Efl_Event_Description *event_desc;
    Eina_List *l;

    EINA_LIST_FOREACH(self->events, l, event_desc)
        if (strcmp(event_desc->name, event_name) == 0)
            break;
    if (l == NULL) {
        PyErr_SetString(PyExc_TypeError, "event name cannot be found");
        return NULL;
    }
    return event_desc;
}

///////////////////////////////////////////////////////////////////////////////
////  The Efl.Object OBJECT  //////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////

static void /* with GIL (NOT SURE) */
_eo_del_callback(void *data, const Efl_Event *event)
{
    PyEfl_Object *self = data;

    /* Acquire the GIL */
    // PyGILState_STATE _gil_state = PyGILState_Ensure();

    DBG("DEL EVENT")

    // TODO need to call the del callbacks in python here ???

    // Free all cb datas ad unref it's content
    struct cb_data_t *d;
    EINA_LIST_FREE(self->cbdatas,d)
        _eo_cbdata_free(d);
    self->cbdatas = NULL;

    // Free the list of event descriptions
    eina_list_free(self->events);
    self->events = NULL;

    // Invalidate the efl object reference
    Py_DECREF(self);
    self->obj = NULL;

    /* Release the GIL */
    // PyGILState_Release(_gil_state);
}

static int
Efl_Object_init(PyEfl_Object *self, PyObject *args, PyObject *kwds)
{
    DBG("init()")

    efl_key_data_set(self->obj, PY_EO_DATA_KEY, self);
    Py_INCREF(self);

    // Keep track of the efl object lifetime (after user del cbs has been called)
    efl_event_callback_priority_add(self->obj, EFL_EVENT_DEL,
                                    EFL_CALLBACK_PRIORITY_AFTER + 9999,
                                    _eo_del_callback, self);
    
    return 0;
}


static void
Efl_Object_dealloc(PyEfl_Object *self)
{
    DBG("dealloc()")
    Py_XDECREF(self->x_attr);
    PyObject_Del(self);
}

static int
Efl_Object_traverse(PyEfl_Object *self, visitproc visit, void *arg)
{
    DBG("traverse()")
    Py_VISIT(self->x_attr);
    return 0;
}


// static int
// Efl_Object_finalize(PyEfl_Object *self)
// {
    // Py_CLEAR(self->x_attr);
    // return 0;
// }


static PyObject *  // Efl.Object.event_callback_add()
Efl_Object_event_callback_add(PyEfl_Object *self, PyObject *args, PyObject *kargs)
{
    DBG("event_callback_add()")

    // Fetch python args (str event_name, callable cb, **kargs)
    const char *event_name;
    PyObject *cb;
    if (!PyArg_ParseTuple(args, "sO:event_callback_add", &event_name, &cb))
        return  NULL;
    if (!PyCallable_Check(cb)) {
        PyErr_SetString(PyExc_TypeError, "parameter must be callable");
        return NULL;
    }

    // Event name -> event desc
    const Efl_Event_Description *event_desc;
    event_desc = _eo_event_find_by_name(self, event_name);
    if (!event_desc) return NULL;

    // Prepare the data that will be attached with the cb
    struct cb_data_t *cbdata;
    cbdata = _eo_cbdata_new(cb, kargs);

    // Actually call the C EFL function
    if (efl_event_callback_add(self->obj, event_desc,
                              _eo_callback_dispatcher, cbdata) == EINA_FALSE) {
        PyErr_SetString(PyExc_TypeError, "Unknown error while attaching callback");
        _eo_cbdata_free(cbdata);
        return NULL;
    }

    // Keep a list of reffed data, we will unref on del or callback_del
    self->cbdatas = eina_list_append(self->cbdatas, cbdata);

    Py_RETURN_NONE;
}

static PyObject *  // Efl.Object.event_callback_del()
Efl_Object_event_callback_del(PyEfl_Object *self, PyObject *args, PyObject *kargs)
{
    DBG("event_callback_del()")

    // Fetch python args (str event_name, callable cb, **kargs)
    const char *event_name;
    PyObject *cb;
    if (!PyArg_ParseTuple(args, "sO:Efl_Object_event_callback_del", &event_name, &cb))
        return  NULL;

    // Search a matching cbdata in our list of connected cbs
    struct cb_data_t *cbdata = NULL;
    Eina_List *l;
    EINA_LIST_FOREACH(self->cbdatas, l, cbdata)
    {
        if ((cbdata->cb == cb) &&
            (PyObject_RichCompareBool(cbdata->kargs, kargs, Py_EQ)))
        {
            self->cbdatas = eina_list_remove_list(self->cbdatas, l);
            break;
        }
    }
    if (l == NULL)
    {
        PyErr_SetString(PyExc_TypeError, "cannot find a matching callback");
        return NULL;
    }

    // Event name -> event desc
    const Efl_Event_Description *event_desc;
    event_desc = _eo_event_find_by_name(self, event_name);
    if (!event_desc) return NULL;

    efl_event_callback_del(self->obj, event_desc, _eo_callback_dispatcher, cbdata);

    // Free data ad unref it's content
    _eo_cbdata_free(cbdata);

    Py_RETURN_NONE;
}


static PyObject *  // Efl.Object.delete()
Efl_Object_delete(PyEfl_Object *self, PyObject *args)
{
    DBG("delete()")
    efl_del(self->obj);
    Py_RETURN_NONE;
}

static PyObject *  // Efl.Object.parent_get()
Efl_Object_parent_get(PyEfl_Object *self, PyObject *args)
{
    DBG("parent_get()")
    Efl_Object *obj;
    PyObject *ret;

    obj = efl_parent_get(self->obj);
    ret = pyefl_object_from_instance(obj);

    return ret;
    
}

/* List of functions defined in the object */
static PyMethodDef Efl_Object_methods[] = {
    {"delete", (PyCFunction)Efl_Object_delete,
        METH_NOARGS, NULL},
    {"event_callback_add", (PyCFunction)Efl_Object_event_callback_add,
        METH_VARARGS | METH_KEYWORDS, NULL},
    {"event_callback_del", (PyCFunction)Efl_Object_event_callback_del,
        METH_VARARGS | METH_KEYWORDS, NULL},
    {"parent_get", (PyCFunction)Efl_Object_parent_get,
        METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}  /* sentinel */
};

PyTypeObject PyEfl_ObjectType = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "_Object",                  /*tp_name*/
    sizeof(PyEfl_Object),       /*tp_basicsize*/
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

Eina_Bool
pyefl_object_object_finalize(PyObject *module)
{
    DBG("pyefl_init");

    PyEfl_ObjectType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&PyEfl_ObjectType) < 0)
        return EINA_FALSE;

    PyModule_AddObject(module, "_Object", (PyObject *)&PyEfl_ObjectType);
    Py_INCREF(&PyEfl_ObjectType);

    return EINA_TRUE;
}

/* C API table - always add new things to the end for binary compatibility. */
// static EflObject_CAPI_t EflObjectCAPI = {
    // &Efl_ObjectType,
    // &_eo_class_register,
    // &_eo_event_register,
    // &_eo_object_from_instance
// };

