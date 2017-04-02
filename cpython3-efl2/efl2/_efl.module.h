#ifndef Py_EFL_MODULE__H
#define Py_EFL_MODULE__H
#ifdef __cplusplus
extern "C" {
#endif

#include <Eo.h>

#include "eo_utils.h"
#include "efl.object.h"
#include "efl.loop.h"
#include "efl.loop_user.h"
#include "efl.animator.h"
#include "efl.config.h"
#include "efl.part.h"



/* Python module and C API name */
#define PyEFL_CAPSULE_NAME "efl2._efl.CAPI"



/* C API for usage by other modules */
typedef struct {
    // Exported types
    PyTypeObject *PyEfl_ObjectType;
    PyTypeObject *PyEfl_LoopType;
    PyTypeObject *PyEfl_Loop_UserType;
    PyTypeObject *PyEfl_AnimatorType;
    PyTypeObject *PyEfl_ConfigType;
    PyTypeObject *PyEfl_PartType;
    // Exported functions
    void (*pyefl_class_register)(const Efl_Class *, const PyTypeObject *type);
    void (*pyefl_event_register)(PyEfl_Object *self, const Efl_Event_Description *desc);
    PyObject* (*pyefl_object_from_instance)(Efl_Object *obj);
} PyEfl_CAPI_t;


/*****************************************************************************/
/***** This section is used ONLY from the efl namespace (same .so file) ******/
#ifdef INSIDE_EFL_MODULE
/*****************************************************************************/
// void pyefl_class_register(const Efl_Class *cls, const PyTypeObject *type);


/*****************************************************************************/
/***** This section is used ONLY in modules that use efl.object.c API ********/
#else
/*****************************************************************************/

static PyEfl_CAPI_t *_EflObject_CAPI;

/* Return -1 on error, 0 on success.
 * PyCapsule_Import will set an exception if there's an error.
 */
static int
import_efl(void)
{
    _EflObject_CAPI = PyCapsule_Import(PyEFL_CAPSULE_NAME, 0); // TODO 0 or 1 ??
    return (_EflObject_CAPI != NULL) ? 0 : -1;
}

// defines for faster access in modules
#define PyEfl_ObjectType _EflObject_CAPI->PyEfl_ObjectType
#define PyEfl_LoopType _EflObject_CAPI->PyEfl_LoopType
#define PyEfl_Loop_UserType _EflObject_CAPI->PyEfl_Loop_UserType
#define PyEfl_AnimatorType _EflObject_CAPI->PyEfl_AnimatorType
#define PyEfl_ConfigType _EflObject_CAPI->PyEfl_ConfigType
#define PyEfl_PartType _EflObject_CAPI->PyEfl_PartType
#define pyefl_class_register _EflObject_CAPI->pyefl_class_register
#define pyefl_event_register _EflObject_CAPI->pyefl_event_register
#define pyefl_object_from_instance _EflObject_CAPI->pyefl_object_from_instance


/*****************************************************************************/
#endif
/*****************************************************************************/


#ifdef __cplusplus
}
#endif

#endif /* Py_EFL_MODULE__H */
