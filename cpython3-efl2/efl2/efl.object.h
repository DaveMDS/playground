

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
    Eina_List *cbdatas;     /* content: cbdata_t pointers  */
    Eina_List *events;      /* content: Efl_Event_Description pointers */
    /* TODO FIX events should be at class level, not per instance! */
} Efl_ObjectObject;


/* C API for usage by other modules */
typedef struct {
    // Exported types
    PyTypeObject *Efl_ObjectType;
    // Exported functions
    void (*_eo_class_register)(const Efl_Class *, const PyTypeObject *type);
    void (*_eo_event_register)(Efl_ObjectObject *self, const Efl_Event_Description *desc);
    PyObject* (*_eo_object_from_instance)(Efl_Object *obj);
} EflObject_CAPI_t;


/******************************************************************************/
/***** This section is used ONLY in modules that use efl.object.c API *********/
/******************************************************************************/
#ifndef INSIDE_EFL_OBJECT_MODULE

static EflObject_CAPI_t *_EflObject_CAPI;

/* Return -1 on error, 0 on success.
 * PyCapsule_Import will set an exception if there's an error.
 */
static int
import_efl(void)
{
    _EflObject_CAPI = PyCapsule_Import(EflObject_CAPSULE_NAME, 0); // TODO 0 or 1 ??
    return (_EflObject_CAPI != NULL) ? 0 : -1;
}

// defines for faster access in modules
#define Efl_ObjectType _EflObject_CAPI->Efl_ObjectType
#define _eo_class_register _EflObject_CAPI->_eo_class_register
#define _eo_event_register _EflObject_CAPI->_eo_event_register
#define _eo_object_from_instance _EflObject_CAPI->_eo_object_from_instance


#endif /* !EFL_OBJECT_MODULE */
/******************************************************************************/

#ifdef __cplusplus
}
#endif
#endif /* !Py__EFL_OBJECT_H */
