#!/usr/bin/env python3
"""
Python OpenGL practical application.
petit souci avec la lumière on dirait, pour la direction?
peut-etre probleme lie aux normales
"""

from viewer import *
from meshes import *
from nodes import *


class Scene:
    """ General scene class """
    # Hierarchical structure not treated yet
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
            obj.parent = self
            # check if the arguments have valid names
            try:
                names = ["rotation_control", "keyframes"]
                for key in animation.keys():
                    if key not in names:
                        raise KeyError
            except KeyError:
                print("KeyError: expected names 'rotation_control' or 'keyframes' in Scene.add()")
                raise
                sys.exit(1)
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
    def __init__(self, shader, name, obj_pos, light_dir=(0, 0, 0), position=(0, 0, 0), scaling=(1, 1, 1), rotation_axis=(0, 0, 0), rotation_angle=0, rotation_mat=None, tex_file=None):
        # Maybe using **kwargs to pass a dictionary
        self.name = name
        self.parent = None
        self.mesh = load(obj_pos, shader, light_dir, tex_file)
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

    def add(self, *objects, **kwargs):
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
                for key in kwargs.keys():
                    if key not in names:
                        raise KeyError
            except KeyError:
                print("KeyError: expected names 'rotation_control' or 'keyframes' in Object.add()")
                raise
                sys.exit(1)
            # update the dictionaries
            if "rotation_control" in kwargs.keys():
                obj.rotation_control.update(kwargs['rotation_control'])
            if "keyframes" in kwargs.keys():
                obj.keyframes.update(kwargs['keyframes'])
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


class TerrainAttributes:
    def __init__(self, texture_map, height_map, max_color, max_height, size):
        self.texture_map = Image.open(texture_map).convert('RGBA')
        height = Image.open(height_map).convert('L')
        # crop to a square height_map
        self.height_map = height.crop((0, 0, min(height.size), min(height.size)))
        self.max_color = max_color
        self.max_height = max_height
        self.size = size

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


class Terrain(Mesh):
    """ Simple first textured object """
    # Ajouter assertion si fichiers non trouvés
    def __init__(self, texture_map, height_map, shader, max_color = 256, max_height = 10, size = 50,
                 light_dir=(0, 1, 0), k_a=(0, 0, 0), k_d=(1, 1, 0), k_s=(0.1, 0.1, 0.1), s=16):
        self.attrib = TerrainAttributes(texture_map, height_map, max_color, max_height, size)
        self.vertices, self.normals, self.indices = self.attrib.generate_attributes()

        super().__init__(shader, [self.vertices, self.normals], self.indices)
        self.light_dir = light_dir
        self.k_a, self.k_d, self.k_s, self.s = k_a, k_d, k_s, s

        names = ['diffuse_map', 'light_dir', 'k_a', 's', 'k_s', 'k_d', 'w_camera_position']
        # names = ['light_dir', 'k_a', 's', 'k_s', 'k_d', 'w_camera_position']
        loc = {n: GL.glGetUniformLocation(shader.glid, n) for n in names}
        self.loc.update(loc)

        # interactive toggles
        self.wrap = cycle([GL.GL_MIRRORED_REPEAT, GL.GL_REPEAT,
                           GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filter = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                             (GL.GL_LINEAR, GL.GL_LINEAR),
                             (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap_mode, self.filter_mode = next(self.wrap), next(self.filter)
        self.texture_map = texture_map
        # setup texture and upload it to GPU
        self.texture = Texture(texture_map, self.wrap_mode, *self.filter_mode)
        print('Loaded terrain \t(x=[%s, %s], z=[%s, %s], %s faces)' % (-self.attrib.size/2, self.attrib.size/2,
                                                                       -self.attrib.size/2, self.attrib.size/2,
                                                                       (self.attrib.height_map.size[0]**2) * 2))

    def key_handler(self, key):
        # some interactive elements
        if key == glfw.KEY_F6:
            self.wrap_mode = next(self.wrap)
            self.texture = Texture(self.texture_map, self.wrap_mode, *self.filter_mode)
        if key == glfw.KEY_F7:
            self.filter_mode = next(self.filter)
            self.texture = Texture(self.texture_map, self.wrap_mode, *self.filter_mode)

    def draw(self, projection, view, model, primitives=GL.GL_TRIANGLES):
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
