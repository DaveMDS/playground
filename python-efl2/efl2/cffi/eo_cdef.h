
// typedef Eina_Bool (*Eo_Event_Cb)(void *data, const Eo_Event *event);



typedef void Eo;       // TODO void is correct?
typedef void Eo_Event; // TODO void is correct?
typedef Eo Eo_Class;

int eo_init(void);
int eo_shutdown(void);

// Eo* eo_add(Eo_Class *klass, Eo *parent, ...);

Eo* _eo_add_internal_start(const char *file, int line, const Eo_Class *klass_id, Eo *parent, Eina_Bool ref);
Eo* _eo_add_end(Eo *obj);

//Eo* eo_add_ref(Eo_Class *klass, Eo *parent);


// Eina_Bool eo_event_callback_add(Eo *obj, const Eo_Event_Description *desc, Eo_Event_Cb cb, const void *data);
// Eina_Bool eo_event_callback_priority_add(Eo *obj, const Eo_Event_Description *desc, Eo_Callback_Priority priority, Eo_Event_Cb cb, const void *data);



#define EO_CALLBACK_STOP ...
#define EO_CALLBACK_CONTINUE ...

// static const int EO_CALLBACK_STOP;
// static const int EO_CALLBACK_CONTINUE;

// enum my_enum { VAL1, VAL2, ... };

