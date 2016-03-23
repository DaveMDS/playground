

// enums
#define ECORE_CALLBACK_CANCEL ...
#define ECORE_CALLBACK_RENEW ...
#define ECORE_CALLBACK_PASS_ON ...
#define ECORE_CALLBACK_DONE ...

// typedefs
typedef Eina_Bool(*Ecore_Task_Cb) (void *data);

// functions
int ecore_init(void);
int ecore_shutdown(void);

void ecore_main_loop_begin(void);
void ecore_main_loop_quit(void);


// Timer
const Eo_Class *ecore_timer_class_get(void);
// #define	ECORE_TIMER_CLASS ...
void ecore_obj_timer_constructor(Eo *obj, double in, Ecore_Task_Cb func, const void *data);
void ecore_obj_timer_loop_constructor(Eo *obj, double in, Ecore_Task_Cb func, const void *data);
void ecore_obj_timer_interval_set(Eo *obj, double in);
double ecore_obj_timer_interval_get(const Eo *obj);
double ecore_obj_timer_pending_get(const Eo *obj);
void ecore_obj_timer_reset(Eo *obj);
void ecore_obj_timer_delay(Eo *obj, double add);



// python callbacks
extern "Python" Eina_Bool _timer_cb(void *data);

