

// enums
// #define ELM_WIN_BASIC ...
// #define ECORE_CALLBACK_RENEW ...
// #define ECORE_CALLBACK_PASS_ON ...
// #define ECORE_CALLBACK_DONE ...

typedef enum {
    ELM_WIN_UNKNOWN,
    ELM_WIN_BASIC,
    ELM_WIN_DIALOG_BASIC,
    ...
} Elm_Win_Type; // TODO COMPLETE


// typedefs
// typedef Eina_Bool(*Ecore_Task_Cb) (void *data);

// functions
int elm_init(int argc, char **argv);
int elm_shutdown(void);
void elm_run(void);
void elm_exit(void);

// void ecore_main_loop_begin(void);
// void ecore_main_loop_quit(void);

// Elm.Box
const Eo_Class *elm_box_class_get(void);
// void elm_obj_box_homogeneous_set(Eo *obj, Eina_Bool homogeneous);
// Eina_Bool elm_obj_box_homogeneous_get(const Eo *obj);
// void elm_obj_box_align_set(Eo *obj, double horizontal, double vertical);
// void elm_obj_box_align_get(const Eo *obj, double *horizontal, double *vertical);
// void elm_obj_box_horizontal_set(Eo *obj, Eina_Bool horizontal);
// Eina_Bool elm_obj_box_horizontal_get(const Eo *obj);
// void elm_obj_box_padding_set(Eo *obj, Evas_Coord horizontal, Evas_Coord vertical);
// void elm_obj_box_padding_get(const Eo *obj, Evas_Coord *horizontal, Evas_Coord *vertical);
// void elm_obj_box_layout_set(Eo *obj, Evas_Object_Box_Layout cb, const void *data, Ecore_Cb free_data);
// Eina_List *elm_obj_box_children_get(const Eo *obj);
void elm_obj_box_pack_end(Eo *obj, Evas_Object *subobj);
// void elm_obj_box_unpack_all(Eo *obj);
// void elm_obj_box_unpack(Eo *obj, Evas_Object *subobj);
// void elm_obj_box_pack_after(Eo *obj, Evas_Object *subobj, Evas_Object *after);
void elm_obj_box_pack_start(Eo *obj, Evas_Object *subobj);
// void elm_obj_box_recalculate(Eo *obj);
// void elm_obj_box_pack_before(Eo *obj, Evas_Object *subobj, Evas_Object *before);
void elm_obj_box_clear(Eo *obj);


// Elm.Layout
Eina_Bool elm_obj_layout_text_set(Eo *obj, const char * part, const char *text);
const char *elm_obj_layout_text_get(const Eo *obj, const char * part);


// Elm.Win
const Eo_Class *elm_win_class_get(void);
void elm_obj_win_name_set(Eo *obj, const char *name);
void elm_obj_win_type_set(Eo *obj, Elm_Win_Type type);

void elm_obj_win_resize_object_add(Eo *obj, Evas_Object *subobj);
void elm_obj_win_title_set(Eo *obj, const char *title);
const char *elm_obj_win_title_get(const Eo *obj);


// Elm.Win_Standard
const Eo_Class *elm_win_standard_class_get(void);


// Elm.Label
const Eo_Class *elm_label_class_get(void);

// Elm.Button
const Eo_Class *elm_button_class_get(void);

