#!/usr/bin/env python3
"""
Python OpenGL practical application.
petit souci avec la lumière on dirait, pour la direction?
peut-etre probleme lie aux normales
"""

from viewer import *
from meshes import *


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
                 light_dir=(0, 1, 0), k_a=(0, 0, 0), k_d=(1, 1, 0), k_s=(1, 1, 1), s=16):
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
