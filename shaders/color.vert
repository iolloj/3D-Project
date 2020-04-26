#version 330 core

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;
layout(location = 2) in vec2 uv_coords;

uniform mat4 model, view, projection;

// position and normal for the fragment shader, in WORLD coordinates
out vec3 w_position, w_normal;   // in world coordinates
out vec3 my_normal;
out vec3 pos;

// texture coordinates
out vec2 frag_tex_coords;

// Underwater fog variables
out float visibility;
out vec4 world_coords;
const float density = 0.007;
const float gradient = 1;

void main() {
    world_coords = model * vec4(position, 1);
    vec4 pos_to_cam =  view * world_coords;
    gl_Position = projection * pos_to_cam;
    
    w_normal = (model * vec4(normal, 0)).xyz;

    // Transformation
    mat4 m = view * model;
    mat3 nit = mat3(transpose(inverse(m)));
    my_normal = nit * normal;

    pos = position;
    frag_tex_coords = uv_coords;

    // Underwater fog
    float distance = length(pos_to_cam.xyz);
    visibility = exp(-pow((distance * density), gradient));
    visibility = clamp(visibility, 0.0, 1.0);
}
