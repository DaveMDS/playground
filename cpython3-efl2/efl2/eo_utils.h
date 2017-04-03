#ifndef Py_EO_UTILS__H
#define Py_EO_UTILS__H
#ifdef __cplusplus
extern "C" {
#endif

// #include <Python.h>

// #include <Eina.h>
// #include <Eo.h>
// #include <Efl.h>
// #include <Ecore.h>

#include "efl.object.h"

#define PY_EO_DATA_KEY "_py_eo_"

void        pyefl_class_register(const Efl_Class *cls,
                                 const PyTypeObject *type,
                                 const Efl_Event_Description **events);

#define           pyefl_object_to_pointer(__PYOBJ__) ((PyEfl_Object *)__PYOBJ__)->obj
PyObject*         pyefl_object_from_instance(Efl_Object *obj);
const Efl_Class*  pyefl_type_to_class(PyObject *type_object);

const Efl_Event_Description *pyefl_event_find_by_name(PyEfl_Object *obj, const char *event_name);

#ifdef __cplusplus
}
#endif

#endif /* Py_EO_UTILS__H */
