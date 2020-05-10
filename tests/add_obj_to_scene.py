#!/usr/bin/env python3
"""
Test object adding in a scene and position updating
"""

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

from src import *


def main():
    # Scene creation
    scene = Scene("../shaders/", light_dir=(0, 1, 0), camera_dist=10)

    # Shader
    color_shader = scene.shaders['color']

    # Parameters
    rotation_matrix = rotate((0, 1, 0), 15) @ rotate((1, 0, 0), 45)

    # Objects creation
    suzanne = Object(color_shader, "suzanne", "../obj/others/suzanne/suzanne.obj", light_dir=(0, 1, 1), position=(-1, 0, 0), rotation_axis=(0, 1, 0), rotation_angle=45)
    suzanne_uncolored = Object(color_shader, "suzanne_uncolored", "../obj/others/suzanne/suzanne_uncolored.obj", light_dir=(1, 0, 0), position=(-1, 2, 0), scaling=(1, 0.5, 1))
    cube = Object(color_shader, "cube", "../obj/others/cube/cube.obj", position=(1, 0, 0), rotation_mat=rotation_matrix, light_dir=(1, 0, 0))
    granit_cube = Object(color_shader, "granit_cube", "../obj/others/cube/cube.obj", tex_file="../img/granit.jpg")

    # Adding objects to the scene
    scene.add(suzanne, suzanne_uncolored, cube, granit_cube)

    # Updating position
    granit_cube.set_position(position=(1, 1.5, 0))
    scene.update_position(granit_cube)

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()