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
    PyObject *arglist;
    if (event->info) {
        // callback signature: (obj, event_name, event_info, **kargs)
        // TODO convert event->info to python
        arglist = Py_BuildValue("(OsO)", obj, event->desc->name, Py_None);
    } else {
        // callback signature: (obj, event_name, **kargs)
        arglist = Py_BuildValue("(Os)", obj, event->desc->name);
    }

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
    Py_XDECREF(self->x_attr);  // TODO REMOVE ME
    Py_TYPE(self)->tp_free((PyObject*)self);
}

static int
Efl_Object_traverse(PyEfl_Object *self, visitproc visit, void *arg)
{
    DBG("traverse()")
    Py_VISIT(self->x_attr);  // TODO REMOVE ME
    return 0;
}


// static int
// Efl_Object_finalize(PyEfl_Object *self)
// {
    // Py_CLEAR(self->x_attr);
    // return 0;
// }


/* Class methods */

static PyObject *  // Efl.Object event_callback_add()
Efl_Object_event_callback_add(PyEfl_Object *self, PyObject *args, PyObject *kargs)
{
    DBG("event_callback_add()")

    // Fetch python args (str event_name, callable cb, **kargs)
    const char *event_name;
    PyObject *cb;
    if (!PyArg_ParseTuple(args, "sO:event_callback_add", &event_name, &cb))
        return  NULL;
    if (!PyCallable_Check(cb))
    {
        PyErr_SetString(PyExc_TypeError, "parameter must be callable");
        return NULL;
    }

    // Event name -> event desc
    const Efl_Event_Description *event_desc;
    event_desc = pyefl_event_find_by_name(self, event_name);
    if (!event_desc)
        return PyErr_Format(PyExc_ValueError,
                            "event '%s' cannot be found for cls '%s'",
                            event_name, efl_class_name_get(efl_class_get(self->obj)));

    // Prepare the data that will be attached with the cb
    struct cb_data_t *cbdata;
    cbdata = _eo_cbdata_new(cb, kargs);

    // Actually call the C EFL function
    if (!efl_event_callback_add(self->obj, event_desc, _eo_callback_dispatcher, cbdata))
    {
        PyErr_SetString(PyExc_TypeError, "Unknown error while attaching callback");
        _eo_cbdata_free(cbdata);
        return NULL;
    }

    // Keep a list of reffed data, we will unref on del or callback_del
    self->cbdatas = eina_list_append(self->cbdatas, cbdata);

    Py_RETURN_NONE;
}

static PyObject *  // Efl.Object event_callback_del()
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
    event_desc = pyefl_event_find_by_name(self, event_name);
    if (!event_desc)
        return PyErr_Format(PyExc_ValueError,
                            "event '%s' cannot be found for cls '%s'",
                            event_name, efl_class_name_get(efl_class_get(self->obj)));

    // Actually call the C EFL function
    if (!efl_event_callback_del(self->obj, event_desc, _eo_callback_dispatcher, cbdata))
    {
        PyErr_SetString(PyExc_TypeError, "Unknown error while removing callback");
        return NULL;
    }

    // Free data ad unref it's content
    _eo_cbdata_free(cbdata);

    Py_RETURN_NONE;
}


static PyObject *  // Efl.Object efl_event_callback_stop()
Efl_Object_event_callback_stop(PyEfl_Object *self, PyObject *args)
{
    DBG("callback_stop()")
    efl_event_callback_stop(self->obj);
    Py_RETURN_NONE;
}

static PyObject *  // Efl.Object event_freeze()
Efl_Object_event_freeze(PyEfl_Object *self, PyObject *args)
{
    DBG("event_freeze()")
    efl_event_freeze(self->obj);
    Py_RETURN_NONE;
}

static PyObject *  // Efl.Object event_thaw()
Efl_Object_event_thaw(PyEfl_Object *self, PyObject *args)
{
    DBG("event_thaw()")
    efl_event_thaw(self->obj);
    Py_RETURN_NONE;
}

static PyObject *  // Efl.Object event_global_freeze()
Efl_Object_event_global_freeze(PyEfl_Object *self, PyObject *args)
{
    DBG("event_global_freeze()")
    efl_event_global_freeze(self->obj);
    Py_RETURN_NONE;
}

static PyObject *  // Efl.Object event_global_thaw()
Efl_Object_event_global_thaw(PyEfl_Object *self, PyObject *args)
{
    DBG("event_global_thaw()")
    efl_event_global_thaw(self->obj);
    Py_RETURN_NONE;
}

