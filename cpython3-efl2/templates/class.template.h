<!--(include)-->copyright_c.include<!--(end)-->#!
<!--(include)-->macros.include<!--(end)-->#!
<!--(macro HEADER_GUARD)-->
Py_${cls.full_name.upper().replace('.','_',)}$__H
<!--(end)-->

#ifndef ${HEADER_GUARD}$
#define ${HEADER_GUARD}$
#ifdef __cplusplus
extern "C" {
#endif


/* The ${cls.full_name}$ Type */
extern PyTypeObject  ${CLS_OBJECT_TYPE}$Internal;
extern PyTypeObject *${CLS_OBJECT_TYPE}$;
#define ${CLS_OBJECT}$_Check(v) (Py_TYPE(v) == ${CLS_OBJECT_TYPE}$)


/* The ${cls.full_name}$ object */
typedef struct {
    ${CLS_BASE_OBJECT}$ base;
} ${CLS_OBJECT}$;


Eina_Bool ${OBJECT_FINALIZE_FUNC}$(PyObject *module);


#ifdef __cplusplus
}
#endif

#endif /* ${HEADER_GUARD}$ */
