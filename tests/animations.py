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
    # scene.viewer.add(("cylinder", SkinnedCylinder(skinning_shader)))
    scene.viewer.add(("test_skinned", *[m for m in load_skinned("../obj/Fish/BottlenoseDolphin/BottleNoseDolphin.fbx", skinning_shader, tex_file="../obj/Fish/BottlenoseDolphin/BottlenoseDolphin_Base_Color.png")]))

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()