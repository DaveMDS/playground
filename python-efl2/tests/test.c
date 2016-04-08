

// gcc -Wall -D EFL_BETA_API_SUPPORT -D EFL_EO_API_SUPPORT `pkg-config --libs --cflags elementary` test.c -o test


#include <Elementary.h>



Eina_Bool
_del_cb(void *data, const Eo_Event *event)
{
    printf("del !!!!\n");

    return 0;
}

Eina_Bool
_click_cb(void *data, const Eo_Event *event)
{
    printf("click !!!!\n");

    return 0;
}

Evas_Object *win, *bt;

EAPI_MAIN int
elm_main(int argc, char **argv)
{
    // win
    // win = _eo_add_internal_start(NULL, 0, ELM_WIN_STANDARD_CLASS, NULL, EINA_FALSE);
    win = _eo_add_internal_start(NULL, 0, elm_win_standard_class_get(), NULL, EINA_FALSE);
    elm_obj_win_name_set(win, "c_test");
    elm_obj_win_title_set(win, "Eo API test");
    _eo_add_end(win);


    // button
    // bt = eo_add(ELM_BUTTON_CLASS, win);
    bt = _eo_add_internal_start(NULL, 0, elm_button_class_get(), win, EINA_FALSE);
    _eo_add_end(bt);
    
    elm_obj_layout_text_set(bt, NULL, "asdasd");
    elm_obj_win_resize_object_add(win, bt);
    efl_gfx_visible_set(bt, EINA_TRUE);

    eo_event_callback_add(bt, EVAS_CLICKABLE_INTERFACE_EVENT_CLICKED, _click_cb, NULL);
    eo_event_callback_add(bt, EO_BASE_EVENT_DEL, _del_cb, NULL);


    //
    efl_gfx_size_set(win, 180, 180);
    efl_gfx_visible_set(win, EINA_TRUE);
    elm_run();


    return 0;
}
ELM_MAIN()
