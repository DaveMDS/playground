

#include <Eo.h>

#ifndef Py__EFL_OBJECT_H
#define Py__EFL_OBJECT_H
#ifdef __cplusplus
extern "C" {
#endif


/* Python module and C API name */
#define EflObject_MODULE_NAME "efl2._object"
#define EflObject_CAPI_NAME "CAPI"
#define EflObject_CAPSULE_NAME "efl2._object.CAPI"


typedef struct {
    PyObject_HEAD
    PyObject            *x_attr;        /* just a demo dictionary */
    Eo *obj;
} Efl_ObjectObject;


/* C API for usage by other modules */
typedef struct {
    PyTypeObject *Efl_ObjectType;
    // PyObject *error;
    // PyObject *timeout_error;
} EflObject_CAPIObject;


#define EflObject_ImportModuleAndAPI() PyCapsule_Import(EflObject_CAPSULE_NAME, 1)


#ifdef __cplusplus
}
#endif
#endif /* !Py__EFL_OBJECT_H */
