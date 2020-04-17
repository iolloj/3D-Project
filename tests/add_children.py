#!/usr/bin/env python3
"""
Test children adding
"""

import sys
# insert at 1, 0 is the script path (or '' in REPL)
sys.path.insert(1, '../')

from src import *


# Maye check that the illumination is propagated to the children
# To do so, an attribute self.light_dir and a method load_mesh should be created but then 
# the method would not be called in the object initialization and would lead to an uglier code
# Or, the object should be created again with the new mesh


def main():
    # Scene creation
    scene = Scene("../shaders/", light_dir=(0, 0, 0), camera_dist=7)

    # Shader
    color_shader = scene.shaders['color']

    # Creating root object
    root = Object(color_shader, "root", "../obj/others/cube/cube.obj", tex_file="../img/granit.jpg")

    # Creating children
    cube = Object(color_shader, "cube", "../obj/others/cube/cube.obj", position=(0, 0.85, 0), scaling=(0.7, 0.7, 0.7))
    bunny1 = Object(color_shader, "bunny1", "../obj/others/bunny/bunny.obj", position=(-0.3, 0.76, 0), scaling=(0.5, 0.5, 0.5), rotation_axis=(0, 1, 0), rotation_angle=45)
    bunny2 = Object(color_shader, "bunny2", "../obj/others/bunny/bunny.obj", position=(0.3, 0.76, 0), scaling=(0.5, 0.5, 0.5), rotation_axis=(0, 1, 0), rotation_angle=45)

    # Adding children to their parents
    root.add(cube)
    cube.add(bunny1, bunny2)
    
    # Adding objects to the scene
    scene.add(root)

    # Updating the position
    root.set_position(position=(0, -0.5, 0))
    scene.update_position(root)

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()
    main()
    glfw.terminate()