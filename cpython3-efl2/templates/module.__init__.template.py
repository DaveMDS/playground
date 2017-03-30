<!--(include)-->copyright_py.include<!--(end)-->#!
<!--(include)-->macros.include<!--(end)-->#!

<!--(for cls in classes)-->
from ._${namespaces[-1].lower()}$ import _${cls.name}$
<!--(end)-->


<!--(for cls in classes)-->
class ${cls.name}$(_${cls.name}$):  # Direct subclass of ${cls.base_class.full_name}$
   pass

<!--(end)-->
