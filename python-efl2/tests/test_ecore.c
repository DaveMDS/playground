

// gcc -Wall -D EFL_BETA_API_SUPPORT -D EFL_EO_API_SUPPORT `pkg-config --libs --cflags eo ecore` test_ecore.c -o test_ecore


#include <Eo.h>
#include <Ecore.h>



// Eina_Bool
// _del_cb(void *data, const Eo_Event *event)
// {
    // printf("del !!!!\n");
// 
    // return 0;
// }


Eina_Bool
_timer_cb(void *data)
{
    printf("Timer\n");
    return 1;
}

int
main(int argc, char **argv)
{
    eo_init();
    ecore_init();

    // timer
    Ecore_Timer *t;
    t = _eo_add_internal_start(NULL, 0, ecore_timer_class_get(), NULL, EINA_FALSE, EINA_FALSE);
    ecore_obj_timer_constructor(t, 1.0, _timer_cb, NULL);
    _eo_add_end(t, EINA_FALSE);


    // mainloop
    Eo *ml;
    ml = _eo_add_internal_start(NULL, 0, ecore_mainloop_class_get(), NULL, EINA_FALSE, EINA_FALSE);
    _eo_add_end(ml, EINA_FALSE);
    ecore_mainloop_begin(ml);


    ecore_shutdown();
    return 0;
}

