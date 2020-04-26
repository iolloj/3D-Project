#version 330 core

in vec3 fragColor;
in vec2 frag_tex_coords;
in vec4 wPosition4;
in float visibility;

uniform sampler2D diffuse_map;

out vec4 outColor;

void main()
{
    //outColor = vec4(fragColor, 1);
    outColor = texture(diffuse_map, frag_tex_coords);

    // Underwater fog
    if (wPosition4.y < 0)
        outColor = mix(vec4(0.1, 0.1, 0.1, 1), outColor, visibility);
}