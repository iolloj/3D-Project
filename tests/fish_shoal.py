#!/usr/bin/env python3
"""
Test boids model
"""

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

from src import *


def main():
    # Scene creation
    scene = Scene("../shaders/", light_dir=(0, 0, 0), camera_dist=50)

    # Shader
    skinning_shader = scene.shaders['skinning']

    # Boids
    boids = Boids(skinning_shader, 27, "../obj/Fish/BlueTang/BlueTang.fbx", scaling=0.001, index=0, tex_file="../obj/Fish/BlueTang/BlueTang_Base_Color.png")
   
    scene.add(boids)

    scene.viewer.run()

if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()