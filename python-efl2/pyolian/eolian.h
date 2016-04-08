///////////////////////////////////////////////////////////////////////////////
////                   THIS FILE IS MANUALLY WRITTEN                       ////
///////////////////////////////////////////////////////////////////////////////

////  Eina  ///////////////////////////////////////////////////////////////////
typedef unsigned char Eina_Bool;
#define EINA_FALSE 0
#define EINA_TRUE  1

typedef struct _Eina_Iterator Eina_Iterator;
typedef const char Eina_Stringshare;

void      eina_iterator_free         (Eina_Iterator *iterator);
Eina_Bool eina_iterator_next         (Eina_Iterator *iterator, void **data);
Eina_Bool eina_iterator_lock         (Eina_Iterator *iterator);
Eina_Bool eina_iterator_unlock       (Eina_Iterator *iterator);
void     *eina_iterator_container_get(Eina_Iterator *iterator);


////  enums  //////////////////////////////////////////////////////////////////
typedef enum
{
   EOLIAN_UNRESOLVED = 0,
   EOLIAN_PROPERTY,
   EOLIAN_PROP_SET,
   EOLIAN_PROP_GET,
   EOLIAN_METHOD
} Eolian_Function_Type;

typedef enum
{
   EOLIAN_IN_PARAM = 0,
   EOLIAN_OUT_PARAM,
   EOLIAN_INOUT_PARAM
} Eolian_Parameter_Dir;

typedef enum
{
   EOLIAN_CLASS_UNKNOWN_TYPE = 0,
   EOLIAN_CLASS_REGULAR,
   EOLIAN_CLASS_ABSTRACT,
   EOLIAN_CLASS_MIXIN,
   EOLIAN_CLASS_INTERFACE
} Eolian_Class_Type;

typedef enum
{
   EOLIAN_SCOPE_PUBLIC = 0,
   EOLIAN_SCOPE_PRIVATE,
   EOLIAN_SCOPE_PROTECTED
} Eolian_Object_Scope;

typedef enum
{
   EOLIAN_TYPEDECL_UNKNOWN = 0,
   EOLIAN_TYPEDECL_STRUCT,
   EOLIAN_TYPEDECL_STRUCT_OPAQUE,
   EOLIAN_TYPEDECL_ENUM,
   EOLIAN_TYPEDECL_ALIAS
} Eolian_Typedecl_Type;

typedef enum
{
   EOLIAN_TYPE_UNKNOWN_TYPE = 0,
   EOLIAN_TYPE_VOID,
   EOLIAN_TYPE_REGULAR,
   EOLIAN_TYPE_COMPLEX,
   EOLIAN_TYPE_POINTER,
   EOLIAN_TYPE_CLASS,
   EOLIAN_TYPE_UNDEFINED
} Eolian_Type_Type;

typedef enum
{
   EOLIAN_EXPR_UNKNOWN = 0,
   EOLIAN_EXPR_INT,
   EOLIAN_EXPR_UINT,
   EOLIAN_EXPR_LONG,
   EOLIAN_EXPR_ULONG,
   EOLIAN_EXPR_LLONG,
   EOLIAN_EXPR_ULLONG,
   EOLIAN_EXPR_FLOAT,
   EOLIAN_EXPR_DOUBLE,
   EOLIAN_EXPR_STRING,
   EOLIAN_EXPR_CHAR,
   EOLIAN_EXPR_NULL,
   EOLIAN_EXPR_BOOL,
   EOLIAN_EXPR_NAME,
   EOLIAN_EXPR_UNARY,
   EOLIAN_EXPR_BINARY
} Eolian_Expression_Type;

typedef enum
{
   EOLIAN_MASK_SINT,
   EOLIAN_MASK_UINT,
   EOLIAN_MASK_INT,
   EOLIAN_MASK_FLOAT,
   EOLIAN_MASK_BOOL,
   EOLIAN_MASK_STRING,
   EOLIAN_MASK_CHAR,
   EOLIAN_MASK_NULL,
   EOLIAN_MASK_NUMBER,
   EOLIAN_MASK_ALL,
   ...
} Eolian_Expression_Mask;