static PyObject *  // Efl.Object name_find()
Efl_Object_name_find(PyEfl_Object *self, PyObject *arg)
{
    DBG("name_find()")
    if (!PyUnicode_Check(arg))
    {
        PyErr_SetString(PyExc_TypeError, "name must be a string");
        return NULL;
    }
    const char *name = PyUnicode_AsUTF8(arg);
    Efl_Object *obj = efl_name_find(self->obj, name);
    return pyefl_object_from_instance(obj);
}

static PyObject *  // Efl.Object composite_attach()
Efl_Object_composite_attach(PyEfl_Object *self, PyObject *arg)
{
    DBG("composite_attach()")
    if (!PyObject_TypeCheck(arg, PyEfl_ObjectType))
    {
        PyErr_SetString(PyExc_TypeError, "comp_obj must be an Efl Object");
        return NULL;
    }
    Efl_Object *comp_obj = pyefl_object_to_pointer(arg);
    Eina_Bool ret = efl_composite_attach(self->obj, comp_obj);
    return PyBool_FromLong(ret);
}

static PyObject *  // Efl.Object composite_detach()
Efl_Object_composite_detach(PyEfl_Object *self, PyObject *arg)
{
    DBG("composite_detach()")
    if (!PyObject_TypeCheck(arg, PyEfl_ObjectType))
    {
        PyErr_SetString(PyExc_TypeError, "comp_obj must be an Efl Object");
        return NULL;
    }
    Efl_Object *comp_obj = pyefl_object_to_pointer(arg);
    Eina_Bool ret = efl_composite_detach(self->obj, comp_obj);
    return PyBool_FromLong(ret);
}

static PyObject *  // Efl.Object composite_part_is()
Efl_Object_composite_part_is(PyEfl_Object *self, PyObject *args)
{
    DBG("composite_part_is()")
    Eina_Bool ret = efl_composite_part_is(self->obj);
    return PyBool_FromLong(ret);
}

static PyObject *  // Efl.Object delete()
Efl_Object_delete(PyEfl_Object *self, PyObject *args)
{
    DBG("delete()")
    efl_del(self->obj);
    Py_RETURN_NONE;
}

/* Class methods table */
static PyMethodDef Efl_Object_methods[] = {
    {"delete", (PyCFunction)Efl_Object_delete,
        METH_NOARGS, NULL},
    {"event_callback_add", (PyCFunction)Efl_Object_event_callback_add,
        METH_VARARGS | METH_KEYWORDS, NULL},
    {"event_callback_del", (PyCFunction)Efl_Object_event_callback_del,
        METH_VARARGS | METH_KEYWORDS, NULL},
    {"event_callback_stop", (PyCFunction)Efl_Object_event_callback_stop,
        METH_NOARGS, NULL},
    {"event_freeze", (PyCFunction)Efl_Object_event_freeze,
        METH_NOARGS, NULL},
    {"event_thaw", (PyCFunction)Efl_Object_event_thaw,
        METH_NOARGS, NULL},
    {"event_global_freeze", (PyCFunction)Efl_Object_event_global_freeze,
        METH_NOARGS, NULL},
    {"event_global_thaw", (PyCFunction)Efl_Object_event_global_thaw,
        METH_NOARGS, NULL},
    {"name_find", (PyCFunction)Efl_Object_name_find,
        METH_O, NULL},
    {"composite_attach", (PyCFunction)Efl_Object_composite_attach,
        METH_O, NULL},
    {"composite_detach", (PyCFunction)Efl_Object_composite_detach,
        METH_O, NULL},
    {"composite_part_is", (PyCFunction)Efl_Object_composite_part_is,
        METH_NOARGS, NULL},
    {NULL, NULL, 0, NULL}  /* sentinel */
};


/* Properties */

static PyObject *  // Efl.Object parent  (getter)
PyEfl_Object_parent_get(PyEfl_Object *self, void *closure)
{
    DBG("parent_get")
    Efl_Object *obj = efl_parent_get(self->obj);
    return pyefl_object_from_instance(obj);
}
static int  // (setter)
PyEfl_Object_parent_set(PyEfl_Object *self, PyObject *value, void *closure)
{
    DBG("parent_set")
    if (value != Py_None && !PyObject_TypeCheck(value, PyEfl_ObjectType))
    {
        PyErr_SetString(PyExc_TypeError, "parent must be an Efl Object, or None");
        return -1;
    }
    Efl_Object *parent = pyefl_object_to_pointer(value);
    efl_parent_set(self->obj, parent);
    return 0;
}

