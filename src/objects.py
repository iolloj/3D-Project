#!/usr/bin/env python3
"""
Python OpenGL practical application.
petit souci avec la lumière on dirait, pour la direction?
peut-etre probleme lie aux normales
"""

import copy
import random

from viewer import *
from meshes import *
from nodes import *


class Scene:
    """ General scene class """
    def __init__(self, shaders_dir, light_dir, camera_dist):
        """ Maybe add rotations in the viewer initialisation """
        self.viewer = Viewer(distance = camera_dist)
        self.shaders = {'color': Shader(shaders_dir+"color.vert", shaders_dir+"color.frag"),
                        'terrain': Shader(shaders_dir+"terrain.vert", shaders_dir+"terrain.frag")}
        self.node = Node()
        self.viewer.add(("root", self.node))
        self.light_dir = light_dir
        self.terrain = None

    def generate_terrain(self, texture, height, max_height, size):
        self.terrain = Terrain(texture, height, self.shaders['terrain'], max_height=max_height, size=size,
                               light_dir=self.light_dir)
        self.viewer.add(("terrain", self.terrain))

    def add(self, *objects, **animation):
        """
        Other arguments than obj have to be named and the named arguments have to be 
        called either rotation_control or keyframes
        """
        for obj in objects:
            # check if the arguments have valid names
            try:
                names = ["rotation_control", "keyframes", "place_boids"]
                for key in animation.keys():
                    if key not in names:
                        raise KeyError
            except KeyError:
                print("KeyError: expected names 'rotation_control', 'keyframes' or 'place_boids' in Scene.add()")
                raise
                sys.exit(1)

            # placing the boids in the scene
            if isinstance(obj, Boids):
                transform = identity()
                if "place_boids" in animation.keys():
                    place_boids = animation['place_boids']
                    if "position" in place_boids.keys():
                        boid_position = translate(place_boids['position'])
                    else:
                        boid_position = identity()
                    if "scaling" in place_boids.keys():
                        boid_scaling = scale(place_boids['scaling'])
                    else:
                        boid_scaling = identity()
                    if "rotation_axis" and "rotation_angle" in place_boids.keys():
                        boid_rotation = rotate(place_boids['rotation_axis'], place_boids['rotation_angle'])
                    else:
                        boid_rotation = identity()
                    transform = boid_position @ boid_rotation @ boid_scaling
                new_node = Node(transform=transform)
                new_node.add(("boids"+str(obj.index), obj))
                self.node.add(("Boid"+str(obj.index), new_node))

            # placing the objects in the scene
            else:
                obj.parent = self
                # update the dictionaries
                if "rotation_control" in animation.keys():
                    obj.rotation_control.update(animation['rotation_control'])
                if "keyframes" in animation.keys():
                    obj.keyframes.update(animation['keyframes'])
                name = obj.name
                tmp = name + "_tmp"
                rot = name + "_rot"
                keyframe = name + "_keyframe"
                new_node = Node(transform=obj.transform)
                new_node.add((tmp, obj))
                if obj.rotation_control['rotation_control']:
                    rotation_node = RotationControlNode(obj.rotation_control['key_up'], obj.rotation_control['key_down'],
                                                        obj.rotation_control['axis'], obj.rotation_control['angle'])
                    rotation_node.add((rot, new_node))
                    # add another node if there is a keyframe animation
                    if obj.keyframes['keyframes']:
                        keynode = KeyFrameControlNode(obj.keyframes['translate_keys'], obj.keyframes['rotate_keys'],
                                                    obj.keyframes['scale_keys'])
                        keynode.add((rot, rotation_node))
                        self.node.add((keyframe, keynode))
                    else:
                        self.node.add((name, rotation_node))
                else:
                    # add another node if there is a keyframe animation
                    if obj.keyframes['keyframes']:
                        keynode = KeyFrameControlNode(obj.keyframes['translate_keys'], obj.keyframes['rotate_keys'],
                                                    obj.keyframes['scale_keys'])
                        keynode.add((name, new_node))
                        self.node.add((keyframe, keynode))
                    else:
                        self.node.add((name, new_node))

    def update_position(self, obj):
        """ The entry in the dictionary is replaced """
        obj.parent.add(obj, rotation_control=obj.rotation_control)


