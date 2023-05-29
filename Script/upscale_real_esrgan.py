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

#----------------------------------------#
# This script use xinntao/Real-ESRGAN-ncnn-vulkan to upscale the images
# You can download it from : https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan/releases
# Choose release for your operating system, unzip the file on your hard drive.
#----------------------------------------#

import os
import subprocess
import bpy

# path to realesrgan-ncnn-vulkan executable.
# on Linux render the file executable
# on Windows, use "/" or "\\" in path
#path_to_real_esrgan = "C:/Users/franck/Documents/Dvp/Real-ESRGAN/realesrgan-ncnn-vulkan.exe"
path_to_real_esrgan = "/home/franck/Softs/Real-ESRGAN/realesrgan-ncnn-vulkan"

# Choose a scale from 2, 3 or 4 
# The render resolution will be divided by this value and then the images scaled by the same ratio.
scale = 4 # 2, 3 or 4

# Render animation (True) or current frame (False)
render_animation = False

# model
models = [
    'realesr-animevideov3',     # 0
    'realesrgan-x4plus',        # 1
    'realesrgan-x4plus-anime',  # 2
]
model_idx = 2

#######################

def poll():
    return bpy.data.is_saved

def get_file_path():    
    filepath = bpy.data.filepath
    return os.path.basename(filepath), os.path.dirname(filepath)

def create_dir(dir_path, dir_name):
    dir = os.path.join(dir_path, dir_name)
    if not os.path.isdir(dir):
        os.mkdir(dir) 
    return dir

def upscale(executable, model, input, output, scale):
    print(executable)
    print(model)
    print(input)
    print(output)
    print(scale)
    
    subprocess.call([
        executable, 
        "-i", 
        input,
        "-o", 
        output,
        "-s",
        str(scale),
        "-n",
        model
    ])

def render_complete(scene):
    settings = scene.upscale_settings
    
    scene.render.resolution_x = settings.initial_x
    scene.render.resolution_y = settings.initial_y
    
    print('Render Complete')
    print('---------------')
    print('Start upscale...')
    print('---------------')
    
    input = settings.render_dir
    output = settings.render_upscaled
    if not settings.render_animation:
        name = f"image_{settings.frame_current:04d}{settings.extension}"
        input = os.path.join(input, name)
        output = os.path.join(output, name)
            
    upscale(
        settings.executable,
        settings.model,
        input, 
        output,
        settings.scale
    )
    print('---------------')    
    print("images upscaled")
        
def main(executable, model, scale, render_animation):
    scene = bpy.context.scene
    settings = scene.upscale_settings
    
    file_name, dir_path = get_file_path()
    render_dir = create_dir(dir_path, f"render_{file_name[:-6]}")
    
    output = os.path.join(render_dir, 'img_')
    if not render_animation:
        output = os.path.join(render_dir, f"image_{scene.frame_current:04d}")
    scene.render.filepath = os.path.join(render_dir, output)
    
    render_upscaled = create_dir(render_dir, f"{model}_x{scale}")
    
    initial_x = scene.render.resolution_x
    initial_y = scene.render.resolution_y
    
    scene.render.resolution_x = round(initial_x / scale)
    scene.render.resolution_y = round(initial_y / scale)
        
    settings.executable = executable
    settings.model = model
    settings.scale = scale
    settings.render_animation = render_animation
    settings.render_dir = render_dir
    settings.render_upscaled = render_upscaled
    settings.frame_current = scene.frame_current
    settings.extension = scene.render.file_extension
    settings.initial_x = initial_x
    settings.initial_y = initial_y
        
    bpy.ops.render.render('INVOKE_DEFAULT', animation=render_animation, write_still=True)
   
       
class UpscaleSettings(bpy.types.PropertyGroup):
    executable: bpy.props.StringProperty()
    model: bpy.props.StringProperty()
    scale: bpy.props.IntProperty(default=4)
    render_animation : bpy.props.BoolProperty()
    render_dir: bpy.props.StringProperty()
    render_upscaled: bpy.props.StringProperty()
    frame_current : bpy.props.IntProperty()
    extension : bpy.props.StringProperty()
    initial_x: bpy.props.IntProperty()
    initial_y : bpy.props.IntProperty()
    

bpy.utils.register_class(UpscaleSettings)

if __name__ == "__main__":    
    bpy.types.Scene.upscale_settings = bpy.props.PointerProperty(type=UpscaleSettings)

    for h in bpy.app.handlers.render_complete:
        if h.__name__ == 'render_complete':
            bpy.app.handlers.render_complete.remove(h)
    bpy.app.handlers.render_complete.append(render_complete)
    
    if not poll():
        raise IOError('The file must be saved')
        
    main(
        executable=path_to_real_esrgan,
        model=models[model_idx],
        scale=scale,
        render_animation=render_animation
    )