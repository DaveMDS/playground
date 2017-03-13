#ifndef Py_EFL_OBJECT__H
#define Py_EFL_OBJECT__H
#ifdef __cplusplus
extern "C" {
#endif


#include <Eo.h>


/* The object type */
extern PyTypeObject PyEfl_ObjectType;
#define Efl_Object_Check(v) (Py_TYPE(v) == Efl_ObjectType)

typedef struct {
    PyObject_HEAD
    PyObject            *x_attr;        /* just a demo dictionary */
    Eo *obj;
    Eina_List *cbdatas;     /* content: cbdata_t pointers  */
    Eina_List *events;      /* content: Efl_Event_Description pointers */
    /* TODO FIX events should be at class level, not per instance! */
} PyEfl_Object;

Eina_Bool pyefl_object_object_finalize(PyObject *module);


#ifdef __cplusplus
}
#endif

#endif /* Py_EFL_OBJECT__H */
