#!/usr/bin/env python
import subprocess

# TODO use argparse to set these variables
addr = '/tmp/togetic-blender'
blender_file = './base.blend'

python_script = ''
python_script += 'import bpy\n'
python_script += 'import time\n'
python_script += 'bpy.types.Scene.socket_address = '
python_script += 'bpy.props.StringProperty('
python_script += 'name="socket_address", default="' + addr + '")\n'
python_script += 'for area in bpy.context.screen.areas:\n'
python_script += '  if area.type == "VIEW_3D":\n'
python_script += '    area.spaces[0].region_3d.view_perspective = "CAMERA"\n'
# python_script += 'bpy.context.area.type = "VIEW_3D"\n'
# python_script += 'bpy.ops.view3d.zoom_camera_1_to_1()\n'
python_script += 'bpy.ops.wm.window_fullscreen_toggle()\n'
python_script += 'bpy.context.scene.game_settings.use_auto_start = True\n'

script_file = addr + '.py'
script = open(script_file, 'w')
script.write(python_script)
script.close()

# TODO find a way to avoid the black line around the game
subprocess.call(['blender', blender_file, '--python', script_file])
