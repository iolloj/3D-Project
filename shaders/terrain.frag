#version 330 core
#define VTXSIZE 0.01f   // Amplitude

#define WAVESIZE 10.0f  // Frequency

#define FACTOR 1.0f
#define SPEED 2.0f
#define OCTAVES 5
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

// texture
uniform sampler2D diffuse_map;
uniform sampler2D caustics;

in vec2 frag_tex_coords;

out vec4 out_color;

   vec2 gradwave(float x,
                float y,
                float timer)
{
  float dZx = 0.0f;
  float dZy = 0.0f;
  float octaves = OCTAVES;
  float factor = FACTOR;
  float d = sqrt(x * x + y * y);

  do {
    dZx += d * sin(timer * SPEED + (1/factor) * x * y * WAVESIZE) *
             y * WAVESIZE - factor *
             cos(timer * SPEED + (1/factor) * x * y * WAVESIZE) * x/d;
    dZy += d * sin(timer * SPEED + (1/factor) * x * y * WAVESIZE) *
             x * WAVESIZE - factor *
             cos(timer * SPEED + (1/factor) * x * y * WAVESIZE) * y/d;
    factor = factor/2;
    octaves--;
  } while (octaves > 0);

  return vec2(2 * VTXSIZE * dZx, 2 * VTXSIZE * dZy);
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

    vec2 dxdy = gradwave(pos.x, pos.y, 0.1);
    vec3 intercept = line_plane_intercept(
                    pos.xyz,
                    vec3(dxdy, pos.z),
                    vec3(0, 0, 1), -0.8);

    vec3 l = normalize(light_dir);
    vec3 r = reflect(-l, n);
    
    // Point P in camera space is the view vector
    vec3 v = normalize(pos);
    
    vec4 kd = texture(caustics, 0.001*intercept.xz);

    // Shades of blue varying with the depth
    if (world_coords.y < 2)
        kd += vec4(pos.y/20, pos.y/20, pos.y/200, 1)/2;

    // Phong model + texture
    if (light_dir == vec3(0, 0, 0))
        out_color = kd;
    else
        out_color = kd * max(0, dot(n, l)) + vec4(k_a + k_s * pow(max(0, dot(r, v)), s), 1);

    // Underwater fog
    if (world_coords.y < 0)
        out_color = mix(vec4(0.1, 0.1, 0.1, 1), out_color, visibility);
    //out_color += vec4(vec3(texture(caustics, 0.001*intercept.xz)), 1);
    out_color = vec4(vec3(intercept.z)/10, 1);
    //out_color = vec4(vec3(0.5), 1);
}
