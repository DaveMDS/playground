#ifndef Py_EFL_LOOP_TIMER_H
#define Py_EFL_LOOP_TIMER_H
#ifdef __cplusplus
extern "C" {
#endif

#include <Eo.h>


/* The Efl.Loop.Timer Type */
extern PyTypeObject PyEfl_Loop_TimerType;
#define Efl_Loop_Timer_Check(v) (Py_TYPE(v) == PyEfl_Loop_TimerType)

/* The Efl.Loop.Timer object */
typedef struct {
    PyEfl_Loop_User base;
} PyEfl_Loop_Timer;


Eina_Bool pyefl_loop_timer_object_finalize(PyObject *module);



#ifdef __cplusplus
}
#endif

#endif /* Py_EFL_LOOP_TIMER_H */
