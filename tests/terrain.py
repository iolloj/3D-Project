#!/usr/bin/env python3
"""
Test plane creation
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
    scene = Scene("../shaders/", light_dir=(0, 1, 1), camera_dist=100)
    
    # Terrain generation
    scene.generate_terrain("img/sand.jpg", "img/height.jpg", 100, 1000)

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()