#!/usr/bin/env python3
"""
Animations testing
"""

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

from src import *


def main():
    # Scene creation
    scene = Scene("../shaders/", light_dir=(0, 1, 0), camera_dist=1500)

    # Shader
    skinning_shader = scene.shaders['skinning']

    # Objects
    dolphin = Object(skinning_shader, "dolphin", "../obj/Fish/BottlenoseDolphin/BottleNoseDolphin.fbx", tex_file="../obj/Fish/BottlenoseDolphin/BottlenoseDolphin_Base_Color.png", animated=True)
    scene.add(dolphin)

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()