typedef enum
{
   EOLIAN_VAR_UNKNOWN = 0,
   EOLIAN_VAR_CONSTANT,
   EOLIAN_VAR_GLOBAL
} Eolian_Variable_Type;

typedef union
{
   char               c;
   Eina_Bool          b;
   const    char     *s;
   signed   int       i;
   unsigned int       u;
   signed   long      l;
   unsigned long      ul;
   signed   long long ll;
   unsigned long long ull;
   float              f;
   double             d;
} Eolian_Value_Union;

typedef struct _Eolian_Value
{
   Eolian_Expression_Type type;
   Eolian_Value_Union value;
} Eolian_Value;

typedef enum
{
   EOLIAN_BINOP_INVALID = -1,

   EOLIAN_BINOP_ADD, /* + int, float */
   EOLIAN_BINOP_SUB, /* - int, float */
   EOLIAN_BINOP_MUL, /* * int, float */
   EOLIAN_BINOP_DIV, /* / int, float */
   EOLIAN_BINOP_MOD, /* % int */

   EOLIAN_BINOP_EQ, /* == all types */
   EOLIAN_BINOP_NQ, /* != all types */
   EOLIAN_BINOP_GT, /* >  int, float */
   EOLIAN_BINOP_LT, /* <  int, float */
   EOLIAN_BINOP_GE, /* >= int, float */
   EOLIAN_BINOP_LE, /* <= int, float */

   EOLIAN_BINOP_AND, /* && all types */
   EOLIAN_BINOP_OR,  /* || all types */

   EOLIAN_BINOP_BAND, /* &  int */
   EOLIAN_BINOP_BOR,  /* |  int */
   EOLIAN_BINOP_BXOR, /* ^  int */
   EOLIAN_BINOP_LSH,  /* << int */
   EOLIAN_BINOP_RSH   /* >> int */
} Eolian_Binary_Operator;

typedef enum
{
   EOLIAN_UNOP_INVALID = -1,

   EOLIAN_UNOP_UNM, /* - sint */
   EOLIAN_UNOP_UNP, /* + sint */

   EOLIAN_UNOP_NOT,  /* ! int, float, bool */
   EOLIAN_UNOP_BNOT, /* ~ int */
} Eolian_Unary_Operator;

typedef enum
{
   EOLIAN_DECL_UNKNOWN = -1,
   EOLIAN_DECL_CLASS,
   EOLIAN_DECL_ALIAS,
   EOLIAN_DECL_STRUCT,
   EOLIAN_DECL_ENUM,
   EOLIAN_DECL_VAR,
} Eolian_Declaration_Type;

////  typedefs  ///////////////////////////////////////////////////////////////
typedef struct _Eolian_Class Eolian_Class;
typedef struct _Eolian_Function Eolian_Function;
typedef struct _Eolian_Type Eolian_Type;
typedef struct _Eolian_Typedecl Eolian_Typedecl;
typedef struct _Eolian_Function_Parameter Eolian_Function_Parameter;
typedef struct _Eolian_Implement Eolian_Implement;
typedef struct _Eolian_Constructor Eolian_Constructor;
typedef struct _Eolian_Event Eolian_Event;
typedef struct _Eolian_Expression Eolian_Expression;
typedef struct _Eolian_Variable Eolian_Variable;
typedef struct _Eolian_Struct_Type_Field Eolian_Struct_Type_Field;
typedef struct _Eolian_Enum_Type_Field Eolian_Enum_Type_Field;
typedef struct _Eolian_Declaration Eolian_Declaration;
typedef struct _Eolian_Documentation Eolian_Documentation;


////  functions  //////////////////////////////////////////////////////////////
int eolian_init(void);
int eolian_shutdown(void);

