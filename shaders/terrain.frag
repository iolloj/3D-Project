#version 330 core

#define nb_waves 4
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
uniform float time;
// world camera position
uniform vec3 w_camera_position;

// texture
uniform sampler2D diffuse_map;
uniform sampler2D caustics;

in vec2 frag_tex_coords;

out vec4 out_color;

uniform struct GerstnerWave {
    vec2 direction;
    float amplitude;
    float steepness;
    float frequency;
    float speed;
};
GerstnerWave gerstner_waves[nb_waves] = GerstnerWave[](
    GerstnerWave(vec2(0., 1.), 1.8, 0.2, 0.07, 0.5),
    GerstnerWave(vec2(1., 0.), 2.5, 0.1, 0.02, 0.2),
    GerstnerWave(vec2(-1, 0.7), 0.8, 0.5, 0.09, 0.4),
    GerstnerWave(vec2(3., -4.), 1.2, 0.3, 0.04, 0.3)
    );


vec3 gerstner_wave_normal(vec3 position, float time) {
    vec3 wave_normal = vec3(0.0, 1.0, 0.0);
    for (int i = 0; i <nb_waves; ++i) {
        float proj = dot(position.xz, gerstner_waves[i].direction),
              phase = time * gerstner_waves[i].speed,
              psi = proj * gerstner_waves[i].frequency + phase,
              Af = gerstner_waves[i].amplitude *
                   gerstner_waves[i].frequency,
              alpha = Af * sin(psi);

        wave_normal.y -= gerstner_waves[i].steepness * alpha;

        float x = gerstner_waves[i].direction.x,
              y = gerstner_waves[i].direction.y,
              omega = Af * cos(psi);

        wave_normal.x -= x * omega;
        wave_normal.z -= y * omega;
    } return wave_normal;
}

vec3 line_plane_intercept(vec3 lineP,
                            vec3 lineN,
                            vec3 planeN,
                            float  planeD)
{
    float distance = (planeD - dot(planeN, lineP)) /dot(lineN, planeN);
    return lineP + lineN * distance;
}

void main() {
    // Object frame
    vec3 n = normalize(w_normal);
    // World frame
    //vec3 n = normalize(my_normal);

    vec3 waveN = gerstner_wave_normal(pos, time);
    vec3 intercept = line_plane_intercept(
                    pos.xyz,
                    waveN,
                    light_dir, 230);

    vec3 l = normalize(light_dir);
    vec3 r = reflect(-l, n);
    
    // Point P in camera space is the view vector
    vec3 v = normalize(pos);
    
    vec4 kd = texture(diffuse_map, frag_tex_coords);

    // Shades of blue varying with the depth
    if (world_coords.y < 2)
        kd += vec4(pos.y/20, pos.y/20, pos.y/200, 1)/2;

    // Phong model + texture
    if (light_dir == vec3(0, 0, 0))
        out_color = kd;
    else
        out_color = kd * max(0, dot(n, l)) + vec4(k_a + k_s * pow(max(0, dot(r, v)), s), 1);

    // Underwater fog
    if (world_coords.y < 0){
        out_color = mix(vec4(0.1, 0.1, 0.1, 1), out_color, visibility);
        out_color += mix(vec4(0.1, 0.1, 0.1, 1), vec4(0.5*vec3(texture(caustics, 0.008*intercept.xz)), 0.1), visibility);
    }
}
