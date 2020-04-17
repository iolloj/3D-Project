#!/usr/bin/env python3
"""
Test plane creation
"""

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

from src import *


def main():
    # Scene creation
    scene = Scene("../shaders/", light_dir=(0, 1, 1), camera_dist=2000)
    
    # Terrain generation
    scene.generate_terrain("../img/sand.jpg", "../img/perlin_noise.png", 2000, 10000)

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()