#!/usr/bin/env python3
# This Python file uses the following encoding: utf-8
#
# Just a simple playground for testing eolian functionalities.
#

import eolian


# TODO FIXME !!
SCAN_FOLDER = '/home/dave/e/core/efl/src/lib/'


# create main eolian state
state = eolian.Eolian()
if not isinstance(state, eolian.Eolian):
    raise(RuntimeError('Eolian, failed to create Eolian state'))


# eolian system scan (BROKEN)
#  if not state.system_directory_scan():
    #  raise(RuntimeError('Eolian, failed to scan system directories'))

# eolian source tree scan
if not state.directory_scan(SCAN_FOLDER):
    raise(RuntimeError('Eolian, failed to scan source directory'))


# Test various file listing
l = list(state.all_eo_file_paths)
if len(l) < 5 or not l[0].endswith('.eo'):
    raise(RuntimeError('Eolian, failed to get eo file paths list'))
l = list(state.all_eo_files)
if len(l) < 5 or not l[0].endswith('.eo'):
    raise(RuntimeError('Eolian, failed to get eo files list'))
l = list(state.all_eot_file_paths)
if len(l) < 5 or not l[0].endswith('.eot'):
    raise(RuntimeError('Eolian, failed to get eot file paths list'))
l = list(state.all_eot_files)
if len(l) < 5 or not l[0].endswith('.eot'):
    raise(RuntimeError('Eolian, failed to get eot files list'))


# Parse all known eo files
if not state.all_eot_files_parse():
    raise(RuntimeError('Eolian, failed to parse all EOT files'))
    
if not state.all_eo_files_parse():
    raise(RuntimeError('Eolian, failed to parse all EO files'))