// database population
Eina_Bool      eolian_file_parse(const char *filepath);
Eina_Iterator *eolian_all_eo_file_paths_get(void);
Eina_Iterator *eolian_all_eot_file_paths_get(void);
Eina_Iterator *eolian_all_eo_files_get(void);
Eina_Iterator *eolian_all_eot_files_get(void);
Eina_Bool      eolian_directory_scan(const char *dir);
Eina_Bool      eolian_system_directory_scan(void);
Eina_Bool      eolian_all_eo_files_parse(void);
Eina_Bool      eolian_all_eot_files_parse(void);
Eina_Bool      eolian_database_validate(Eina_Bool silent_types);

// class
Eina_Iterator         *eolian_all_classes_get(void);
Eina_Stringshare      *eolian_class_c_get_function_name_get(const Eolian_Class *klass);
const Eolian_Class    *eolian_class_get_by_name(const char *class_name);
const Eolian_Class    *eolian_class_get_by_file(const char *file_name);
Eina_Stringshare      *eolian_class_file_get(const Eolian_Class *klass);
Eina_Stringshare      *eolian_class_full_name_get(const Eolian_Class *klass);
Eina_Stringshare      *eolian_class_name_get(const Eolian_Class *klass);
Eina_Iterator         *eolian_class_namespaces_get(const Eolian_Class *klass);
Eolian_Class_Type      eolian_class_type_get(const Eolian_Class *klass);
const Eolian_Documentation *eolian_class_documentation_get(const Eolian_Class *klass);
Eina_Stringshare      *eolian_class_legacy_prefix_get(const Eolian_Class *klass);
Eina_Stringshare      *eolian_class_eo_prefix_get(const Eolian_Class *klass);
Eina_Stringshare      *eolian_class_data_type_get(const Eolian_Class *klass);
Eina_Iterator         *eolian_class_inherits_get(const Eolian_Class *klass);
Eina_Iterator         *eolian_class_functions_get(const Eolian_Class *klass, Eolian_Function_Type func_type);
const Eolian_Function *eolian_class_function_get_by_name(const Eolian_Class *klass, const char *func_name, Eolian_Function_Type f_type);
const Eolian_Event    *eolian_class_event_get_by_name(const Eolian_Class *klass, const char *event_name);
Eina_Bool              eolian_class_ctor_enable_get(const Eolian_Class *klass);
Eina_Bool              eolian_class_dtor_enable_get(const Eolian_Class *klass);
Eina_Iterator         *eolian_class_constructors_get(const Eolian_Class *klass);
Eina_Iterator         *eolian_class_events_get(const Eolian_Class *klass);
Eina_Iterator         *eolian_class_implements_get(const Eolian_Class *klass);

// constructor
Eina_Stringshare      *eolian_constructor_full_name_get(const Eolian_Constructor *ctor);
const Eolian_Class    *eolian_constructor_class_get(const Eolian_Constructor *ctor);
const Eolian_Function *eolian_constructor_function_get(const Eolian_Constructor *ctor);
Eina_Bool              eolian_constructor_is_optional(const Eolian_Constructor *ctor);

// event 
Eina_Stringshare           *eolian_event_name_get(const Eolian_Event *event);
const Eolian_Type          *eolian_event_type_get(const Eolian_Event *event);
const Eolian_Documentation *eolian_event_documentation_get(const Eolian_Event *event);
Eolian_Object_Scope         eolian_event_scope_get(const Eolian_Event *event);
Eina_Bool                   eolian_event_is_beta(const Eolian_Event *event);
Eina_Bool                   eolian_event_is_hot(const Eolian_Event *event);
Eina_Stringshare           *eolian_event_c_name_get(const Eolian_Event *event);

// property
Eina_Iterator              *eolian_property_keys_get(const Eolian_Function *foo_id, Eolian_Function_Type ftype);
Eina_Iterator              *eolian_property_values_get(const Eolian_Function *foo_id, Eolian_Function_Type ftype);

