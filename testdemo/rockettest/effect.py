import moderngl as mgl

import math
from demosys.effects import effect
from demosys import geometry
from OpenGL import GL
from pyrr import matrix44


class DefaultEffect(effect.Effect):
    """Generated default efffect"""
    def __init__(self):
        self.shader = self.get_shader("default.glsl", local=False)
        self.cube = geometry.cube(4.0, 4.0, 4.0)

        # Tracks
        self.rot_x = self.get_track("cube:rot.x")
        self.rot_y = self.get_track("cube:rot.y")
        self.rot_z = self.get_track("cube:rot.z")
        self.pos_z = self.get_track("cube:pos.z")

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.enable(mgl.DEPTH_TEST)

        # Rotate and translate
        m_mv = self.create_transformation(rotation=(self.rot_x.time_value(time) * math.pi / 180,
                                                    self.rot_y.time_value(time) * math.pi / 180,
                                                    self.rot_z.time_value(time) * math.pi / 180),
                                          translation=(0.0,
                                                       0.0,
                                                       self.pos_z.time_value(time)))

        # Apply the rotation and translation from the system camera
        # m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        # Create normal matrix from model-view
        m_normal = self.create_normal_matrix(m_mv)

        # Draw the cube
        self.shader.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.shader.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.shader.uniform("m_normal", m_normal.astype('f4').tobytes())
        self.cube.draw(self.shader)
