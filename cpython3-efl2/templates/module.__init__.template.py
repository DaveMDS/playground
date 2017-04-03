<!--(include)-->copyright_py.include<!--(end)-->#!
<!--(include)-->macros.include<!--(end)-->#!

import efl2 as efl
<!--(for cls in classes)-->
from ._${namespaces[-1].lower()}$ import _${cls.name}$
<!--(end)-->


<!--(for cls in classes)-->
class ${cls.name}$(_${cls.name}$#!
   <!--(for i, base in enumerate(cls.inherits))-->
      <!--(if i > 10)-->#! TODO "i > 0" TODO "i > 0" TODO "i > 0" TODO "i > 0"
, ${CLS_TP_NAME(cls=base)}$#!
      <!--(end)-->
   <!--(end)-->
):  # Direct subclass of ${cls.base_class.full_name}$
   pass

<!--(end)-->