# Test a single class (by name and by file)
print('# # # #  Testing Class  # # # # # # # # # # # # # # # # # # # # # # # #')
for cls in (state.class_get_by_name('Efl.Loop.Timer'),
            state.class_get_by_file('efl_loop_timer.eo')):
    print(cls)
    assert isinstance(cls, eolian.Class)
    assert cls.name == 'Timer'
    assert cls.full_name == 'Efl.Loop.Timer'
    assert cls.file == 'efl_loop_timer.eo'
    assert list(cls.namespaces) == ['Efl', 'Loop']
    assert cls.type == eolian.Eolian_Class_Type.REGULAR
    assert isinstance(cls.documentation, eolian.Documentation)
    assert cls.legacy_prefix == 'ecore_timer'
    assert cls.eo_prefix is None  # TODO fin a class with a value
    assert cls.event_prefix is None  # TODO same as above
    assert cls.data_type is None  # TODO same as above
    assert len(list(cls.inherits)) == 1
    assert cls.ctor_enable is False
    assert cls.dtor_enable is False
    assert cls.c_get_function_name == 'efl_loop_timer_class_get'
    assert cls.c_name == 'EFL_LOOP_TIMER_CLASS'
    assert cls.c_data_type == 'Efl_Loop_Timer_Data'
    assert [f.name for f in cls.methods] == ['reset','loop_reset','delay']
    assert [f.name for f in cls.properties] == ['interval','pending']
    assert len(list(cls.implements)) > 5
    assert isinstance(list(cls.implements)[0], eolian.Implement)

    # test eolian.Function
    f = cls.function_get_by_name('delay')
    assert f.name == 'delay'
    assert f.type == eolian.Eolian_Function_Type.METHOD
    assert f.method_scope == eolian.Eolian_Object_Scope.PUBLIC
    assert f.getter_scope == eolian.Eolian_Object_Scope.UNKNOWN  # TODO correct?
    assert f.setter_scope == eolian.Eolian_Object_Scope.UNKNOWN  # TODO correct?
    assert f.full_c_method_name == 'efl_loop_timer_delay'
    assert f.full_c_getter_name == 'efl_loop_timer_delay_get'
    assert f.full_c_setter_name == 'efl_loop_timer_delay_set'
    assert f.full_c_method_name_legacy == 'ecore_timer_delay'
    assert f.full_c_getter_name_legacy == 'ecore_timer_delay_get'
    assert f.full_c_setter_name_legacy == 'ecore_timer_delay_set'
    assert f.method_return_type is None  # TODO correct ?
    assert f.setter_return_type is None  # TODO correct ?
    assert f.getter_return_type is None  # TODO correct ?    
    assert f.is_legacy_only(eolian.Eolian_Function_Type.PROP_GET) is False
    assert f.is_class is False
    assert f.is_beta is False
    assert f.is_constructor(cls) is False
    #  assert f.is_function_pointer == False  # TODO broken somehow
    assert len(list(f.getter_values)) == 1
    assert len(list(f.getter_values)) == 1
    assert len(list(f.parameters)) == 1
    assert f.return_is_warn_unused(eolian.Eolian_Function_Type.METHOD) is False
    assert f.object_is_const is False
    assert f.class_.full_name == 'Efl.Loop.Timer'

    # test eolian.Implement
    im = f.implement
    assert isinstance(im, eolian.Implement)
    assert im.full_name == 'Efl.Loop.Timer.delay'
    assert isinstance(im.class_, eolian.Class)
    assert isinstance(im.function_get(), eolian.Function) # TODO is UNRESOLVED correct ?
    assert isinstance(im.documentation_get(), eolian.Documentation) # TODO is UNRESOLVED correct ?
    assert im.is_auto() is False
    assert im.is_empty() is False
    assert im.is_pure_virtual() is False
    assert im.is_prop_set is False
    assert im.is_prop_get is False

    # test eolian.Parameter
    p = list(f.parameters)[0]
    assert p.direction == eolian.Eolian_Parameter_Dir.IN
    assert p.name == 'add'
    assert p.default_value is None
    assert p.is_nonull is False  # TODO is correct ?? 'add' can be null?
    assert p.is_nullable is False
    assert p.is_optional is False
    assert p.type.name == 'double'
    assert isinstance(p.documentation, eolian.Documentation)
    
    # test eolian.Event
    assert [e.name for e in cls.events] == ['tick']
    ev = cls.event_get_by_name('tick')
    assert isinstance(ev, eolian.Event)
    assert ev.name == 'tick'
    assert ev.c_name == 'EFL_LOOP_TIMER_EVENT_TICK'
    assert ev.type is None  # TODO is this correct
    assert isinstance(ev.documentation, eolian.Documentation)
    assert ev.scope == eolian.Eolian_Object_Scope.PUBLIC
    assert ev.is_beta is False
    assert ev.is_hot is False
    assert ev.is_restart is False


# test eolian.Part
print('# # # #  Testing Part   # # # # # # # # # # # # # # # # # # # # # # # #')
cls = state.class_get_by_name('Efl.Ui.Popup')
parts = list(cls.parts)
assert len(parts) > 0
part = parts[0]
assert part.name == 'backwall'
assert isinstance(part.class_, eolian.Class)
assert part.class_.full_name == 'Efl.Ui.Popup.Part'
assert isinstance(part.documentation, eolian.Documentation)
#  print(part.documentation)


# test eolian.Constructor
print('# # # #  Testing Constructor  # # # # # # # # # # # # # # # # # # # # #')
cls = state.class_get_by_name('Efl.Ui.Win')
ctors = list(cls.constructors)
assert len(ctors) > 0
ctor = ctors[0]
assert isinstance(ctor, eolian.Constructor)
assert ctor.full_name == 'Efl.Ui.Win.win_name'
assert ctor.is_optional is False
assert isinstance(ctor.class_, eolian.Class)
assert ctor.class_.full_name == 'Efl.Ui.Win'
assert isinstance(ctor.function, eolian.Function)
assert ctor.function.name == 'win_name'
#  print(ctor.function)





