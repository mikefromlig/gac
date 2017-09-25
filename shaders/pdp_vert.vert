#version 330 core
precision highp float;

uniform mat4 projection_mat;
uniform mat4 modelview_mat;
uniform mat4 displacement;

in vec3 in_vertex;
in vec4 in_color;
in vec3 in_normal;

out vec4 v_color;

vec3 light_p = vec3(0, 20, 20);
void main() {
    gl_Position = projection_mat * modelview_mat * displacement * vec4(in_vertex, 1.0);
    
    //Lighting
    vec3 light_v = normalize(light_p - in_vertex);
    float d = dot(light_v, in_normal);
    
    //Color from lighting
    v_color = vec4(d*(in_color.xyz), 1.0);
}
