#ifndef Py_EFL_OBJECT__H
#define Py_EFL_OBJECT__H
#ifdef __cplusplus
extern "C" {
#endif


#include <Eo.h>


/* The object type */
extern PyTypeObject  PyEfl_ObjectTypeInternal;
extern PyTypeObject *PyEfl_ObjectType;
#define PyEfl_Object_Check(v) (Py_TYPE(v) == PyEfl_ObjectType)

typedef struct {
    PyObject_HEAD
    PyObject            *x_attr;        /* just a demo dictionary */
    Eo *obj;
    Eina_List *cbdatas;     /* content: cbdata_t pointers  */
} PyEfl_Object;

Eina_Bool pyefl_object_object_finalize(PyObject *module);


#ifdef __cplusplus
}
#endif

#endif /* Py_EFL_OBJECT__H */
