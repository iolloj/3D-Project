#!/usr/bin/env python3

from viewer import *
from objects import *
from nodes import *
from meshes import *


def main():
    scene = Scene("../shaders/", vec(0, 1, 0), 10)
    scene.generate_terrain("../tests/img/brown.png", "../tests/img/height.jpg", 10, 100)

    rotation_matrix = rotate((0, 1, 0), 45) @ rotate((1, 0, 0), 45)

    cube1 = Object(scene.shaders['color'], "cube1", "../tests/cube/cube.obj", position=(0, 5, 0), rotation_mat=rotation_matrix, scaling=(0.5, 0.3, 0.7))
    cube2 = Object(scene.shaders['color'], "cube2", '../tests/cube/cube.obj', position=(-5, 5, 3), scaling=(2, 2, 2))
    rabbit1 = Object(scene.shaders['color'], "rabbit", "../tests/bunny/bunny.obj", position=(0, 1, 0))
    cube3 = Object(scene.shaders['color'], "suzanne", "../tests/cube/cube.obj", position=(1, 1, 0))
    rabbit2 = Object(scene.shaders['color'], "bis", "../tests/bunny/bunny.obj", position=(0, 1, 0))

    cube2.add(rabbit1)
    cube2.add(cube3)
    rabbit1.add(rabbit2)

    scene.add(cube1)
    scene.add(cube2)

    cube1.set_position(position=(-10, -5, 0), scaling=(15, 15, 15))
    scene.update_position(cube1)

    cube2.set_position(position=(10, 10, 0), scaling=(10, 10, 10))
    scene.update_position(cube2)

    rabbit1.set_position(position=(-1, 1, 0), scaling=(0.5, 0.5, 0.5))
    scene.update_position(rabbit1)

    cube1.set_position(position=(-9, -5, 0))
    scene.update_position(cube1)

    cube2.set_position(position=(9, 5, 0))
    scene.update_position(cube2)

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
