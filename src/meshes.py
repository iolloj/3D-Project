#!/usr/bin/env python3
from viewer import *

# mesh to refactor all previous classes
class Mesh:

    def __init__(self, shader, attributes, index=None):
        self.shader = shader
        names = ['view', 'projection', 'model']
        self.loc = {n: GL.glGetUniformLocation(shader.glid, n) for n in names}
        self.vertex_array = VertexArray(attributes, index)

    def draw(self, projection, view, model, primitives=GL.GL_TRIANGLES):
        GL.glUseProgram(self.shader.glid)

        GL.glUniformMatrix4fv(self.loc['view'], 1, True, view)
        GL.glUniformMatrix4fv(self.loc['projection'], 1, True, projection)
        GL.glUniformMatrix4fv(self.loc['model'], 1, True, model)

        # draw triangle as GL_TRIANGLE vertex array, draw array call
        self.vertex_array.execute(primitives)


class PhongMesh(Mesh):
    """ Mesh with Phong illumination """

    def __init__(self, shader, attributes, index=None,
                 light_dir=(0, -1, 0),   # directionnal light (in world coords)
                 k_a=(0, 0, 0), k_d=(1, 1, 0), k_s=(1, 1, 1), s=16.):
        super().__init__(shader, attributes, index)
        self.light_dir = light_dir
        self.k_a, self.k_d, self.k_s, self.s = k_a, k_d, k_s, s

        # retrieve OpenGL locations of shader variables at initialization
        names = ['light_dir', 'k_a', 's', 'k_s', 'k_d', 'w_camera_position']

        loc = {n: GL.glGetUniformLocation(shader.glid, n) for n in names}
        self.loc.update(loc)

    def draw(self, projection, view, model, primitives=GL.GL_TRIANGLES):
        GL.glUseProgram(self.shader.glid)

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



class ComplexMesh(Mesh):
    """ Simple first textured object """

    def __init__(self, shader, texture, attributes, index=None,
                 light_dir=(0, 0, 0),  # directional light (in world coords)
                 k_a=(0, 0, 0), k_d=(1, 1, 0), k_s=(1, 1, 1), s=16):

        super().__init__(shader, attributes, index)
        self.light_dir = light_dir
        self.k_a, self.k_d, self.k_s, self.s = k_a, k_d, k_s, s

        names = ['diffuse_map', 'light_dir', 'k_a', 's', 'k_s', 'k_d', 'w_camera_position']
        loc = {n: GL.glGetUniformLocation(shader.glid, n) for n in names}
        self.loc.update(loc)

        # interactive toggles
        self.wrap = cycle([GL.GL_REPEAT, GL.GL_MIRRORED_REPEAT,
                           GL.GL_CLAMP_TO_BORDER, GL.GL_CLAMP_TO_EDGE])
        self.filter = cycle([(GL.GL_NEAREST, GL.GL_NEAREST),
                             (GL.GL_LINEAR, GL.GL_LINEAR),
                             (GL.GL_LINEAR, GL.GL_LINEAR_MIPMAP_LINEAR)])
        self.wrap_mode, self.filter_mode = next(self.wrap), next(self.filter)

        # setup texture and upload it to GPU
        self.texture = texture

    def key_handler(self, key):
        # some interactive elements
        if key == glfw.KEY_F6:
            self.wrap_mode = next(self.wrap)
            self.texture = Texture(self.file, self.wrap_mode, *self.filter_mode)
        if key == glfw.KEY_F7:
            self.filter_mode = next(self.filter)
            self.texture = Texture(self.file, self.wrap_mode, *self.filter_mode)

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



# -------------- 3D resource loader -----------------------------------------
def load(file, shader, light_dir=(0, 0, 0), tex_file=None):
    """
    load a complex mesh
    if light_dir is not specified, acts like load_textured
    if light_dir is specified, combines phong and texture
    returns a list of ComplexMesh
    """
    try:
        pp = assimpcy.aiPostProcessSteps
        flags = pp.aiProcess_Triangulate | pp.aiProcess_FlipUVs
        scene = assimpcy.aiImportFile(file, flags)
    except assimpcy.all.AssimpError as exception:
        print('ERROR loading', file + ': ', exception.args[0].decode())
        return []

    # Note: embedded textures not supported at the moment
    path = os.path.dirname(file) if os.path.dirname(file) != '' else './'
    for mat in scene.mMaterials:
        if not tex_file and 'TEXTURE_BASE' in mat.properties:  # texture token
            name = os.path.basename(mat.properties['TEXTURE_BASE'])
            # search texture in file's whole subdir since path often screwed up
            paths = os.walk(path, followlinks=True)
            found = [os.path.join(d, f) for d, _, n in paths for f in n
                     if name.startswith(f) or f.startswith(name)]
            assert found, 'Cannot find texture %s in %s subtree' % (name, path)
            tex_file = found[0]
        if tex_file:
            mat.properties['diffuse_map'] = Texture(file=tex_file)

    # prepare textured mesh
    meshes = []
    for mesh in scene.mMeshes:
        mat = scene.mMaterials[mesh.mMaterialIndex].properties
        # assert mat['diffuse_map'], "Trying to map using a textureless material"
        attributes = [mesh.mVertices, mesh.mNormals, mesh.mTextureCoords[0]]
        if 'diffuse_map' in mat.keys():
            mesh = ComplexMesh(shader, mat['diffuse_map'], attributes, mesh.mFaces,
                             k_d=mat.get('COLOR_DIFFUSE', (1, 1, 1)),
                             k_s=mat.get('COLOR_SPECULAR', (1, 1, 1)),
                             k_a=mat.get('COLOR_AMBIENT', (0, 0, 0)),
                             s=mat.get('SHININESS', 16.),
                             light_dir=light_dir)
        else:
            mesh = PhongMesh(shader, attributes[:-1], mesh.mFaces,
                             k_d=mat.get('COLOR_DIFFUSE', (1, 1, 1)),
                             k_s=mat.get('COLOR_SPECULAR', (1, 1, 1)),
                             k_a=mat.get('COLOR_AMBIENT', (0, 0, 0)),
                             s=mat.get('SHININESS', 16.),
                             light_dir=light_dir)

        meshes.append(mesh)

    size = sum((mesh.mNumFaces for mesh in scene.mMeshes))
    print('Loaded %s\t(%d meshes, %d faces)' % (file, len(meshes), size))
    return meshes

