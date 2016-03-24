

// enums
// #define ECORE_CALLBACK_RENEW ...
// #define ECORE_CALLBACK_PASS_ON ...
// #define ECORE_CALLBACK_DONE ...

// typedef enum {
    // ELM_WIN_UNKNOWN,
    // ELM_WIN_BASIC,
    // ELM_WIN_DIALOG_BASIC,
    // ...
// } Elm_Win_Type; // TODO COMPLETE


// typedefs
// typedef Eo Evas_Object;
// typedef Eina_Bool(*Ecore_Task_Cb) (void *data);

// functions
// int efl_init(void);
// int efl_shutdown(void);

// Efl.Gfx.Base
Eo_Class *efl_gfx_base_interface_get(void);
void efl_gfx_position_set(Eo *obj, int x, int y);
void efl_gfx_position_get(const Eo *obj, int *x, int *y);
void efl_gfx_size_set(Eo *obj, int w, int h);
void efl_gfx_size_get(const Eo *obj, int *w, int *h);
void efl_gfx_color_set(Eo *obj, int r, int g, int b, int a);
void efl_gfx_color_get(const Eo *obj, int *r, int *g, int *b, int *a);
Eina_Bool efl_gfx_color_part_set(Eo *obj, const char * part, int r, int g, int b, int a);
Eina_Bool efl_gfx_color_part_get(const Eo *obj, const char * part, int *r, int *g, int *b, int *a);
void efl_gfx_visible_set(Eo *obj, Eina_Bool v);
Eina_Bool efl_gfx_visible_get(const Eo *obj);



// void evas_object_show(Eo *obj); // TODO use eo API instead
// void evas_object_resize(Eo *obj, int w, int h);

// void ecore_main_loop_begin(void);
// void ecore_main_loop_quit(void);

// Elm.Layout
// Eina_Bool elm_obj_layout_text_set(Eo *obj, const char * part, const char *text);
// const char *elm_obj_layout_text_get(const Eo *obj, const char * part);


// Elm.Win



