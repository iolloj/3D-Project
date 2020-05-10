#version 330 core

// fragment position and normal of the fragment, in WORLD coordinates
in vec3 w_position, w_normal;   // in world coodinates
in vec3 my_normal;
in vec3 pos;
in float visibility;
in vec4 world_coords;

// light dir, in world coordinates
uniform vec3 light_dir;

// material properties
uniform vec3 k_a;
uniform vec3 k_d;
uniform vec3 k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

// textures
uniform sampler2D diffuse_map;
in vec2 frag_tex_coords;

out vec4 out_color;

void main() {
    // Object frame
    vec3 n = normalize(w_normal);
    // World frame
    //vec3 n = normalize(my_normal);

    vec3 l = normalize(light_dir);
    vec3 r = reflect(-l, n);
    
    // Point P in camera space is the view vector
    vec3 v = normalize(pos);
    
    // Texture = ambiant color
    vec4 kd = texture(diffuse_map, frag_tex_coords);

    // Phong model + texture
    if (light_dir == vec3(0, 0, 0))
        out_color = kd;
    else
        out_color = kd * max(0, dot(n, l)) + vec4(k_a + k_s * pow(max(0, dot(r, v)), s), 1);

    // Underwater fog
    if (world_coords.y < 0)
            out_color = mix(vec4(0.1, 0.1, 0.1, 1), out_color, visibility);
}