# test eolian.Typedecl (enum)
print('# # # #  Testing Typedecl (enum)  # # # # # # # # # # # # # # # # # # #')
td = state.typedecl_enum_get_by_name('Efl.Net.Http.Version')
assert isinstance(td, eolian.Typedecl)
assert td.name == 'Version'
assert td.full_name == 'Efl.Net.Http.Version'
assert td.file == 'efl_net_http_types.eot'
assert td.base_type == None  # TODO find a better test
assert td.free_func == None  # TODO find a better test
assert td.function_pointer == None  # TODO find a better test
assert td.is_extern is False
assert list(td.namespaces) == ['Efl','Net','Http']
fields = list(td.enum_fields)
assert len(fields) == 3
assert isinstance(td.documentation, eolian.Documentation)
# test eolian.Enum_Type_Field
field = td.enum_field_get('v1_0')
assert isinstance(field, eolian.Enum_Type_Field)
assert field.name == 'v1_0'
assert field.c_name == 'EFL_NET_HTTP_VERSION_V1_0'
assert isinstance(field.documentation, eolian.Documentation)
assert isinstance(field.value, eolian.Expression)

# test eolian.Expression
print('# # # #  Testing Expression   # # # # # # # # # # # # # # # # # # # # #')
exp = field.value
assert isinstance(exp, eolian.Expression)
assert exp.serialize == '100'
assert exp.type == eolian.Eolian_Expression_Type.INT
#  exp.binary_operator # TODO find a better test (only works for BINARY expr)
#  exp.binary_lhs # TODO find a better test (only works for BINARY expr)
#  exp.binary_rhs # TODO find a better test (only works for BINARY expr)
#  exp.unary_operator # TODO find a better test (only works for UNARY expr)
#  exp.unary_expression # TODO find a better test (only works for UNARY expr)

print("+++", exp.unary_expression)

# test eolian.Variable
print('# # # #  Testing Variable   # # # # # # # # # # # # # # # # # # # # # #')
l = list(state.variable_all_constants)
assert len(l) > 2
assert isinstance(l[0], eolian.Variable)

l = list(state.variable_all_globals)
assert len(l) > 20
assert isinstance(l[0], eolian.Variable)

l = list(state.variable_constants_get_by_file('efl_gfx_stack.eo'))
assert len(l) > 1
assert isinstance(l[0], eolian.Variable)

l = list(state.variable_globals_get_by_file('efl_net_http_types.eot'))
assert len(l) > 10
assert isinstance(l[0], eolian.Variable)

var = l[0]
assert isinstance(var, eolian.Variable)
assert var.full_name == 'Efl.Net.Http.Error.BAD_CONTENT_ENCODING'
assert var.name == 'BAD_CONTENT_ENCODING'
assert var.type == eolian.Eolian_Variable_Type.GLOBAL
assert var.file == 'efl_net_http_types.eot'
assert var.is_extern is False
assert list(var.namespaces) == ['Efl','Net','Http','Error']
assert isinstance(var.documentation, eolian.Documentation)
assert isinstance(var.base_type, eolian.Type)
assert var.value is None  # TODO find a better test

#  print(state.variable_constant_get_by_name(''))  # TODO
#  print(state.variable_global_get_by_name(''))  # TODO


# test eolian.Declaration
print('# # # #  Testing Declaration  # # # # # # # # # # # # # # # # # # # # #')
l = list(state.declarations_get_by_file('eina_types.eot'))
assert len(l) > 10
assert isinstance(l[0], eolian.Declaration)

l = list(state.all_declarations)
assert len(l) > 100
assert isinstance(l[0], eolian.Declaration)

d = state.declaration_get_by_name('Eina.File')
assert isinstance(d, eolian.Declaration)
assert d.name == 'Eina.File'
assert d.type == eolian.Eolian_Declaration_Type.STRUCT
#  assert d.class_ is None  # TODO find a better test
#  assert d.variable is None  # TODO find a better test
assert isinstance(d.data_type, eolian.Typedecl)
assert d.data_type.full_name == 'Eina.File'



