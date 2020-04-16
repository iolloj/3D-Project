#version 330 core

in vec3 position;
out vec3 textureCoords;

uniform mat4 projection;
uniform mat4 view;


void main()
{
    vec4 pos = projection * view * vec4(position, 1);
    // Normalization
    gl_Position = pos.xyww;
    textureCoords = position;
}