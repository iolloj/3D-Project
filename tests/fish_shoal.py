#!/usr/bin/env python3
"""
Test boids model
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
    scene = Scene("../shaders/", light_dir=(0, 0, 0), camera_dist=50)

    # Shader
    color_shader = scene.shaders['color']

    # Boids
    boids = Boids(color_shader, 27, "obj/LionFish/LionFish.obj", scaling=0.1, index=0)
    
    scene.add(boids)

    scene.viewer.run()

if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()