#ifndef Py_EFL_LOOP_USER_H
#define Py_EFL_LOOP_USER_H
#ifdef __cplusplus
extern "C" {
#endif

/* The Efl.Loop_User Type */
extern PyTypeObject PyEfl_Loop_UserType;
#define Efl_Loop_User_Check(v) (Py_TYPE(v) == Efl_Loop_UserType)

/* The Efl.Loop_User object */
typedef struct {
    PyEfl_Object base;
} PyEfl_Loop_User;

Eina_Bool pyefl_loop_user_object_finalize(PyObject *module);

#ifdef __cplusplus
}
#endif
#endif /* !Py_EFL_LOOP_USER_H */
