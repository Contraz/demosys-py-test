import moderngl as mgl
import numpy as np
import random

from demosys.effects import effect
from demosys import geometry
from demosys.opengl import VAO
# from pyrr import matrix44


class InstancedCubeEffect(effect.Effect):
    """Generated default effect"""

    def __init__(self):
        self.shader = self.get_shader("cube_plain.glsl", local=True)
        self.transform_shader = self.get_shader("transform.glsl", local=True)
        self.cube = geometry.cube(10.0, 10.0, 10.0)

        self.dim = 500
        self.instances = self.dim ** 2

        # Per instance buffer for position and time offsets
        self.instance1 = self.cube.buffer(
            np.fromiter(self.gen_positions(self.dim, 11.0), dtype=np.float32),
            '3f 1f',
            ['in_pos_offset', 'in_time_offset'],
            per_instance=True,
        )

        # Copy of the position buffer. We need some dummy instances in oder to do the calculations
        self.instance2 = self.ctx.buffer(reserve=self.instances * 16)
        self.ctx.copy_buffer(self.instance2, self.instance1)

        # VAO for doing position transforms
        self.pos_vao = VAO("positions")
        self.pos_vao.buffer(self.instance2, '3f 1f', ['in_position', 'in_time_offset'])

        self.m_proj = self.create_projection(fov=75, near=1.0, far=5000.0)

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.enable(mgl.DEPTH_TEST)
        self.sys_camera.velocity = 250.0

        m_normal = self.create_normal_matrix(self.sys_camera.view_matrix)

        # Calculate positions: Loops instance2 buffer storing result in instance1
        self.transform_shader.uniform("time", time)
        self.pos_vao.transform(self.transform_shader, self.instance1)

        # Draw the cubes
        self.shader.uniform("m_proj", self.m_proj.astype('f4').tobytes())
        self.shader.uniform("m_camera", self.sys_camera.view_matrix.astype('f4').tobytes())
        self.shader.uniform("m_normal", m_normal.astype('f4').tobytes())
        self.shader.uniform("time", time * 100)

        self.cube.draw(self.shader, instances=self.instances)

    def gen_positions(self, dim, spacing):
        for i in range(-dim // 2, dim // 2):
            for j in range(-dim // 2, dim // 2):
                yield i * -spacing
                yield 0
                yield j * -spacing
                yield random.random() * 100
