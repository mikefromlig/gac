#version 330 core
precision highp float; //High precision, critical !!!

in vec4 v_color;

out vec4 fragColor;

void main() {
    fragColor = v_color;
}