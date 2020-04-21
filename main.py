#!/usr/bin/env python3

from src import *


def main():
    scene = Scene("shaders/", light_dir=vec(1, 1, 1), camera_dist=230)

    color_shader = scene.shaders['color']
    skinning_shader = scene.shaders['skinning']

    #Generates sur sand surface
    scene.generate_terrain("img/sand.jpg", "img/perlin_noise.png", 200, 1000, -10)
    
    #Generates the water surfacer
    scene.generate_water("img/blue.jpg", 1000)

    boids = Boids(color_shader, 27, "obj/Fish/BlueTang/BlueTang.obj", scaling=0.3, index=0)
    boids_placement = {
        "position": (-10, -10, 200)
    }
    scene.add(boids, place_boids=boids_placement)

    rotation_matrix = rotate((0, 1, 0), 45) @ rotate((1, 0, 0), 45)
    
    anim = {"rotation_control": True, "key_up": glfw.KEY_UP, "key_down": glfw.KEY_DOWN, "axis": (3, 0, 3)}
    keyframe_anim = {
        "keyframes": True,
        "translate_keys": {5: vec(0, 0, 0), 8: vec(1, 1, 0), 15: vec(0, 0, 0)},
        "rotate_keys": {5: quaternion(), 8: quaternion_from_euler(180, 45, 90), 10: quaternion_from_euler(180, 0, 180), 15: quaternion()},
        "scale_keys": {5: 1, 8: 0.5, 15: 1}
    }
    
    #Adding a bird TODO le faire voler autour d'une/des colonne(s) & trouver un oiseau
    flying_bird = Object(color_shader, "Flying Brid", "obj/Fish/NurseShark/NurseShark.obj", position=(50, 30, 0), scaling=(1, 1, 1), tex_file = "obj/Fish/NurseShark/NurseShark_Base_Color.png")
    scene.add(flying_bird, rotation_control=anim, keyframes=keyframe_anim)
    
    #Loading and adding Hercules to the scene TODO Tourver la bonne rotation
    Hercules = Object(color_shader, "Hercules", "obj/others/hercules/Hercules.obj", position=(10, -20, 150), scaling=(0.7, 0.7, 0.7 ), rotation_axis=(1, 0, 0), rotation_angle=-90, tex_file="obj/others/hercules/Hercules.jpg")
    scene.add(Hercules)
    
    #Loading the two columns, ionic and ionic_2
    column = Object(color_shader, "column", "obj/others/ionic/ionic.obj", position=(50, 20, 0), scaling=(0.2, 0.2, 0.2), rotation_axis=(1, 0, 0), rotation_angle=-100)
    column_2 = Object(color_shader, "column_2", "obj/others/ionic/ionic.obj", position=(55, 25, 10), scaling=(0.2, 0.2, 0.2), rotation_axis=(1, 0, 0), rotation_angle=-100)
    #Adding the columns to the scene
    scene.add(column, column_2)
    
    #scene.viewer.add(("seahorse_skinned", *[m for m in load_skinned("obj/Fish/SeaHorse/SeaHorse.fbx", skinning_shader, tex_file="obj/Fish/SeaHorse/SeaHorse_Base_Color.png")]))#, position = (15, -10, 250))
    #seahorse_skinned.set_position(position=(-10, -5, 0), scaling=(0.15, 0.15, 0.15))
    #scene.update_position(seahorse_skinned)

    skybox = Skybox(scene.shaders['skybox'], "img/skybox/right.png", "img/skybox/left.png", "img/skybox/top.png", "img/skybox/bottom.png", "img/skybox/front.png", "img/skybox/back.png")
    scene.add_skybox(skybox)

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
