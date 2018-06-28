#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;
in vec3 in_pos_offset;
in float in_time_offset;

uniform mat4 m_proj;
uniform mat4 m_camera;
uniform mat3 m_normal;

out vec3 normal;
out vec2 uv;
out float time_offset;

void main() {
	gl_Position = m_proj * m_camera * vec4(in_position + in_pos_offset, 1.0);
    normal = m_normal * in_normal;
    time_offset = in_time_offset;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform float time;

in vec3 normal;
in float time_offset;

void main()
{
    vec3 dir = vec3(0.0, 0.0, 1.0);
    float l = dot(dir, normalize(normal));
    fragColor = vec4(l, sin((time + time_offset)  / 20.0), l * 2.0, 1.0);
}

#endif
