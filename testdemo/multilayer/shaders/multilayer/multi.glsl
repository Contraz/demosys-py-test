#version 330

#if defined VERTEX_SHADER

in vec3 in_position;

uniform mat4 m_proj;
uniform mat4 m_mv;

void main() {
    gl_Position = m_proj * m_mv * vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

layout(location = 0) out vec4 outColor0;
layout(location = 1) out vec4 outColor1;

void main() {
    outColor0 = vec4(1.0, 0.0, 0.0, 1.0);
    outColor1 = vec4(0.0, 1.0, 0.0, 1.0);
}

#endif
