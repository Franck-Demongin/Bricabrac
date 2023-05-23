# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import bpy

PATH = "/home/franck/Bureau/"

objs = [o for o in bpy.context.scene.objects if o.type == 'MESH' and  o.visible_get() == True and not o.hide_viewport]

for o in objs:
    bpy.ops.object.select_all(action='DESELECT')
    o.select_set(True)
    bpy.context.view_layer.objects.active = o
    filepath = os.path.join(PATH, o.name)
    bpy.ops.export_scene.gltf(
        filepath=filepath, 
        export_format='GLB',
        use_selection=True, 
        export_apply=True
    )