// function
Eolian_Function_Type        eolian_function_type_get(const Eolian_Function *function_id);
Eolian_Object_Scope         eolian_function_scope_get(const Eolian_Function *function_id);
Eina_Stringshare           *eolian_function_name_get(const Eolian_Function *function_id);
Eina_Stringshare           *eolian_function_full_c_name_get(const Eolian_Function *function_id, Eolian_Function_Type ftype, Eina_Bool use_legacy);
Eina_Stringshare           *eolian_function_legacy_get(const Eolian_Function *function_id, Eolian_Function_Type f_type);
const Eolian_Documentation *eolian_function_documentation_get(const Eolian_Function *function_id, Eolian_Function_Type f_type);
Eina_Bool                   eolian_function_is_virtual_pure(const Eolian_Function *function_id, Eolian_Function_Type f_type);
Eina_Bool                   eolian_function_is_auto(const Eolian_Function *function_id, Eolian_Function_Type f_type);
Eina_Bool                   eolian_function_is_empty(const Eolian_Function *function_id, Eolian_Function_Type f_type);
Eina_Bool                   eolian_function_is_legacy_only(const Eolian_Function *function_id, Eolian_Function_Type ftype);
Eina_Bool                   eolian_function_is_class(const Eolian_Function *function_id);
Eina_Bool                   eolian_function_is_c_only(const Eolian_Function *function_id);
Eina_Bool                   eolian_function_is_beta(const Eolian_Function *function_id);
Eina_Bool                   eolian_function_is_constructor(const Eolian_Function *function_id, const Eolian_Class *klass);
Eina_Iterator              *eolian_function_parameters_get(const Eolian_Function *function_id);
Eina_Bool                   eolian_function_object_is_const(const Eolian_Function *function_id);
const Eolian_Class         *eolian_function_class_get(const Eolian_Function *function_id);
Eina_Bool                   eolian_function_is_implemented(const Eolian_Function *function_id, Eolian_Function_Type func_type, const Eolian_Class *klass);

// parameter
Eolian_Parameter_Dir        eolian_parameter_direction_get(const Eolian_Function_Parameter *param);
const Eolian_Type          *eolian_parameter_type_get(const Eolian_Function_Parameter *param);
const Eolian_Expression    *eolian_parameter_default_value_get(const Eolian_Function_Parameter *param);
Eina_Stringshare           *eolian_parameter_name_get(const Eolian_Function_Parameter *param);
const Eolian_Documentation *eolian_parameter_documentation_get(const Eolian_Function_Parameter *param);
Eina_Bool                   eolian_parameter_is_nonull(const Eolian_Function_Parameter *param_desc);
Eina_Bool                   eolian_parameter_is_nullable(const Eolian_Function_Parameter *param_desc);
Eina_Bool                   eolian_parameter_is_optional(const Eolian_Function_Parameter *param_desc);

// return
const Eolian_Type          *eolian_function_return_type_get(const Eolian_Function *function_id, Eolian_Function_Type ftype);
const Eolian_Expression    *eolian_function_return_default_value_get(const Eolian_Function *foo_id, Eolian_Function_Type ftype);
const Eolian_Documentation *eolian_function_return_documentation_get(const Eolian_Function *foo_id, Eolian_Function_Type ftype);
Eina_Bool                   eolian_function_return_is_warn_unused(const Eolian_Function *foo_id, Eolian_Function_Type ftype);

// implement
Eina_Stringshare      *eolian_implement_full_name_get(const Eolian_Implement *impl);
const Eolian_Class    *eolian_implement_class_get(const Eolian_Implement *impl);
const Eolian_Function *eolian_implement_function_get(const Eolian_Implement *impl, Eolian_Function_Type *func_type);
Eina_Bool              eolian_implement_is_auto(const Eolian_Implement *impl);
Eina_Bool              eolian_implement_is_empty(const Eolian_Implement *impl);
Eina_Bool              eolian_implement_is_virtual(const Eolian_Implement *impl);
Eina_Bool              eolian_implement_is_prop_get(const Eolian_Implement *impl);
Eina_Bool              eolian_implement_is_prop_set(const Eolian_Implement *impl);