# test eolian.Typedecl (struct)
print('# # # #  Testing Typedecl (struct)  # # # # # # # # # # # # # # # # # #')
td = state.typedecl_struct_get_by_name('Efl.Gfx.Color32')
assert isinstance(td, eolian.Typedecl)

fields = list(td.struct_fields)
assert len(fields) == 4
assert [f.name for f in fields] == ['r', 'g', 'b', 'a']

# test eolian.Struct_Type_Field
field = td.struct_field_get('b')
assert isinstance(field, eolian.Struct_Type_Field)
assert field.name == 'b'
assert isinstance(field.type, eolian.Type)
assert isinstance(field.documentation, eolian.Documentation)


# test eolian.Type
print('# # # #  Testing Type   # # # # # # # # # # # # # # # # # # # # # # # #')
t = field.type
assert isinstance(t, eolian.Type)
assert t.name == 'uint8'
assert t.full_name == 'uint8'
assert t.type == eolian.Eolian_Type_Type.REGULAR
assert t.builtin_type == eolian.Eolian_Type_Builtin_Type.UINT8
assert t.file == 'efl_canvas_filter_internal.eo'
assert t.base_type is None  # TODO find a better test
assert t.next_type is None  # TODO find a better test
assert t.is_owned is False
assert t.is_const is False
assert t.is_ptr is False
assert list(t.namespaces) == []   # TODO find a better test
assert t.free_func is None  # TODO find a better test
#  print("****", t.builtin_type)


# test eolian.Documentation
print('# # # #  Testing Documentation  # # # # # # # # # # # # # # # # # # # #')
#  td = state.class_get_by_name('Efl.Ui.Button')
td = state.class_get_by_name('Efl.Net.Control')
doc = td.documentation
assert isinstance(doc, eolian.Documentation)
assert isinstance(doc.summary, str) and len(doc.summary) > 10
assert isinstance(doc.description, str) and len(doc.description) > 20
assert doc.since == '1.19'



# ALL classes
#  print('# ' * 40)
#  for cls in state.all_classes:
    #  print(cls)


# ALL enums
print('# # # #  Testing enums fetchers   # # # # # # # # # # # # # # # # # # #')
enum = state.typedecl_enum_get_by_name('Efl.Orient')
assert isinstance(enum, eolian.Typedecl)

enums = list(state.typedecl_enums_get_by_file('efl_ui_win.eo'))
assert len(enums) > 5

enum_ok = False
for typedecl in state.typedecl_all_enums:
    assert isinstance(typedecl, eolian.Typedecl)
    #  print(typedecl, typedecl.file)
    enum_ok = True
assert enum_ok == True



# ALL structs
print('# # # #  Testing struct fetchers  # # # # # # # # # # # # # # # # # # #')

struct = state.typedecl_struct_get_by_name('Eina.File')
assert isinstance(struct, eolian.Typedecl)

structs = list(state.typedecl_structs_get_by_file('eina_types.eot'))
assert len(structs) > 10

struct_ok = False
for typedecl in state.typedecl_all_structs:
    assert isinstance(typedecl, eolian.Typedecl)
    #  print(typedecl, typedecl.file)
    struct_ok = True
assert struct_ok == True



# ALL aliases
print('# # # #  Testing alias fetchers   # # # # # # # # # # # # # # # # # # #')

alias = state.typedecl_alias_get_by_name('Eina.Error')
assert isinstance(alias, eolian.Typedecl)
assert alias.name == 'Error'

aliases = list(state.typedecl_aliases_get_by_file('edje_types.eot'))
assert len(aliases) > 5

#  for typedecl in state.typedecl_all_aliases:
    #  print(typedecl, typedecl.file)




# Cleanup
del state
print('cool, everything worked as expected :)')
exit(0)









