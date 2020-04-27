#!/usr/bin/env python3

from src import *


def main():
    scene = Scene("shaders/", light_dir=vec(1, 1, 1), camera_dist=230)

    color_shader = scene.shaders['color']

    scene.generate_terrain("img/sand.jpg", "img/perlin_noise.png", 200, 1000, -10)
    scene.generate_water("img/blue.jpg", 1000)

    boids = Boids(color_shader, 27, "obj/Fish/BlueTang/BlueTang.obj", scaling=0.1, index=0)
    boids_placement = {
        "position": (0, -10, 200)
    }
    scene.add(boids, place_boids=boids_placement)

    rotation_matrix = rotate((0, 1, 0), 45) @ rotate((1, 0, 0), 45)
    anim = {"rotation_control": True, "key_up": glfw.KEY_UP, "key_down": glfw.KEY_DOWN, "axis": (1, 0, 0)}
    keyframe_anim = {
        "keyframes": True,
        "translate_keys": {5: vec(0, 0, 0), 8: vec(1, 1, 0), 15: vec(0, 0, 0)},
        "rotate_keys": {5: quaternion(), 8: quaternion_from_euler(180, 45, 90), 10: quaternion_from_euler(180, 0, 180), 15: quaternion()},
        "scale_keys": {5: 1, 8: 0.5, 15: 1}
    }

    cube1 = Object(color_shader, "cube1", "obj/others/cube/cube.obj", position=(0, 5, 0), rotation_mat=rotation_matrix, scaling=(0.5, 0.3, 0.7))
    cube2 = Object(color_shader, "cube2", 'obj/others/cube/cube.obj', position=(-5, 5, 3), scaling=(2, 2, 2), tex_file="obj/others/column/granit.jpg")
    rabbit1 = Object(color_shader, "rabbit", ".obj/thers/bunny/bunny.obj", position=(0, 1, 0))
    cube3 = Object(color_shader, "suzanne", "obj/others/cube/cube.obj", position=(1, 1, 0))
    rabbit2 = Object(color_shader, "bis", "obj/others/bunny/bunny.obj", position=(0, 1, 0))

    column = Object(color_shader, "column", "obj/others/column/column.obj", position=(0, 15, 15), scaling=(0.005, 0.005, 0.005), rotation_axis=(1, 0, 0), rotation_angle=-45)
    scene.add(column)

    doric = Object(color_shader, "doric", "obj/others/doric/doric.obj", position = (0, -15, 15), scaling=(0.05, 0.05, 0.05))
    scene.add(doric)

    ionic = Object(color_shader, "ionic", "obj/others/ionic/ionic.obj", position=(-10, 10, 0), scaling=(0.05, 0.05, 0.05))
    scene.add(ionic)

    cube2.add(rabbit1)
    cube2.add(cube3, keyframes=keyframe_anim)
    rabbit1.add(rabbit2)

    scene.add(cube1)
    scene.add(cube2, rotation_control=anim, keyframes=keyframe_anim)

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

    skybox = Skybox(scene.shaders['skybox'], "img/skybox/right.png", "img/skybox/left.png", "img/skybox/top.png", "img/skybox/bottom.png", "img/skybox/front.png", "img/skybox/back.png")
    scene.add_skybox(skybox)

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
