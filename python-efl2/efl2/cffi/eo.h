
// enums
#define EO_CALLBACK_PRIORITY_BEFORE -100
#define EO_CALLBACK_PRIORITY_DEFAULT 0
#define EO_CALLBACK_PRIORITY_AFTER 100
#define EO_CALLBACK_STOP ...
#define EO_CALLBACK_CONTINUE ...

enum _Eo_Class_Type {
    EO_CLASS_TYPE_REGULAR,
    EO_CLASS_TYPE_REGULAR_NO_INSTANT,
    EO_CLASS_TYPE_INTERFACE,
    EO_CLASS_TYPE_MIXIN,
    ... };
typedef enum _Eo_Class_Type Eo_Class_Type;

enum _Eo_Op_Type {
   EO_OP_TYPE_INVALID,
   EO_OP_TYPE_REGULAR,
   EO_OP_TYPE_CLASS,
   EO_OP_TYPE_REGULAR_OVERRIDE,
   EO_OP_TYPE_CLASS_OVERRIDE,
   ... };
typedef enum _Eo_Op_Type Eo_Op_Type;


// typedefs
typedef void Eo;                 // TODO void* is correct?
// typedef struct _Eo_Opaque Eo; // this should be better  :/
typedef Eo Eo_Class;
typedef Eo Eo_Base;
typedef short Eo_Callback_Priority;

typedef struct _Eo_Op_Description
{
   void *api_func;         /**< The EAPI function offering this op. (The name of the func on windows) */
   void *func;             /**< The static function to call for the op. */
   Eo_Op_Type op_type;     /**< The type of the Op. */
} Eo_Op_Description;

typedef struct _Eo_Event_Description
{
  const char *name;
  Eina_Bool unfreezable;
  Eina_Bool legacy_is;
} Eo_Event_Description;

typedef struct _Eo_Event
{
  Eo_Base *obj; /** The object the event was called on. */
  const Eo_Event_Description *desc; /** The event description. */
  void *event_info; /** Extra event information passed by the event caller. */
} Eo_Event;

typedef struct _Eo_Class_Description
{
   unsigned int version; /**< The current version of eo, use #EO_VERSION */
   const char *name; /**< The name of the class. */
   Eo_Class_Type type; /**< The type of the class. */
   struct {
        const Eo_Op_Description *descs; /**< The op descriptions array of size count. */
        size_t count; /**< Number of op descriptions. */
   } ops; /**< The ops description, should be filled using #EO_CLASS_DESCRIPTION_OPS (later sorted by Eo). */
   const Eo_Event_Description **events; /**< The event descriptions for this class. */
   size_t data_size; /**< The size of data (private + protected + public) this class needs per object. */
   void (*class_constructor)(Eo_Class *klass); /**< The constructor of the class. */
   void (*class_destructor)(Eo_Class *klass); /**< The destructor of the class. */
}Eo_Class_Description;


// typedef void (*eo_key_data_free_func)(void *);
typedef Eina_Bool (*Eo_Event_Cb)(void *data, const Eo_Event *event);


// functions
int eo_init(void);
int eo_shutdown(void);

// Eo* eo_add(Eo_Class *klass, Eo *parent, ...);
Eo* _eo_add_internal_start(const char *file, int line, const Eo_Class *klass_id, Eo *parent, Eina_Bool ref);
Eo* _eo_add_end(Eo *obj);

//Eo* eo_add_ref(Eo_Class *klass, Eo *parent);
void eo_parent_set(Eo *obj, Eo_Base *parent);
Eo_Base *eo_parent_get(const Eo *obj);
int eo_event_global_freeze_count_get(const Eo *obj);
int eo_event_freeze_count_get(const Eo *obj);
Eina_Bool eo_finalized_get(const Eo *obj);
Eo_Base *eo_constructor(Eo *obj);
void eo_destructor(Eo *obj);
Eo_Base *eo_finalize(Eo *obj);
// void eo_wref_add(Eo *obj, Eo_Base **wref);
// void eo_wref_del(Eo *obj, Eo_Base **wref);
void eo_key_data_set(Eo *obj, const char *key, const void *data);
void *eo_key_data_get(const Eo *obj, const char *key);
void eo_key_data_del(Eo *obj, const char *key);
void eo_event_thaw(Eo *obj);
void eo_event_freeze(Eo *obj);
void eo_event_global_thaw(const Eo *obj);
void eo_event_global_freeze(const Eo *obj);
Eina_Bool eo_event_callback_priority_add(Eo *obj, const Eo_Event_Description *desc, Eo_Callback_Priority priority, Eo_Event_Cb cb, const void *data);

Eina_Bool eo_event_callback_add(Eo *obj, const Eo_Event_Description *desc, Eo_Event_Cb cb, const void *data);

Eina_Bool eo_event_callback_del(Eo *obj, const Eo_Event_Description *desc, Eo_Event_Cb func, const void *user_data);
// Eina_Bool eo_event_callback_array_priority_add(Eo *obj, const Eo_Callback_Array_Item *array, Eo_Callback_Priority priority, const void *data);
// Eina_Bool eo_event_callback_array_del(Eo *obj, const Eo_Callback_Array_Item *array, const void *user_data);
// Eina_Bool eo_event_callback_call(Eo *obj, const Eo_Event_Description *desc, void *event_info);
// void eo_event_callback_forwarder_add(Eo *obj, const Eo_Event_Description *desc, Eo_Base *new_obj);
// void eo_event_callback_forwarder_del(Eo *obj, const Eo_Event_Description *desc, Eo_Base *new_obj);
// void eo_dbg_info_get(Eo *obj, Eo_Dbg_Info *root_node);
// Eina_Iterator *eo_children_iterator_new(Eo *obj);


extern const Eo_Event_Description _EO_BASE_EVENT_CALLBACK_ADD;
extern const Eo_Event_Description _EO_BASE_EVENT_CALLBACK_DEL;
extern const Eo_Event_Description _EO_BASE_EVENT_DEL;


// from Eo.h
Eo *eo_ref(const Eo *obj);
void eo_unref(const Eo *obj);
int eo_ref_get(const Eo *obj);
void eo_del(const Eo *obj);





// python callbacks
extern "Python" Eina_Bool _eo_event_cb(void *data, const Eo_Event *event);
extern "Python" Eina_Bool _eo_del_cb(void *data, const Eo_Event *event);


