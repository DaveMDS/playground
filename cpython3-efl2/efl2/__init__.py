# This Python file uses the following encoding: utf-8
#
# Copyright (C) 2007-2016 various contributors (see AUTHORS)
#
# This file is part of Python-EFL.
#
# Python-EFL is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# Python-EFL is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this Python-EFL.  If not, see <http://www.gnu.org/licenses/>.

# semver examples:
# development: "1.12.99" ( 1, 12, 99 )
# pre-release: "1.13.0-beta1" ( 1, 13, 0 )
# release:     "1.13.0" ( 1, 13, 0 )

__version__ = "2.0.0-test1"
__version_info__ = ( 2, 0, 0 )


from ._efl import _Object, _Loop, _Loop_User, system


class Object(_Object):  # Direct subclass of python object
   pass

class Loop(_Loop):  # Direct subclass of efl._Object
   pass

class Loop_User(_Loop_User):  # Direct subclass of efl._Object
   pass
