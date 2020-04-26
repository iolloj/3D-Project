#version 330 core

// ---- camera geometry
uniform mat4 projection, view;

// ---- skinning globals and attributes
const int MAX_VERTEX_BONES=4, MAX_BONES=128;
uniform mat4 boneMatrix[MAX_BONES];

// ---- vertex attributes
layout(location = 0) in vec3 position;
layout(location = 1) in vec3 color;
layout(location = 2) in vec2 uv_coords;
layout(location = 3) in vec4 bone_ids;
layout(location = 4) in vec4 bone_weights;

// ----- interpolated attribute variables to be passed to fragment shader
out vec3 fragColor;
out vec2 frag_tex_coords;
out vec4 wPosition4;


// Underwater fog variables
out float visibility;
const float density = 0.007;
const float gradient = 1;

void main()
{
    // ------ creation of the skinning deformation matrix
    mat4 skinMatrix = mat4(0);
    for (int b=0; b < MAX_VERTEX_BONES; b++)
        skinMatrix += bone_weights[b] * boneMatrix[int(bone_ids[b])];

    // ------ compute world and normalized eye coordinates of our vertex
    wPosition4 = skinMatrix * vec4(position, 1.0);
    vec4 pos_to_cam = view * wPosition4;
    gl_Position = projection * pos_to_cam;

    fragColor = color;
    frag_tex_coords = uv_coords;

    // Underwater fog
    float distance = length(pos_to_cam.xyz);
    visibility = exp(-pow((distance * density), gradient));
    visibility = clamp(visibility, 0.0, 1.0);
}