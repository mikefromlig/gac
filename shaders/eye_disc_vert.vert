in vec3 in_vertex;
in vec4 in_color;

out vec4 v_color;
void main() {
    gl_Position = vec4(in_vertex, 1.0);
    v_color = in_color;
}
