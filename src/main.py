#!/usr/bin/env python3

from viewer import *
from objects import *
from nodes import *
from meshes import *

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer(distance=10)

    shader_dir = "../shaders/"
    tests_dir = "../tests/"

    shader = Shader(shader_dir + "color.vert", shader_dir + "color.frag")
    terrain_shader = Shader(shader_dir + "terrain.vert", shader_dir + "terrain.frag")

    translate_keys = {5: vec(0, 0, 0), 8: vec(1, 1, 0), 15: vec(0, 0, 0)}
    rotate_keys = {5: quaternion(), 8: quaternion_from_euler(180, 45, 90),
                   10: quaternion_from_euler(180, 0, 180), 15: quaternion()}
    scale_keys = {5: 1, 8: 0.5, 15: 1}

    light_dir = vec(-1, 0, 1)

    # floor
    terrain = Terrain(tests_dir + "img/brown.png", tests_dir + "img/height.jpg", terrain_shader, light_dir=light_dir, k_d=(0.3, 0.3, 0), size=100)
    viewer.add(terrain)

    # lapin pas éclairé
    rabbit = Node(transform=translate(0, 1, 0))
    rabbit_rotation = RotationControlNode(glfw.KEY_RIGHT, glfw.KEY_LEFT, (0, 1, 0))
    rabbit.add(*[mesh for mesh in load(tests_dir + "bunny/bunny.obj", shader)])
    rabbit_rotation.add(rabbit)

    cube = Node(transform=rotate((0, 1, 0), 45))
    cube_rotation = RotationControlNode(glfw.KEY_DOWN, glfw.KEY_UP, (1, 0, 0))
    cube.add(rabbit_rotation, *[mesh for mesh in load(tests_dir + "cube/cube.obj", shader, light_dir)])
    cube_rotation.add(cube)

    cube_translation = Node(transform=translate(0, 1.5, 0))
    cube_translation.add(cube_rotation)

    keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(cube_translation)

    # chargement d'un objet sans texture
    suzanne = Node(transform=translate(-2.5, 0, 0))
    suzanne.add(*[mesh for mesh in load(tests_dir + "suzanne/suzanne.obj", shader, light_dir)])
    viewer.add(suzanne)

    # chargement d'un objet sans texture et sans couleur
    suzanne_uncolored = Node(transform=translate(-2.5, 2, 0) @ scale(0.6, 0.6, 0.6))
    suzanne_uncolored.add(*[mesh for mesh in load(tests_dir + "suzanne/suzanne_uncolored.obj", shader, light_dir)])
    viewer.add(suzanne_uncolored)

    viewer.add(keynode)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
