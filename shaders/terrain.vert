#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

uniform mat4 model, view, projection;

// position and normal for the fragment shader, in WORLD coordinates
out vec3 w_position, w_normal;   // in world coordinates
out vec3 my_normal;
out vec3 pos;
out vec2 frag_tex_coords;

void main() {
    pos = position;
    
    gl_Position = projection * view * model * vec4(position, 1);
    
    // Normals
    w_normal = (model * vec4(normal, 0)).xyz;

    // Transformation
    mat4 m = view * model;
    mat3 nit = mat3(transpose(inverse(m)));
    my_normal = nit * normal;

    frag_tex_coords = position.xz;
}
