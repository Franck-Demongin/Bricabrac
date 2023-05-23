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

class NXBIL_OT_render(bpy.types.Operator):
    bl_idname = "nxbil.render"
    bl_label = "Bake indirect lighting and make render of each frame"
    
    _frame = 0
    _timer = None
    _path = None
    _filepath = None
    _format = ('PNG', 'png')
    _run = False
    
    def execute(self, context):
        scene = context.scene
        scene.render.image_settings.file_format = self._format[0]
        scene.frame_current = self._frame                 
        bpy.ops.scene.light_cache_bake()        
        self._filepath = f"{self._path}{self._frame:04d}.{self._format[1]}"
        scene.render.filepath = self._filepath            
        bpy.ops.render.render(write_still=True)
        self._frame += 1
        self._run = False
        
        return {'FINISHED'}

    def modal(self, context, event):     
        scene = context.scene
        frame_end = scene.frame_end
         
        if event.type == 'ESC':
            context.window_manager.event_timer_remove(self._timer)
            scene.render.filepath = self._path
            self.report({'WARNING'}, f"Exit {self._frame - 1}/{frame_end}")    
            return {'CANCELLED'}        
        elif self._frame > frame_end: 
            context.window_manager.event_timer_remove(self._timer)
            scene.render.filepath = self._path
            self.report({'INFO'}, f"Finish {frame_end}/{frame_end}")    
            return {'FINISHED'}
        if event.type == 'TIMER':            
            if not self._run:
                self._run = True
                self.execute(context)
                areas = [area for area in context.screen.areas if area.type in ['VIEW_3D', 'IMAGE_EDITOR']]
                if len(areas) > 0:
                    area = areas[-1]
                    with context.temp_override(area=area):
                        context.area.type = 'IMAGE_EDITOR'
                        img = bpy.data.images.load(self._filepath, check_existing=False)
                        context.area.spaces.active.image = img                
           
                        
        return {'PASS_THROUGH'}
        

    def invoke(self, context, event):   
        wm = context.window_manager   
        self._frame = context.scene.frame_start 
        if os.path.isdir(context.scene.render.filepath):
            self._path = context.scene.render.filepath
            if not self._path.endswith(os.sep):
                 self._path += os.sep
        else:
            self._path = os.path.splitext(context.scene.render.filepath)[0]
            if not self._path.endswith('_'):
                 self._path += '_'
            
            print(self._path)
        self._timer = wm.event_timer_add(0.1, window=context.window)        
        wm.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}
    

def register():
    bpy.utils.register_class(NXBIL_OT_render)

def unregister():
    bpy.utils.unregister_class(XBIL_OT_render)

if '__main__' in __name__:
    register()
    bpy.ops.nxbil.render('INVOKE_DEFAULT')
