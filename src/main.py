#!/usr/bin/env python3

from viewer import *
from objects import *
from nodes import *
from meshes import *


def main():
    scene = Scene("../shaders/", light_dir=vec(0, 0, 1), camera_dist=100)

    color_shader = scene.shaders['color']

    #scene.generate_terrain("../others/img/sand.jpg", "../others/img/height.jpg", 10, 100)
    scene.generate_water("../others/img/blu.jpg", 100)
    # Boids
    boids = Boids(color_shader, 27, "../obj/Fish/LionFish/LionFish.obj", scaling=0.1, index=0)
    
    #scene.add(boids)

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
