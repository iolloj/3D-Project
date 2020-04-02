#!/usr/bin/env python3
"""
Test children adding
"""

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../src/')

from viewer import *
from objects import *
from nodes import *
from meshes import *


def main():
    # Scene creation
    scene = Scene("../shaders/", light_dir=(0, 0, 0), camera_dist=7)

    # Shader
    color_shader = scene.shaders['color']

    # TODO
    # Parameters
    rotation_matrix = rotate((0, 1, 0), 45) @ rotate((1, 0, 0), 45)
    anim = {"rotation_control": True,
            "key_up": glfw.KEY_UP,
            "key_down": glfw.KEY_DOWN,
            "axis": (1, 0, 0)
           }
    keyframe_anim = {"keyframes": True,
                     "translate_keys": {5: vec(0, 0, 0), 8: vec(1, 1, 0), 15: vec(0, 0, 0)},
                     "rotate_keys": {5: quaternion(), 8: quaternion_from_euler(180, 45, 90), 10: quaternion_from_euler(180, 0, 180), 15: quaternion()},
                     "scale_keys": {5: 1, 8: 0.5, 15: 1}
                    }

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()