// typedecl
const Eolian_Typedecl          *eolian_typedecl_alias_get_by_name(const char *name);
const Eolian_Typedecl          *eolian_typedecl_struct_get_by_name(const char *name);
const Eolian_Typedecl          *eolian_typedecl_enum_get_by_name(const char *name);
Eina_Iterator                  *eolian_typedecl_aliases_get_by_file(const char *fname);
Eina_Iterator                  *eolian_typedecl_structs_get_by_file(const char *fname);
Eina_Iterator                  *eolian_typedecl_enums_get_by_file(const char *fname);
Eolian_Typedecl_Type            eolian_typedecl_type_get(const Eolian_Typedecl *tp);
Eina_Iterator                  *eolian_typedecl_struct_fields_get(const Eolian_Typedecl *tp);
const Eolian_Struct_Type_Field *eolian_typedecl_struct_field_get(const Eolian_Typedecl *tp, const char *field);
Eina_Stringshare               *eolian_typedecl_struct_field_name_get(const Eolian_Struct_Type_Field *fl);
const Eolian_Documentation     *eolian_typedecl_struct_field_documentation_get(const Eolian_Struct_Type_Field *fl);
const Eolian_Type              *eolian_typedecl_struct_field_type_get(const Eolian_Struct_Type_Field *fl);
Eina_Iterator                  *eolian_typedecl_enum_fields_get(const Eolian_Typedecl *tp);
const Eolian_Enum_Type_Field   *eolian_typedecl_enum_field_get(const Eolian_Typedecl *tp, const char *field);
Eina_Stringshare               *eolian_typedecl_enum_field_name_get(const Eolian_Enum_Type_Field *fl);
Eina_Stringshare               *eolian_typedecl_enum_field_c_name_get(const Eolian_Enum_Type_Field *fl);
const Eolian_Documentation     *eolian_typedecl_enum_field_documentation_get(const Eolian_Enum_Type_Field *fl);
const Eolian_Expression        *eolian_typedecl_enum_field_value_get(const Eolian_Enum_Type_Field *fl, Eina_Bool force);
Eina_Stringshare               *eolian_typedecl_enum_legacy_prefix_get(const Eolian_Typedecl *tp);
const Eolian_Documentation     *eolian_typedecl_documentation_get(const Eolian_Typedecl *tp);
Eina_Stringshare               *eolian_typedecl_file_get(const Eolian_Typedecl *tp);
const Eolian_Type              *eolian_typedecl_base_type_get(const Eolian_Typedecl *tp);
const Eolian_Type              *eolian_typedecl_aliased_base_get(const Eolian_Typedecl *tp);
Eina_Bool                       eolian_typedecl_is_extern(const Eolian_Typedecl *tp);
Eina_Stringshare               *eolian_typedecl_c_type_named_get(const Eolian_Typedecl *tp, const char *name);
Eina_Stringshare               *eolian_typedecl_c_type_get(const Eolian_Typedecl *tp);
Eina_Stringshare               *eolian_typedecl_name_get(const Eolian_Typedecl *tp);
Eina_Stringshare               *eolian_typedecl_full_name_get(const Eolian_Typedecl *tp);
Eina_Iterator                  *eolian_typedecl_namespaces_get(const Eolian_Typedecl *tp);
Eina_Stringshare               *eolian_typedecl_free_func_get(const Eolian_Typedecl *tp);

