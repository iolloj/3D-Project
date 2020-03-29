#!/usr/bin/env python3

from viewer import *
from terrain import *

# -------------- main program and scene setup --------------------------------
def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer(distance=10)
    shader = Shader("color.vert", "color.frag")
    terrain_shader = Shader("terrain.vert", "terrain.frag")


    translate_keys = {0: vec(0, 0, 0), 2: vec(1, 1, 0), 4: vec(0, 0, 0)}
    rotate_keys = {0: quaternion(), 2: quaternion_from_euler(180, 45, 90),
                   3: quaternion_from_euler(180, 0, 180), 4: quaternion()}
    scale_keys = {0: 1, 2: 0.5, 4: 1}

    light_dir = vec(-1, 0, 1)

    # lapin pas éclairé
    rabbit = Node(transform=translate(0, 1, 0))
    rabbit_rotation = RotationControlNode(glfw.KEY_RIGHT, glfw.KEY_LEFT, (0, 1, 0))
    rabbit.add(*[mesh for mesh in load("bunny/bunny.obj", shader)])
    rabbit_rotation.add(rabbit)

    cube = Node(transform=rotate((0, 1, 0), 45))
    cube_rotation = RotationControlNode(glfw.KEY_UP, glfw.KEY_DOWN, (1, 0, 0))
    cube.add(rabbit_rotation, *[mesh for mesh in load("cube/cube.obj", shader, light_dir)])
    cube_rotation.add(cube)

    keynode = KeyFrameControlNode(translate_keys, rotate_keys, scale_keys)
    keynode.add(cube_rotation)

    # chargement d'un objet sans texture
    suzanne = Node(transform=translate(-2.5, 0, 0))
    suzanne.add(*[mesh for mesh in load("suzanne/suzanne.obj", shader, light_dir)])
    viewer.add(suzanne)

    # chargement d'un objet sans texture et sans couleur
    suzanne_uncolored = Node(transform=translate(-2.5, 2, 0) @ scale(0.6, 0.6, 0.6))
    suzanne_uncolored.add(*[mesh for mesh in load("suzanne/suzanne_uncolored.obj", shader, light_dir)])
    viewer.add(suzanne_uncolored)

    viewer.add(keynode)

    terrain = Terrain("img/sand.png", "height.jpg", terrain_shader, light_dir=light_dir, k_d=(0.3, 0.3, 0))
    viewer.add(terrain)

    # start rendering loop
    viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
