from demosys.effects import effect
from demosys.opengl import geometry
from OpenGL import GL
from pyrr import matrix44


class DefaultEffect(effect.Effect):
    """Generated default efffect"""
    def __init__(self):
        self.shader = self.get_shader("default.glsl")
        self.cube = geometry.cube(4.0, 4.0, 4.0)

        # Tracks
        self.rot_x = self.get_track("test:rot.x")
        self.rot_y = self.get_track("test:rot.y")
        self.rot_z = self.get_track("test:rot.z")
        self.pos_z = self.get_track("test:pos.z")

    @effect.bind_target
    def draw(self, time, frametime, target):
        GL.glEnable(GL.GL_DEPTH_TEST)

        # Rotate and translate
        m_mv = self.create_transformation(rotation=(self.rot_x.time_value(time),
                                                    self.rot_y.time_value(time),
                                                    self.rot_z.time_value(time)),
                                          translation=(0.0,
                                                       0.0,
                                                       self.pos_z.time_value(time)))

        # Apply the rotation and translation from the system camera
        m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        # Create normal matrix from model-view
        m_normal = self.create_normal_matrix(m_mv)

        # Draw the cube
        with self.cube.bind(self.shader) as shader:
            shader.uniform_mat4("m_proj", self.sys_camera.projection)
            shader.uniform_mat4("m_mv", m_mv)
            shader.uniform_mat3("m_normal", m_normal)
        self.cube.draw()
