

#include <Eo.h>

#ifndef Py__EFL_LOOP_USER_H
#define Py__EFL_LOOP_USER_H
#ifdef __cplusplus
extern "C" {
#endif


/* Python module and C API name */
#define EflLoop_User_MODULE_NAME "efl2._loop_user"
#define EflLoop_User_CAPI_NAME "CAPI"
#define EflLoop_User_CAPSULE_NAME "efl2._loop_user.CAPI"


typedef struct {
    Efl_ObjectObject base;
    // PyObject            *x_attr;        /* Attributes dictionary */
} Efl_Loop_UserObject;

/* C API for usage by other modules */
typedef struct {
    // Exported types
    PyTypeObject *Efl_Loop_UserType;
    // Exported functions
} EflLoop_User_CAPI_t;


/******************************************************************************/
/***** This section is used ONLY in modules that use efl.object.c API *********/
/******************************************************************************/
#ifndef INSIDE_EFL_LOOP_USER_MODULE

static EflLoop_User_CAPI_t *_EflLoop_User_CAPI;

/* Return -1 on error, 0 on success.
 * PyCapsule_Import will set an exception if there's an error.
 */
static int
import_efl_loop_user(void)
{
    _EflLoop_User_CAPI = PyCapsule_Import(EflLoop_User_CAPSULE_NAME, 0); // TODO 0 or 1 ??
    return (_EflLoop_User_CAPI != NULL) ? 0 : -1;
}

// defines for faster access in modules
#define Efl_Loop_UserType _EflLoop_User_CAPI->Efl_Loop_UserType


#endif /* !INSIDE_EFL_LOOP_USER_MODULE */
/******************************************************************************/

#ifdef __cplusplus
}
#endif
#endif /* !Py__EFL_LOOP_USER_H */
