#!/usr/bin/env python3
"""
Test keyboard control and keyframe animation
"""

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

from src import *


def main():
    # Scene creation
    scene = Scene("../shaders/", light_dir=(0, 0, 0), camera_dist=7)

    # Shader
    color_shader = scene.shaders['color']

    # Parameters
    rotation_matrix = rotate((0, 1, 0), 45) @ rotate((1, 0, 0), 45)
    x_rotation = {"rotation_control": True,
                  "key_up": glfw.KEY_DOWN,
                  "key_down": glfw.KEY_UP,
                  "axis": (1, 0, 0)
                 }
    y_rotation = {"rotation_control": True,
                  "key_up": glfw.KEY_RIGHT,
                  "key_down": glfw.KEY_LEFT,
                  "axis": (0, 1, 0)
                 }
    keyframe_anim = {"keyframes": True,
                     "translate_keys": {1: vec(0, 0, 0), 4: vec(1, 1, 0), 9: vec(0, 0, 0)},
                     "rotate_keys": {1: quaternion(), 4: quaternion_from_euler(180, 45, 90), 7: quaternion_from_euler(180, 0, 180), 9: quaternion()},
                     "scale_keys": {1: 1, 4: 0.4, 9: 1}
                    }

    # Objects creation
    granit_cube = Object(color_shader, "granit_cube", "../obj/others/cube/cube.obj", tex_file="../img/granit.jpg")
    cube = Object(color_shader, "cube", "../obj/others/cube/cube.obj", position=(0, 0.85, 0), scaling=(0.7, 0.7, 0.7))

    # Adding children
    granit_cube.add(cube, keyframes=keyframe_anim, rotation_control=y_rotation)
    scene.add(granit_cube, keyframes=keyframe_anim, rotation_control=x_rotation)

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()