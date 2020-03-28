#version 330 core

// fragment position and normal of the fragment, in WORLD coordinates
// (you can also compute in VIEW coordinates, your choice! rename variables)
in vec3 w_position, w_normal;   // in world coodinates
in vec3 my_normal;
in vec3 pos;

// light dir, in world coordinates
uniform vec3 light_dir;

// material properties
uniform vec3 k_a;
uniform vec3 k_d;
uniform vec3 k_s;
uniform float s;

// world camera position
uniform vec3 w_camera_position;

out vec4 out_color;

void main() {
    // TODO: compute Lambert illumination
    vec3 n = normalize(w_normal);
    //vec3 n = normalize(my_normal);
    vec3 l = normalize(light_dir);
    vec3 r = reflect(-l, n);
    vec3 v = normalize(-(w_position - w_camera_position));
    // cf. after
    //vec3 v = normalize(pos);

    // Point P in camera space is the view vector
    // vec3 v = mat3(inverse(view)) * (0, 0, 1) // why (0, 0, 1)? cf. first practical 4

    // Lambertian model
    // out_color = vec4(k_d * max(0, dot(n, light_dir)), 1);

    // Phong model
    out_color = vec4(k_a + k_d * max(0, dot(n, l)) + k_s * pow(max(0, dot(r, v)), s), 1);
}
