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
    scene = Scene("../shaders/", light_dir=(0, 0, 0), camera_dist=15)

    # Shader
    color_shader = scene.shaders['color']

    # Boids
    boids = Boids(color_shader, 27, "obj/LionFish/LionFish.obj", scale=0.1, index=0)
    pos = {"scaling": (2, 2, 2),
           "rotation_axis": (0, 1, 0),
           "rotation_angle": -45
          }
    
    scene.add(boids, place_boids=pos)

    scene.viewer.run()

if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()