class Object:
    """ Generic object """
    def __init__(self, shader, name, obj_pos=None, light_dir=(0, 0, 0), position=(0, 0, 0), scaling=(1, 1, 1), rotation_axis=(0, 0, 0), rotation_angle=0, rotation_mat=None, tex_file=None):
        # Maybe using **kwargs to pass a dictionary
        self.name = name
        self.parent = None
        if obj_pos is not None:
            self.mesh = load(obj_pos, shader, light_dir, tex_file)
        else:
            self.mesh = None
        self.translation = translate(position)
        self.scale = scale(scaling)
        if rotation_mat is None:
            self.rotation = rotate(rotation_axis, rotation_angle)
        else:
            self.rotation = rotation_mat
        self.transform = self.translation @ self.rotation @ self.scale
        self.node = Node()
        self.rotation_control = {"rotation_control": False, "key_up": glfw.KEY_RIGHT, "key_down": glfw.KEY_LEFT,
                                 "axis": (0, 1, 0), "angle": 0}
        self.keyframes = {"keyframes": False, "translate_keys": None, "rotate_keys": None, "scale_keys": None}

    def set_position(self, **kwargs):
        """ Position has to be updated in the scene class """
        # check if the arguments have valid names
        try:
            names = ["position", "scaling", "rotation_axis", "rotation_angle", "rotation_mat"]
            for key in kwargs.keys():
                if key not in names:
                    raise KeyError
        except KeyError:
            print("KeyError: expected names 'position', 'scaling', 'rotation_axis', 'rotation_angle' or 'rotation_mat' in Object.set_position()")
            raise
            sys.exit(1)
        if "position" in kwargs.keys():
            self.translation = translate(kwargs['position'])
        if "scaling" in kwargs.keys():
            self.scale = scale(kwargs['scaling'])
        if "rotation_axis" in kwargs.keys() and "rotation_angle" in kwargs.keys():
            self.rotation = rotate(kwargs['rotation_axis'], kwargs['rotation_angle'])
        if "rotation_mat" in kwargs.keys():
            self.rotation = kwargs['rotation_mat']
        self.transform = self.translation @ self.rotation @ self.scale

    def add(self, *objects, **animation):
        """
        Other arguments than obj have to be named and the named arguments have to be 
        called either rotation_control or keyframes
        """
        for obj in objects:
            obj.parent = self
            name = obj.name
            # check if the arguments have valid names
            try:
                names = ["rotation_control", "keyframes"]
                for key in animation.keys():
                    if key not in names:
                        raise KeyError
            except KeyError:
                print("KeyError: expected names 'rotation_control' or 'keyframes' in Object.add()")
                raise
                sys.exit(1)
            # update the dictionaries
            if "rotation_control" in animation.keys():
                obj.rotation_control.update(animation['rotation_control'])
            if "keyframes" in animation.keys():
                obj.keyframes.update(animation['keyframes'])
            tmp = name + "_tmp"
            rot = name + "_rot"
            keyframe = name + "_keyframe"
            new_node = Node(transform=obj.transform)
            new_node.add((tmp, obj))
            if obj.rotation_control['rotation_control']:
                rotation_node = RotationControlNode(obj.rotation_control['key_up'], obj.rotation_control['key_down'],
                                                    obj.rotation_control['axis'], obj.rotation_control['angle'])
                rotation_node.add((name, new_node))
                # add another node if there is a keyframe animation
                if obj.keyframes['keyframes']:
                    keynode = KeyFrameControlNode(obj.keyframes['translate_keys'], obj.keyframes['rotate_keys'],
                                                  obj.keyframes['scale_keys'])
                    keynode.add((rot, rotation_node))
                    self.node.add((keyframe, keynode))
                else:
                    self.node.add((rot, rotation_node))
            else:
                # add another node if there is a keyframe animation
                if obj.keyframes['keyframes']:
                    keynode = KeyFrameControlNode(obj.keyframes['translate_keys'], obj.keyframes['rotate_keys'],
                                                  obj.keyframes['scale_keys'])
                    keynode.add((name, new_node))
                    self.node.add((keyframe, keynode))
                else:
                    self.node.add((name, new_node))

    def draw(self, projection, view, model):
        if self.mesh is not None:
            for mesh in self.mesh:
                mesh.draw(projection, view, model)
        for node in self.node.children.values():
            node.draw(projection, view, model)

    def key_handler(self, key):
        """ Dispatch keyboard events to children """
        for child in self.node.children.values():
            if hasattr(child, 'key_handler'):
                child.key_handler(key)


class Cylinder(Node):
    """ Very simple cylinder based on practical 2 load function """
    def __init__(self, shader):
        super().__init__()
        self.add(*load('cylinder.obj', shader))  # just load cylinder from file


