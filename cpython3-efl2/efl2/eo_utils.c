#include <Python.h>

#include <Eina.h>
#include <Eo.h>
#include <Efl.h>
#include <Ecore.h>

// #include "efl.object.h"
#include "eo_utils.h"


// #define DBG(...) {}
#define DBG(_fmt_, ...) printf("[%s:%d] "_fmt_"\n", __FILE__, __LINE__, ##__VA_ARGS__);


///////////////////////////////////////////////////////////////////////////////
////  Basic Utils ///////// ///////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////
static Eina_Hash *_pyefl_class_map = NULL;
static Eina_Hash *_pyefl_type_map = NULL;

void
pyefl_class_register(const Efl_Class *cls, const PyTypeObject *type)
{
    DBG("register class: '%s'%p with type: %s", efl_class_name_get(cls),cls, type->tp_name);
    // Init the "class name" => PyTypeObject* hash map
    if (_pyefl_class_map == NULL)
    {
        _pyefl_class_map = eina_hash_string_superfast_new(NULL);
        if (!_pyefl_class_map) return;
    }
    // Add the class to the map
    if (!eina_hash_direct_add(_pyefl_class_map, efl_class_name_get(cls), type))
        DBG("ERROR: cannot register class");

    // Init the "type name" => Efl_Class* hash map
    if (_pyefl_type_map == NULL)
    {
        _pyefl_type_map = eina_hash_string_superfast_new(NULL);
        if (!_pyefl_type_map) return;
    }
    // Add the class to the map
    if (!eina_hash_direct_add(_pyefl_type_map, type->tp_name, cls))
        DBG("ERROR: cannot register class");
}

void
pyefl_event_register(PyEfl_Object *self, const Efl_Event_Description *desc)
{
    DBG("register event: %s", desc->name);
    self->events = eina_list_append(self->events, desc);
}

const Efl_Class*
pyefl_type_to_class(PyObject *type_object) {
    
    PyTypeObject *type = (PyTypeObject*)type_object;
    Efl_Class *cls;

    if (!type_object)
        return NULL;

    // Find the registered class using the type name
    cls = eina_hash_find(_pyefl_class_map, type->tp_name);    
    if (!cls)
        DBG("ERROR: cannot find a matching efl class")

    return cls;
}

PyObject*
pyefl_object_from_instance(Efl_Object *obj)
{
    PyObject *ret;

    DBG("_eo_object_from_instance %p", obj);
    if (!obj)
    {
        Py_RETURN_NONE;
    }

    // Search in key data for an existing py instance
    ret = efl_key_data_get(obj, PY_EO_DATA_KEY);
    if (ret)
    {
        DBG("Found an existing Python object instance in key data");
        return ret;
    }

    // Get the efl class
    const Efl_Class *cls = efl_class_get(obj);
    if (!cls)
    {
        DBG("ERROR: cannot get class from object")
        Py_RETURN_NONE;  // or NULL ??
    }
    DBG("class: '%s'%p", efl_class_name_get(cls), cls);

    // Find the registered python object type
    PyTypeObject *type;
    type = eina_hash_find(_pyefl_class_map, efl_class_name_get(cls));
    if (!type)
    {
        DBG("ERROR: cannot find a matching python class")
        Py_RETURN_NONE;  // or NULL ??
    }

    // Create a new object of the correct class
    ret = type->tp_alloc(type, 0);
    if (ret)
    {
        DBG("Created a new object of class: %s from obj: %p", type->tp_name, obj);
        ((PyEfl_Object*)ret)->obj = obj;
        // Call the __init_func in the base class (Efl.Object)
        PyEfl_ObjectType->tp_init(ret, NULL, NULL);
        // TODO need to INCREF ret ??
        return ret;
    }

    DBG("ERROR: cannot convert Efl_Object* object to python") 
    Py_RETURN_NONE;  // or NULL ??
}
