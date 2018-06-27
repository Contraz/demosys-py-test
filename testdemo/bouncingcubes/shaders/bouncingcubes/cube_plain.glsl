#version 330

#if defined VERTEX_SHADER

in vec3 in_position;
in vec3 in_normal;

uniform mat4 m_proj;
uniform mat4 m_camera;
uniform vec3 pos;

out vec3 normal;
out vec2 uv;

void main() {
	gl_Position = m_proj * m_camera * vec4(in_position + pos, 1.0);
	mat3 m_normal = mat3(transpose(inverse(m_camera)));
    normal = m_normal * in_normal;
}

#elif defined FRAGMENT_SHADER

out vec4 fragColor;
uniform float time;

in vec3 normal;

void main()
{
    vec3 dir = vec3(0.0, 0.0, 1.0);
    float l = dot(dir, normal);
    fragColor = vec4(l, sin(time / 20.0), l * 2.0, 1.0);
}

#endif
