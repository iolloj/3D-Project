#!/usr/bin/env python3
"""
Test skybox creation
"""

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

from src import *


def main():
    # Scene creation
    scene = Scene("../shaders/", light_dir=(1, 1, 1), camera_dist=3000)

    # Shader
    skybox_shader = scene.shaders['skybox']

    # Scene
    skybox = Skybox(skybox_shader, "../img/skybox/right.png", "../img/skybox/left.png", "../img/skybox/top.png", "../img/skybox/bottom.png", "../img/skybox/front.png", "../img/skybox/back.png")
    
    scene.add_skybox(skybox)
    
    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()
