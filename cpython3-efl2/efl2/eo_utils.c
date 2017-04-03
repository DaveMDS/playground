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
static Eina_Hash *_pyefl_class_map = NULL;  // Cls name -> PyTypeObject *
static Eina_Hash *_pyefl_type_map = NULL;   // Cls name -> Efl_Class *
static Eina_Hash *_pyefl_event_map = NULL;  // Cls name -> Efl_Event_Description **

void
pyefl_class_register(const Efl_Class *cls, const PyTypeObject *type,
                     const Efl_Event_Description **events)
{
    DBG("register class: '%s'%p with type: %s", efl_class_name_get(cls),cls, type->tp_name);
    // The "class name" => PyTypeObject* hash map
    if (_pyefl_class_map == NULL)
    {
        _pyefl_class_map = eina_hash_string_superfast_new(NULL);
        if (!_pyefl_class_map) return;
    }
    if (!eina_hash_direct_add(_pyefl_class_map, efl_class_name_get(cls), type))
        DBG("ERROR: cannot register class");

    // The "type name" => Efl_Class* hash map
    if (_pyefl_type_map == NULL)
    {
        _pyefl_type_map = eina_hash_string_superfast_new(NULL);
        if (!_pyefl_type_map) return;
    }
    if (!eina_hash_direct_add(_pyefl_type_map, type->tp_name, cls))
        DBG("ERROR: cannot register type");

    // The "class name" => Efl_Event_Description ** hash map
    if (events && _pyefl_event_map == NULL)
    {
        _pyefl_event_map = eina_hash_string_superfast_new(NULL);
        if (!_pyefl_event_map) return;
    }
    if (events && !eina_hash_direct_add(_pyefl_event_map, efl_class_name_get(cls), events))
        DBG("ERROR: cannot register class events");
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

const Efl_Event_Description *
pyefl_event_find_by_name(PyEfl_Object *obj, const char *event_name)
{
    const Efl_Event_Description **events;
    int i = 0;

    // Get the efl class
    const Efl_Class *cls = efl_class_get(obj->obj);
    if (!cls)
    {
        DBG("ERROR: cannot get class from object")
        return NULL;
    }
    DBG("class: '%s'%p", efl_class_name_get(cls), cls);

    // Find the registered array of events for this class
    events = eina_hash_find(_pyefl_event_map, efl_class_name_get(cls));
    if (!events)
        return NULL;

    // Search the event in the array
    while (events[i])
    {
        if (!strcmp(events[i]->name, event_name))
            return events[i];
        i++;
    }

    return NULL;
}

