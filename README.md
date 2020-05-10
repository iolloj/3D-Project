# 3D project: Underwater scene

This project aims to create an ocean / underwater scene using 3D graphics techniques including modeling, rendering, animation and interaction.

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

To run the app, you will need to install [Assimp](https://www.assimp.org/) and [AssimpCy](https://pypi.org/project/AssimpCy/).

### Installing

This app does not need to be installed, it can already be run.

## Features

The following features have been implemented:

* Textures [Group]
* Illumination (Phong model) [Group]
* Animation (keyboard control, keyframes, FBX files) [Carole]
* Skybox [Carole]
* Non flat terrain (heightmaps) [Thomas]
* Water surface (Gerstner waves) [Jacopo]
* Water caustics [Jacopo]
* Underwater effects (fog, blue color) [Thomas]
* Boids model [Thomas]

## Running the tests

Here is how to run the tests and the app.

### General tests

General tests can be found in the `tests` repository. They test the features individually.

```
cd tests
python3 <TEST_NAME>
```

The exhaustive list of test programs is the following:

 * `add_children.py`: test of the hierarchical structure of classes `Scene` and `Object` using nodes
 * `add_obj_to_scene.py`: test of the mesh loaders and the method `add` from class `Scene`
 * `animations.py`: test of the animation loader (FBX files); the part $y \leq 0$ is attenuated by a fog (underwater effect)
 * `control_and_keyframes.py`: test of keyboard control and keyframe animations
 * `fish_shoal.py`: test of the boids model on a fish shoal
 * `skybox.py`: test of the skybox
 * `terrain.py`: test of the terrain
 * `water.py`: test of the water surface and objects following the water level

### App

To run the app, go to the root of the project. If you were in the `tests` repository you first have to change the current repository. Enter the following command lines:

```
cd <PATH_TO_ROOT>
python3 main.py
```

## Remarks

Here are some remarks on the projects and some improvement ideas.

### Difficulties

* We encountered some difficulties in direct link with the quarantine: it was not easy to correctly follow the lectures and to do the practicals, as we could not have the same interaction and explanations as before. We managed to implement our solutions and our project, but it took more time than it should normally have.
* Creating the structure of the code so as to be able to add objects to the scene without manipulating low level functionalities was long and not that easy.

### Possible extensions

* Improving the boids model using englobing spheres
* Using spline interpolation instead of linear interpolation for the keyframes
* Postprocessing for the underwater effects by creating a texture and applying filters on it (blue filter for instance)
* Tessellation for the water surface computation to be faster, using an intermediate tessellation control shader
* Normal mapping and shadow mapping
* Physically based rendering to take roughness and metalness into account for example

## Authors

* **Thomas Bauer** - [Pfaffien](https://github.com/Pfaffien)
* **Carole Bellet** - [bellecar](https://github.com/bellecar)
* **Jacopo Iollo** - [Jacopo Iollo](https://github.com/iolloj)