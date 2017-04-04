/*
 * Just a simple playground for testing eolian functionalities.
 *
 * Build:
 * gcc test_eolian.c -o test_eolian -DEFL_BETA_API_SUPPORT=1 -DEFL_EO_API_SUPPORT=1  `pkg-config --libs --cflags eolian eina`
 *
 */

#include <Eina.h>
#include <Eolian.h>


int main(void)
{
   eina_init();
   eolian_init();

   if (!eolian_system_directory_scan())
   {
      printf("Failed to scan system directories");
      return 1;
   }

   if (!eolian_all_eo_files_parse())
   {
      printf("Failed to parse all EO files\n");
      return 1;
   }

   if (!eolian_all_eot_files_parse())
   {
      printf("Failed to parse all EOT files");
      return 1;
   }

   if (!eolian_database_validate())
   {
      printf("Failed to valiadte the DB");
      return 1;
   }


   const Eolian_Class *cls = eolian_class_get_by_name("Efl.Gfx");
   printf("Class: '%s'\n", eolian_class_full_name_get(cls));

   const Eolian_Function *func;
   Eina_Iterator *iter = eolian_class_functions_get(cls, EOLIAN_PROPERTY);
   EINA_ITERATOR_FOREACH(iter, func)
   {
      printf("  func: '%s'\n", eolian_function_name_get(func));

      Eolian_Function_Parameter *value;
      Eina_Iterator *iter2 = eolian_property_values_get(func, EOLIAN_PROP_GET);
      EINA_ITERATOR_FOREACH(iter2, value)
      {
         printf("     param: '%s'\n", eolian_parameter_name_get(value));
      }
   }


   eolian_shutdown();
   eina_shutdown();
   return 0;
}