static PyObject *  // Efl.Object name  (getter)
PyEfl_Object_name_get(PyEfl_Object *self, void *closure)
{
    DBG("name_get")
    const char *name = efl_name_get(self->obj);
    return PyUnicode_FromStringOrNull(name);
}
static int  // (setter)
PyEfl_Object_name_set(PyEfl_Object *self, PyObject *value, void *closure)
{
    DBG("name_set")
    if (value != Py_None && !PyUnicode_Check(value))
    {
        PyErr_SetString(PyExc_TypeError, "name must be a string, or None");
        return -1;
    }
    const char *name = PyUnicodeOrNone_AsUTF8(value);
    efl_name_set(self->obj, name);
    return 0;
}

static PyObject *  // Efl.Object comment  (getter)
PyEfl_Object_comment_get(PyEfl_Object *self, void *closure)
{
    DBG("comment_get")
    const char *comment = efl_comment_get(self->obj);
    return PyUnicode_FromStringOrNull(comment);
}
static int  // (setter)
PyEfl_Object_comment_set(PyEfl_Object *self, PyObject *value, void *closure)
{
    DBG("comment_set")
    if (value != Py_None && !PyUnicode_Check(value))
    {
        PyErr_SetString(PyExc_TypeError, "comment must be a string, or None");
        return -1;
    }
    const char *comment = PyUnicodeOrNone_AsUTF8(value);
    efl_comment_set(self->obj, comment);
    return 0;
}

static PyObject *  // Efl.Object event_freeze_count  (getter)
PyEfl_Object_event_freeze_count_get(PyEfl_Object *self, void *closure)
{
    DBG("event_freeze_count_get")
    int fcount = efl_event_freeze_count_get(self->obj);
    return PyLong_FromLong(fcount);
}

static PyObject *  // Efl.Object event_global_freeze_count  (getter)
PyEfl_Object_event_global_freeze_count_get(PyEfl_Object *self, void *closure)
{
    DBG("event_global_freeze_count_get")
    int fcount = efl_event_global_freeze_count_get(self->obj);
    return PyLong_FromLong(fcount);
}

/* Class getsetter table */
static PyGetSetDef PyEfl_Object_getsetters[] = {
    {"parent",
        (getter)PyEfl_Object_parent_get,
        (setter)PyEfl_Object_parent_set,
        NULL, NULL},
    {"name",
        (getter)PyEfl_Object_name_get,
        (setter)PyEfl_Object_name_set,
        NULL, NULL},
    {"comment",
        (getter)PyEfl_Object_comment_get,
        (setter)PyEfl_Object_comment_set,
        NULL, NULL},
    {"event_freeze_count",
        (getter)PyEfl_Object_event_freeze_count_get,
        NULL, /* read-only */
        NULL, NULL},
    {"event_global_freeze_count",
        (getter)PyEfl_Object_event_global_freeze_count_get,
        NULL, /* read-only */
        NULL, NULL},
    {NULL, 0, 0, NULL, NULL}  /* sentinel */
};

/* Object Type definition */
PyTypeObject PyEfl_ObjectTypeInternal = {
    /* The ob_type field must be initialized in the module init function
     * to be portable to Windows without using C++. */
    PyVarObject_HEAD_INIT(NULL, 0)
    "efl.Object",               /*tp_name*/
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
    PyEfl_Object_getsetters,    /*tp_getset*/
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
PyTypeObject *PyEfl_ObjectType = &PyEfl_ObjectTypeInternal;


/* Class events (including inherited ones) */
const Efl_Event_Description *PyEfl_ObjectEvents[] = {
    EFL_EVENT_CALLBACK_ADD,
    EFL_EVENT_CALLBACK_DEL,
    EFL_EVENT_DEL,
    NULL  /* sentinel */
};


Eina_Bool
pyefl_object_object_finalize(PyObject *module)
{
    DBG("pyefl_init");

    PyEfl_ObjectType->tp_new = PyType_GenericNew;
    if (PyType_Ready(PyEfl_ObjectType) < 0)
        return EINA_FALSE;

    PyModule_AddObject(module, "Object", (PyObject *)PyEfl_ObjectType);
    Py_INCREF(PyEfl_ObjectType);

    /* Link the EO class with the python type object */
    pyefl_class_register(EFL_OBJECT_CLASS,
                         PyEfl_ObjectType,
                         PyEfl_ObjectEvents);

    return EINA_TRUE;
}
