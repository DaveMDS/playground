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
                                 const PyTypeObject *type);
void        pyefl_event_register(PyEfl_Object *self,
                                 const Efl_Event_Description *desc);
PyObject*   pyefl_object_from_instance(Efl_Object *obj);


#ifdef __cplusplus
}
#endif

#endif /* Py_EO_UTILS__H */