class Surface(Mesh):
    """ Generic surface """
    def __init__(self, texture_map, max_height = 10, size = 50, light_dir=(0, 1, 0),
                 k_a=(0, 0, 0), k_d=(1, 1, 0), k_s=(0.1, 0.1, 0.1), s=16):
        self.light_dir = light_dir
        self.k_a, self.k_d, self.k_s, self.s = k_a, k_d, k_s, s

        # interactive toggles
        self.wrap = cycle([GL.GL_MIRRORED_REPEAT, GL.GL_REPEAT,
                           GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filter = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                             (GL.GL_LINEAR, GL.GL_LINEAR),
                             (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap_mode, self.filter_mode = next(self.wrap), next(self.filter)
        self.texture_map = texture_map
        # setup texture and upload it to GPU
        # Peut-être aussi vérifier pour names
        self.texture = Texture(texture_map, self.wrap_mode, *self.filter_mode)

    def key_handler(self, key):
        # some interactive elements
        if key == glfw.KEY_F6:
            self.wrap_mode = next(self.wrap)
            self.texture = Texture(self.texture_map, self.wrap_mode, *self.filter_mode)
        if key == glfw.KEY_F7:
            self.filter_mode = next(self.filter)
            self.texture = Texture(self.texture_map, self.wrap_mode, *self.filter_mode)

    def draw(self, projection, view, model, primitives=GL.GL_TRIANGLES):
        """ vérifier pour diffuse_map ? """
        GL.glUseProgram(self.shader.glid)

        # texture access setups
        GL.glActiveTexture(GL.GL_TEXTURE0)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture.glid)
        GL.glUniform1i(self.loc['diffuse_map'], 0)

        # setup light parameters
        GL.glUniform3fv(self.loc['light_dir'], 1, self.light_dir)

        # setup material parameters
        GL.glUniform3fv(self.loc['k_a'], 1, self.k_a)
        GL.glUniform3fv(self.loc['k_d'], 1, self.k_d)
        GL.glUniform3fv(self.loc['k_s'], 1, self.k_s)
        GL.glUniform1f(self.loc['s'], max(self.s, 0.001))

        # world camera position for Phong illumination specular component
        w_camera_position = np.linalg.inv(view)[:,3]
        GL.glUniform3fv(self.loc['w_camera_position'], 1, w_camera_position)

        super().draw(projection, view, model, primitives)


class Attributes:
    # Ce serait bien de pouvoir mettre compute_normal dans cette classe (trouver un moyen
    # de les calculer indépendamment de la height_map ?)
    def __init__(self, texture_map, max_color, max_height, size):
        self.texture_map = Image.open(texture_map).convert('RGBA')
        self.max_color = max_color
        self.max_height = max_height
        self.size = size


class TerrainAttributes(Attributes):
    def __init__(self, texture_map, height_map, max_color, max_height, size):
        super().__init__(texture_map, max_color, max_height, size)
        height = Image.open(height_map).convert('L')
        # crop to a square height_map
        self.height_map = height.crop((0, 0, min(height.size), min(height.size)))

    def get_height(self, x, z):
        """
        Compute the height of the vertex at position (x, 0, z)
        accordingly to the height map
        """
        # 0 if outside the height map
        if x < 0 or x >= self.height_map.size[1] or z < 0 or z >= self.height_map.size[0]:
            return 0
        height = self.height_map.getpixel((x, z))
        if height >= self.max_color:
            height = self.max_color-1
        # convert in range -max_height +max_height
        height -= self.max_color / 2
        height /= self.max_color
        height *= self.max_height
        return height

    def compute_normal(self, x, z):
        """
        Compute the normal of the vertex at position (x, y, z)
        """
        # cf. video, retrouver la source ecrite
        height_left = self.get_height(x-1, z)
        height_right = self.get_height(x+1, z)
        height_up = self.get_height(x, z-1)
        height_down = self.get_height(x, z+1)
        normal = vec(height_left - height_right, 2, height_up - height_down)
        return normal / np.linalg.norm(normal)

    def generate_attributes(self):
        """
        Generate the vertices, normals and indices to be
        passed to the shader
        """
        # number of vertices along one axis
        number_vertices_x = self.height_map.size[0]
        total_vertices = number_vertices_x**2
        vertex_pointer = 0

        # result containers
        vertices = total_vertices * [0]
        normals = total_vertices * [0]

        # positions and normals computation
        for i in range(number_vertices_x):
            for j in range(number_vertices_x):
                x = j / (number_vertices_x - 1) * self.size
                y = self.get_height(j, i)
                z = i / (number_vertices_x - 1) * self.size
                normal = self.compute_normal(j, i)

                vertices[vertex_pointer] = (x, y, z)
                normals[vertex_pointer] = normal
                vertex_pointer += 1

        # centering the plane on (0, 0, 0)
        vertices -= vec(self.size / 2, 0, self.size / 2)

        # number of indices in the index array
        indices = (6 * (number_vertices_x - 1)**2) * [0]
        indices_pointer = 0

        # indices computation
        for z in range(number_vertices_x-1):
            for x in range(number_vertices_x-1):
                top_left = z * number_vertices_x + x
                top_right = top_left + 1
                bottom_left = (z + 1) * number_vertices_x + x
                bottom_right = bottom_left + 1

                ind = [top_left, bottom_left, top_right, top_right, bottom_left, bottom_right]
                for i in range(6):
                    indices[indices_pointer] = ind[i]
                    indices_pointer += 1

        return vertices, normals, indices


class WaterAttributes(Attributes):
    # TODO
    # La texture utilisée peut être une image de couleur uniforme pour l'eau
    def __init__(self):
        pass


class Terrain(Surface):
    """ Simple first textured object """
    # Ajouter assertion si fichiers non trouvés
    def __init__(self, texture_map, height_map, shader, max_color = 256, max_height = 10, size = 50,
                 light_dir=(0, 1, 0), k_a=(0, 0, 0), k_d=(1, 1, 0), k_s=(0.1, 0.1, 0.1), s=16):
        self.attrib = TerrainAttributes(texture_map, height_map, max_color, max_height, size)
        self.vertices, self.normals, self.indices = self.attrib.generate_attributes()

        super().__init__(texture_map, max_height, size, light_dir, k_a, k_d, k_s, s)
        Mesh.__init__(self, shader=shader, attributes=[self.vertices, self.normals], index=self.indices)

        names = ['diffuse_map', 'light_dir', 'k_a', 's', 'k_s', 'k_d', 'w_camera_position']
        loc = {n: GL.glGetUniformLocation(shader.glid, n) for n in names}
        self.loc.update(loc)

        print('Loaded terrain \t(x=[%s, %s], z=[%s, %s], %s faces)' % (-self.attrib.size/2, self.attrib.size/2,
                                                                       -self.attrib.size/2, self.attrib.size/2,
                                                                       (self.attrib.height_map.size[0]**2) * 2))


class Water(Surface):
    # TODO
    def __init__(self):
        pass


class Boids:
    """
    Testing phase
    """
    # En ajoutant les contraintes, l'orientation déconne
    def __init__(self, shader, number, model, scaling, index):
        """
        For now, number has to be a perfect cube
        """
        self.index = index      # used in Scene.add
        self.number = number
        self.positions = []
        self.boids = []
        self.perception = 2
        self.deltat = 1e-1
        self.max_speed = 4
        self.max_force = 3

        n = round(number ** (1./3))

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    # positioning and centering the cluster
                    self.positions.append(3 * vec(i - (n-1) / 2, j - (n-1) / 2, k - (n-1) / 2))

        self.velocities = [vec(random.uniform(0, np.sqrt(3*self.max_speed**2)),
                               random.uniform(0, np.sqrt(3*self.max_speed**2)),
                               random.uniform(0, np.sqrt(3*self.max_speed**2))) for _ in range(number)]
        self.accelerations = [vec(random.uniform(0, np.sqrt(3*self.max_force**2)),
                                  random.uniform(0, np.sqrt(3*self.max_force**2)),
                                  random.uniform(0, np.sqrt(3*self.max_force**2))) for _ in range(number)]

        self.orientations = [velocity / np.linalg.norm(velocity) for velocity in self.velocities]     # to change the orientation of the boids


        roots = []
        for i in range(number):
            # Open FBX files if they provide an on place movement

            # To be able to rotate the boids in their own quad
            roots.append(Object(shader, "root_{}".format(i), position=self.positions[i], scaling=(scaling, scaling, scaling)))

            # Setting the correct orientation at the beginning
            axis = np.cross(vec(0, 0, 1), self.orientations[i])
            angle =  np.arccos(np.dot(vec(0, 0, 1), self.orientations[i])) * 360 / (2 * np.pi)
            rotation_mat = rotate(self.orientations[i], 180) @ rotate(axis, angle) @ rotate(vec(0, 0, 1), 180)
            roots[i].add(Object(shader, "boid_{}".format(i), model, rotation_mat=rotation_mat))

            # self.boids.append(Object(shader, "boid_{}".format(i), model, position=self.positions[i], scaling=(scale, scale, scale)))
            self.boids.append(roots[i])

        # self.transforms = [boid.transform for boid in self.boids]
       
    def edges(self):
        """
        If the boids hit an edge of the box, its velocity along this axis is inverted and so is the acceleration
        """
        # For now, in a box of size 5, but otherwise the function is ok except for orientation
        # Sometimes the up vector is not preserved
        indices = [i for i in range(self.number)]
        for index, boid, position, orientation, velocity, acceleration in zip(indices, self.boids, self.positions, self.orientations, self.velocities, self.accelerations):
            new_orientation = copy.deepcopy(orientation)
            changed = False
            for i in range(3):
                if (position[i] > 10 and velocity[i] > 0) or (position[i] < -10 and velocity[i] < 0):
                    velocity[i] = -velocity[i]
                    acceleration[i] = -acceleration[i]
                    new_orientation[i] = -orientation[i]
                    changed = True 
                    
            # Changing the orientation of the objects
            if changed:
                # Rotation in the boid's ref and not in the common one
                axis = np.cross(orientation, new_orientation)
                # Angle changend from radians to degrees
                angle = np.arccos(np.dot(orientation, new_orientation)) * 360 / (2 * np.pi)
                # Rotations of 180 degrees to preserve the up vector of the boid cf. schema
                # Bug, il faudrait considérer le up vector (0, 1, 0) d'une certaine manière
                rotation_mat = rotate(new_orientation, 180) @ rotate(axis, angle) @ rotate(orientation, 180)

                for child in boid.node.children.values():
                    child.transform = rotation_mat @ child.transform

            # Updating the orientations
            self.orientations[index] = copy.deepcopy(new_orientation)

    def align(self):
        """
        Alignement of the orientation of a boid
        """
        for index in range(self.number):
            steering = vec(0, 0, 0)
            avg = vec(0, 0, 0)
            total = 0
            for other_index in range(self.number):
                if index != other_index and np.linalg.norm(self.positions[index] - self.positions[other_index]) < self.perception:
                    avg += self.velocities[other_index]
                    total += 1
            if total > 0:
                avg /= total
                avg = avg / np.linalg.norm(avg) * self.max_speed
                steering = avg - self.velocities[index]
                self.accelerations[index] += steering

    def cohesion(self):
        """
        Cohesion rule
        """
        for index in range(self.number):
            steering = vec(0, 0, 0)
            center_of_mass = vec(0, 0, 0)
            total = 0
            for other_index in range(self.number):
                if index != other_index and np.linalg.norm(self.positions[index] - self.positions[other_index]) < self.perception:
                    center_of_mass += self.positions[other_index]
                    total += 1
            if total > 0:
                center_of_mass /= total
                vec_to_com = center_of_mass - self.positions[index]
                if np.linalg.norm(vec_to_com) > 0:
                    vec_to_com = (vec_to_com / np.linalg.norm(vec_to_com)) * self.max_speed
                steering = vec_to_com - self.velocities[index]
                if np.linalg.norm(steering) > self.max_force:
                    steering = (steering /np.linalg.norm(steering)) * self.max_force
                self.accelerations[index] += self.deltat * steering

    def separate(self):
        """
        Separation rule
        """
        for index in range(self.number):
            steering = vec(0, 0, 0)
            avg = vec(0, 0, 0)
            total = 0
            for other_index in range(self.number):
                if index != other_index:
                    distance = np.linalg.norm(self.positions[other_index] - self.positions[index])
                    if distance < self.perception:
                        diff = self.positions[index] - self.positions[other_index]
                        diff /= distance
                        avg += diff
                        total += 1
            if total > 0:
                avg /= total
                # inutile ...
                if np.linalg.norm(steering) > 0:
                    avg = avg / np.linalg.norm(steering) * self.max_speed
                steering = avg - self.velocities[index]
                if np.linalg.norm(steering) > self.max_force:
                    steering = steering / np.linalg.norm(steering) * self.max_force
                self.accelerations[index] += self.deltat * steering

    def update_positions(self):
        self.edges()
        indices = [i for i in range(self.number)]
        for index, boid, velocity, acceleration in zip(indices, self.boids, self.velocities, self.accelerations):
            boid.transform = translate(self.deltat*velocity) @ boid.transform
            self.positions[index] += self.deltat * velocity
            velocity += acceleration * self.deltat
            # max speed
            if np.linalg.norm(velocity) > self.max_speed:
                velocity /= np.linalg.norm(velocity) * self.max_speed
            self.velocities[index] = velocity

    def draw(self, projection, view, model):
        self.align()
        self.cohesion()
        self.separate()
        self.update_positions()
        for boid in self.boids:
            boid.draw(projection, view, model @ boid.transform)