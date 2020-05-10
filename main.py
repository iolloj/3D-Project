#!/usr/bin/env python3

from src import *


def main():
    scene = Scene("shaders/", light_dir=vec(0, 1, 0), camera_dist=230)

    color_shader = scene.shaders['color']
    skinning_shader = scene.shaders['skinning']

    print("Loading...")

    #Generates sur sand surface
    scene.generate_terrain("img/sand.jpg", "img/perlin_noise.png", 200, 1000, -10, "img/sun_Mapping.jpg")
    
    #Generates the water surfacer
    scene.generate_water("img/blue.jpg", 1000)
    boids = Boids(skinning_shader, 19, "obj/Fish/BlueTang/BlueTang.fbx", scaling=0.003, index=0, tex_file="obj/Fish/BlueTang/BlueTang_Base_Color.png")
    boids_placement = {
        "position": (-5, -15, 200)
    }
    scene.add(boids, place_boids=boids_placement)

    rotation_matrix = rotate((0, 1, 0), 45) @ rotate((1, 0, 0), 45)
    rotation_bird = rotate((1, 0, 0), 90) @ rotate((0, 1, 0), 45) @ rotate((0, 0, 1), 30)
    
    anim = {"rotation_control": True, "key_up": glfw.KEY_LEFT, "key_down": glfw.KEY_RIGHT, "axis": (0, 0, 1)}
    keyframe_anim = {
        "keyframes": True,
        "translate_keys": {5: vec(0, 0, 0), 8: vec(1, 1, 0), 15: vec(0, 0, 0)},
        "rotate_keys": {5: quaternion(), 8: quaternion_from_euler(180, 45, 90), 10: quaternion_from_euler(180, 0, 180), 15: quaternion()},
        "scale_keys": {5: 1, 8: 0.5, 15: 1}
    }

    dolphin_keyframes = {
        "keyframes": True,
        "translate_keys": {30: vec(-300, 0, 0), 60: vec(-20, 0, -350), 90: vec(480, 0, 150), 120: vec(0, 0, 350)},
        "rotate_keys": {30: quaternion_from_axis_angle((0, 1, 0), 100), 60: quaternion_from_axis_angle((0, 1, 0), 100), 60.1: quaternion_from_axis_angle((0, 1, 0), 0), 90: quaternion_from_axis_angle((0, 1, 0), 0),  90.1: quaternion_from_axis_angle((0, 1, 0), -115)},
        "scale_keys": {0: 1}
    }
    
    dolphin = Object(skinning_shader, "dolphin", "obj/Fish/BottlenoseDolphin/BottleNoseDolphin.fbx", scaling=(0.01, 0.01, 0.01), rotation_axis=(0, 1, 0), rotation_angle=45, tex_file="obj/Fish/BottlenoseDolphin/BottlenoseDolphin_Base_Color.png", animated=True)
    scene.add(dolphin, keyframes=dolphin_keyframes)

    #Loading and adding Hercules to the scene
    Hercules = Object(color_shader, "Hercules", "obj/others/hercules/Hercules.obj", position=(10, -20, 150), scaling=(0.7, 0.7, 0.7 ), rotation_axis=(1, 0, 0), rotation_angle=-90, tex_file="obj/others/hercules/Hercules.jpg")
    scene.add(Hercules)
    
    #Loading the two columns
    column = Object(color_shader, "column", "obj/others/ionic/ionic.obj", position=(50, 20, 0), scaling=(0.2, 0.2, 0.2), rotation_axis=(1, 0, 0), rotation_angle=-100)
    column_2 = Object(color_shader, "column_2", "obj/others/ionic/ionic.obj", position=(55, 25, 10), scaling=(0.2, 0.2, 0.2), rotation_axis=(1, 0, 0), rotation_angle=-100)
    
    #Adding the columns to the scene
    scene.add(column, column_2)
    
    #seaweeds
    seaweed = Object(color_shader, "seaweed", "obj/others/seaweed/seaweed.dae", position=(5, -35, 145), scaling=(5, 5, 5), rotation_axis=(0, 1, 0), rotation_angle=-100, tex_file = "obj/others/seaweed/seaweed.png" )
    seaweed_2 = Object(color_shader, "seaweed_2", "obj/others/seaweed/seaweed.dae", position=(0, -35, 150), scaling=(5, 5, 5), rotation_axis=(0, 1, 0), rotation_angle=-100, tex_file = "obj/others/seaweed/seaweed.png" )
    seaweed_3 = Object(color_shader, "seaweed_3", "obj/others/seaweed/seaweed.dae", position=(10, -35, 155), scaling=(5, 5, 5), rotation_axis=(0, 1, 0), rotation_angle=-100, tex_file = "obj/others/seaweed/seaweed.png" )
    seaweed_4 = Object(color_shader, "seaweed_4", "obj/others/seaweed/seaweed.dae", position=(-10, -35, 155), scaling=(5, 5, 5), rotation_axis=(0, 1, 0), rotation_angle=-100, tex_file = "obj/others/seaweed/seaweed.png" )
    seaweed_5 = Object(color_shader, "seaweed_5", "obj/others/seaweed/seaweed.dae", position=(-5, -38, 160), scaling=(5, 5, 5), rotation_axis=(0, 1.2, 0), rotation_angle=-100, tex_file = "obj/others/seaweed/seaweed.png" )
    scene.add(seaweed, seaweed_2, seaweed_3, seaweed_4, seaweed_5)
        
    
    #Flying bird around the columns
    flying_bird = Object(color_shader, "Flying Brid", "obj/others/bird/base.fbx", position=(100, 100, 120), scaling=(3, 3, 3), rotation_mat=rotation_bird, tex_file = "obj/others/bird/body_baseColor.png")
    column.add(flying_bird, rotation_control=anim)
    
    #animated seahorse
    seahorse = Object(skinning_shader, "seahorse", "obj/Fish/SeaHorse/SeaHorse.fbx", position=(5, -20, 150), scaling=(0.02, 0.02, 0.02), rotation_axis=(0, 1, 0), rotation_angle=-90, tex_file="obj/Fish/SeaHorse/SeaHorse_Base_Color.png", animated=True)
    scene.add(seahorse)

    #animated fish
    reefFish = Object(skinning_shader, "reefFish", "obj/Fish/ReefFish20/reeffish20.fbx", position=(-25, -8, 140), scaling=(0.02, 0.02, 0.02), rotation_axis=(0, 1, 0), rotation_angle=-90, tex_file="obj/Fish/ReefFish20/ReefFish20_Base_Color.png", animated=True)
    scene.add(reefFish)
    
    #nenuphar
    lotus = Object(scene.shaders['waterlily'], "lotus", "obj/others/lotus/Lotus.fbx",position=(-5, 0, 140), tex_file = "obj/others/lotus/LotusDiffuse.png")
    scene.add(lotus)
    

    # Hierarchical keyboard control
    rotation_matrix = rotate((0, 1, 0), 45) @ rotate((1, 0, 0), 45)
    x_rotation = {"rotation_control": True,
                  "key_up": glfw.KEY_DOWN,
                  "key_down": glfw.KEY_UP,
                  "axis": (1, 0, 0)
                 }
    y_rotation = {"rotation_control": True,
                  "key_up": glfw.KEY_RIGHT,
                  "key_down": glfw.KEY_LEFT,
                  "axis": (0, 1, 0)
                 }

    # cube_root = Object(color_shader, "cube_root", "obj/others/cube/cube.obj", position=(10, -50, 200), scaling=(0.0001, 0.0001, 0.0001))
    # granit_cube = Object(color_shader, "granit_cube", "obj/others/cube/cube.obj", scaling=(1e5, 1e5, 1e5), tex_file="img/granit.jpg")
    # cube = Object(color_shader, "cube", "obj/others/cube/cube.obj", position=(0, 0.85, 0), scaling=(0.7, 0.7, 0.7))

    # granit_cube.add(cube, rotation_control=y_rotation)
    # cube_root.add(granit_cube, rotation_control=x_rotation)
    # scene.add(cube_root)
    
    
    # Skybox
    skybox = Skybox(scene.shaders['skybox'], "img/skybox/right.png", "img/skybox/left.png", "img/skybox/top.png", "img/skybox/bottom.png", "img/skybox/front.png", "img/skybox/back.png")
    scene.add_skybox(skybox)

    print("Scene successfully loaded")

    scene.viewer.run()


if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts
