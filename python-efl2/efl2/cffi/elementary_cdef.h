

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


// Window
const Eo_Class *elm_win_class_get(void);

void elm_obj_win_name_set(Eo *obj, const char *name);
void elm_obj_win_type_set(Eo *obj, Elm_Win_Type type);




// TODO REMOVE ME
void evas_object_show(Eo *obj);
void evas_object_resize(Eo *obj, int w, int h);
