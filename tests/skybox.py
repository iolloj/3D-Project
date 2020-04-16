#!/usr/bin/env python3
"""
Test skybox creation
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
    scene = Scene("../shaders/", light_dir=(0, 1, 1), camera_dist=2000)

    skybox = Skybox(scene.shaders['skybox'], "../img/skybox/right.png", "../img/skybox/left.png", "../img/skybox/top.png", "../img/skybox/bottom.png", "../img/skybox/back.png", "../img/skybox/front.png")
    scene.generate_terrain("img/sand.jpg", "img/perlin_noise.png", 2000, 10000)

    scene.viewer.add_skybox(skybox)
    
    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()