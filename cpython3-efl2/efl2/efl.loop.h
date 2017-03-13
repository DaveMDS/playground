#ifndef Py_EFL_LOOP__H
#define Py_EFL_LOOP__H
#ifdef __cplusplus
extern "C" {
#endif

#include <Eo.h>


/* The Efl.Loop Type */
extern PyTypeObject PyEfl_LoopType;
#define Efl_Loop_Check(v) (Py_TYPE(v) == Efl_LoopType)

/* The Efl.Loop object */
typedef struct {
    PyEfl_Object base_class;
} PyEfl_Loop;


Eina_Bool pyefl_loop_object_finalize(PyObject *module);



#ifdef __cplusplus
}
#endif

#endif /* Py_EFL_LOOP__H */
