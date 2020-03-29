#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
//layout(location = 2) in vec2 texture_coords;

uniform mat4 model, view, projection;
uniform sampler2D height_map;

// position and normal for the fragment shader, in WORLD coordinates
out vec3 w_position, w_normal;   // in world coordinates
out vec3 my_normal;
out vec3 pos;

// texture coordinates
out vec2 frag_tex_coords;

void main() {
    vec4 v = vec4(position.x, position.y, position.z, 1.0);
    v.y = texture2D(height_map, vec2(position.x / 256.0, position.z / 256.0)).y * 5.0;
    //gl_Position = projection * view * model * vec4(position, 1);

    w_normal = (model * vec4(normal, 0)).xyz;

    // Transformation
    mat4 m = view * model;
    mat3 nit = mat3(transpose(inverse(m)));
    my_normal = nit * normal;

    pos = position;
    //pos = v.xyz;
    gl_Position = projection * view * model * v;
    frag_tex_coords = position.xz;
}
