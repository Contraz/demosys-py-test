#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in float in_time_offset;

uniform float time;

out vec3 out_position;
out float out_time_offset;

void main() {
    out_position = vec3(
        in_position.x,
        sin((time + in_position.x / 100.0) * 1.7) * 25.0 +
        sin((time + in_position.z / 100.0) * 2.0) * 22.0,
        in_position.z);

    out_time_offset = in_time_offset;
}
#endif
