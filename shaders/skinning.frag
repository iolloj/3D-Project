#version 330 core

in vec3 fragColor;
in vec2 frag_tex_coords;

uniform sampler2D diffuse_map;

out vec4 outColor;

void main()
{
    //outColor = vec4(fragColor, 1);
    outColor = texture(diffuse_map, frag_tex_coords);
}