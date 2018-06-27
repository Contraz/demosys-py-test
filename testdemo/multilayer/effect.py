import moderngl as mgl

from demosys.effects import effect
from demosys import geometry
from OpenGL import GL
# from pyrr import matrix44
from demosys.opengl import FBO


class DefaultEffect(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.multi_shader = self.get_shader("multilayer/multi.glsl")
        self.tex_shader = self.get_shader("multilayer/texture.glsl")
        self.cube = geometry.cube(4.0, 4.0, 4.0)

        self.plane1 = geometry.quad_2d(width=1.0, height=1.0, xpos=-0.5)
        self.plane2 = geometry.quad_2d(width=1.0, height=1.0, xpos=0.5)

        self.fbo = FBO.create((256, 256), depth=False, layers=2)

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.enable(mgl.DEPTH_TEST)

        # Rotate and translate
        m_mv = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -8.0))

        # Apply the rotation and translation from the system camera
        # m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        # Create normal matrix from model-view
        # m_normal = self.create_normal_matrix(m_mv)

        with self.fbo:
            # Draw the cube
            self.multi_shader.uniform("m_proj", self.sys_camera.projection.tobytes())
            self.multi_shader.uniform("m_mv", m_mv.astype('f4').tobytes())
            self.cube.draw(self.multi_shader)

        # m_mv = matrix44.create_identity()

        self.fbo.color_buffers[0].use(location=0)
        self.tex_shader.uniform("texture0", 0)
        self.plane1.draw(self.tex_shader)

        self.fbo.color_buffers[1].use(location=0)
        self.tex_shader.uniform("texture0", 0)
        self.plane2.draw(self.tex_shader)

        self.fbo.clear()