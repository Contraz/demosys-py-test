#version 410

#if defined VERTEX_SHADER

in vec3 in_position;
in vec2 in_uv;

out vec2 uv;

//uniform mat4 m_proj;
//uniform mat4 m_mv;

void main() {
    uv = in_uv;
//    gl_Position = m_proj * m_mv * vec4(in_position, 1.0);
    gl_Position = vec4(in_position, 1.0);
}

#elif defined FRAGMENT_SHADER

in vec2 uv;

uniform sampler2D texture0;

out vec4 outColor;

void main() {
    outColor = texture(texture0, uv) + vec4(0.5);
}

#endif
