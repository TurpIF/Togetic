#!/usr/bin/env python

import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', required=True, metavar='input', type=str,
        help='Filename of the socket to read in')
parser.add_argument('--blender', required=True, metavar='blender', type=str,
        help='Filename of the blender file to use')
parsed_args = parser.parse_args()

# shortcuts for command-line args
addr = parsed_args.input
blender_file = parsed_args.blender

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