// type
Eolian_Type_Type       eolian_type_type_get(const Eolian_Type *tp);
Eina_Iterator         *eolian_type_subtypes_get(const Eolian_Type *tp);
Eina_Stringshare      *eolian_type_file_get(const Eolian_Type *tp);
const Eolian_Type     *eolian_type_base_type_get(const Eolian_Type *tp);
const Eolian_Typedecl *eolian_type_typedecl_get(const Eolian_Type *tp);
const Eolian_Type     *eolian_type_aliased_base_get(const Eolian_Type *tp);
const Eolian_Class    *eolian_type_class_get(const Eolian_Type *tp);
Eina_Bool              eolian_type_is_own(const Eolian_Type *tp);
Eina_Bool              eolian_type_is_const(const Eolian_Type *tp);
Eina_Stringshare      *eolian_type_c_type_named_get(const Eolian_Type *tp, const char *name);
Eina_Stringshare      *eolian_type_c_type_get(const Eolian_Type *tp);
Eina_Stringshare      *eolian_type_name_get(const Eolian_Type *tp);
Eina_Stringshare      *eolian_type_full_name_get(const Eolian_Type *tp);
Eina_Iterator         *eolian_type_namespaces_get(const Eolian_Type *tp);
Eina_Stringshare      *eolian_type_free_func_get(const Eolian_Type *tp);

// expression
Eolian_Value             eolian_expression_eval(const Eolian_Expression *expr, Eolian_Expression_Mask m);
Eolian_Value             eolian_expression_eval_type(const Eolian_Expression *expr, const Eolian_Type *type);
Eina_Stringshare        *eolian_expression_value_to_literal(const Eolian_Value *v);
Eina_Stringshare        *eolian_expression_serialize(const Eolian_Expression *expr);
Eolian_Expression_Type   eolian_expression_type_get(const Eolian_Expression *expr);
Eolian_Binary_Operator   eolian_expression_binary_operator_get(const Eolian_Expression *expr);
const Eolian_Expression *eolian_expression_binary_lhs_get(const Eolian_Expression *expr);
const Eolian_Expression *eolian_expression_binary_rhs_get(const Eolian_Expression *expr);
Eolian_Unary_Operator    eolian_expression_unary_operator_get(const Eolian_Expression *expr);
const Eolian_Expression *eolian_expression_unary_expression_get(const Eolian_Expression *expr);
Eolian_Value             eolian_expression_value_get(const Eolian_Expression *expr);

// variable
const Eolian_Variable      *eolian_variable_global_get_by_name(const char *name);
const Eolian_Variable      *eolian_variable_constant_get_by_name(const char *name);
Eina_Iterator              *eolian_variable_globals_get_by_file(const char *fname);
Eina_Iterator              *eolian_variable_constants_get_by_file(const char *fname);
Eolian_Variable_Type        eolian_variable_type_get(const Eolian_Variable *var);
const Eolian_Documentation *eolian_variable_documentation_get(const Eolian_Variable *var);
Eina_Stringshare           *eolian_variable_file_get(const Eolian_Variable *var);
const Eolian_Type          *eolian_variable_base_type_get(const Eolian_Variable *var);
const Eolian_Expression    *eolian_variable_value_get(const Eolian_Variable *var);
Eina_Stringshare           *eolian_variable_name_get(const Eolian_Variable *var);
Eina_Stringshare           *eolian_variable_full_name_get(const Eolian_Variable *var);
Eina_Iterator              *eolian_variable_namespaces_get(const Eolian_Variable *var);
Eina_Bool                   eolian_variable_is_extern(const Eolian_Variable *var);

// declaration
const Eolian_Declaration *eolian_declaration_get_by_name(const char *name);
Eina_Iterator            *eolian_declarations_get_by_file(const char *fname);
Eolian_Declaration_Type   eolian_declaration_type_get(const Eolian_Declaration *decl);
Eina_Stringshare         *eolian_declaration_name_get(const Eolian_Declaration *decl);
const Eolian_Class       *eolian_declaration_class_get(const Eolian_Declaration *decl);
const Eolian_Typedecl    *eolian_declaration_data_type_get(const Eolian_Declaration *decl);
const Eolian_Variable    *eolian_declaration_variable_get(const Eolian_Declaration *decl);

// documentation
Eina_Stringshare    *eolian_documentation_summary_get(const Eolian_Documentation *doc);
Eina_Stringshare    *eolian_documentation_description_get(const Eolian_Documentation *doc);
Eina_Stringshare    *eolian_documentation_since_get(const Eolian_Documentation *doc);
