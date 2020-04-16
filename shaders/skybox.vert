#version 330 core

in vec3 position;
out vec3 textureCoords;

// Vérifier dans le code qu'on les passe bien
uniform mat4 projection;
uniform mat4 view;


void main()
{
    gl_Position = projection * view * vec4(position, 1);
    textureCoords = position;
}