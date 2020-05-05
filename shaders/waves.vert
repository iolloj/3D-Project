#version 330 core
#define nb_waves 4

layout(location = 0) in vec3 position;
layout(location = 1) in vec3 normal;

// position and normal for the fragment shader, in WORLD coordinates
out vec3 w_position, w_normal;   // in world coordinates
out vec3 my_normal;
out vec3 pos;
out vec2 frag_tex_coords;

uniform float time;
uniform mat4 model, view, projection;



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

vec3 gerstner_wave_position(vec2 position, float time) {
    vec3 wave_position = vec3(position.x, 0, position.y);
    for (int i = 0; i < nb_waves; ++i) {
        float proj = dot(position, gerstner_waves[i].direction),
              phase = time * gerstner_waves[i].speed,
              theta = proj * gerstner_waves[i].frequency + phase,
              height = gerstner_waves[i].amplitude * sin(theta);

        wave_position.y += height;

        float maximum_width = gerstner_waves[i].steepness *
                              gerstner_waves[i].amplitude,
              width = maximum_width * cos(theta),
              x = gerstner_waves[i].direction.x,
              y = gerstner_waves[i].direction.y;

        wave_position.x += x * width;
        wave_position.z += y * width;
    } return wave_position;
}

vec3 gerstner_wave(vec2 position, float time, inout vec3 normal) {
    vec3 wave_position = gerstner_wave_position(position, time);
    normal = gerstner_wave_normal(wave_position, time);
    return wave_position; // Accumulated Gerstner Wave.
}




void main() {
    vec3 newNormal = normal;
    pos = gerstner_wave(position.xz, time, newNormal);
    //pos = position*cos(time);
    gl_Position = projection * view * model * vec4(pos, 1);
    // Normals
    w_normal = (model * vec4(normal, 0)).xyz;

    // Transformation
    mat4 m = view * model;
    mat3 nit = mat3(transpose(inverse(m)));
    my_normal = nit * normal;

    frag_tex_coords = pos.xz;
}
