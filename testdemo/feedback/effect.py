import moderngl as mgl
import math
import numpy
import random

from OpenGL import GL

from demosys import geometry
from demosys.effects import effect
from demosys.opengl import VAO

from pyrr import matrix44
from pyrr import vector3


class DefaultEffect(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.feedback = self.get_shader("feedback/feedback.glsl")
        self.shader = self.get_shader("feedback/default.glsl")
        self.texture = self.get_texture("feedback/particle.png")

        self.cube = geometry.cube(width=4, height=4, depth=4)
        self.cube_shader = self.get_shader("feedback/cube.glsl")

        # VAOs representing the two different buffer bindings
        self.particles1 = None
        self.particles2 = None
        self.particles = None

        # VBOs for each position buffer
        self.pos1 = None
        self.pos2 = None
        self.pos = None
        self.init_particles()

    @effect.bind_target
    def draw(self, time, frametime, target):
        GL.glDisable(GL.GL_DEPTH_TEST)

        GL.glEnable(GL.GL_BLEND)
        GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)

        m_proj = self.create_projection(90.0, 1.0, 1000.0)

        # Rotate and translate
        m_mv = self.create_transformation(rotation=(time * 0.0, time * 0, time * 0),
                                          translation=(0.0, 0.0, -40.0))

        # Apply the rotation and translation from the system camera
        m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)

        # gravity = vector3.create(math.sin(time) * 10.0
        gravity_pos = vector3.create(math.sin(time) * 5,
                                     math.cos(time) * 5,
                                     math.sin(time/3) * 5)
        gravity_force = math.cos(time / 2) * 3.0 + 3.0
        # gravity_force = 2.0

        # Transform
        self.feedback.uniform("gravity_pos", gravity_pos.astype('f4').tobytes())
        self.feedback.uniform("gravity_force", gravity_force)
        self.feedback.uniform("timedelta", frametime)
        self.particles.transform(self.feedback, self.pos)

        # Draw particles
        self.shader.uniform("m_proj", m_proj.astype('f4').tobytes())
        self.shader.uniform("m_mv", m_mv.astype('f4').tobytes())
        self.texture.use(location=0)
        self.shader.uniform("texture0", 0)
        self.particles.draw(self.shader)

        # Swap buffers
        self.pos = self.pos1 if self.pos == self.pos2 else self.pos2
        self.particles = self.particles1 if self.particles == self.particles2 else self.particles2

    def init_particles(self):
        count = 10000
        area = 60.0
        speed = 5.0

        def gen():
            for i in range(count):
                # Position
                yield random.uniform(-area, area)
                yield random.uniform(-area, area)
                yield random.uniform(-area, area)
                # Velocity
                yield random.uniform(-speed, speed)
                yield random.uniform(-speed, speed)
                yield random.uniform(-speed, speed)

        # d = list(gen())

        data1 = numpy.fromiter(gen(), count=count * 6, dtype=numpy.float32)
        data2 = numpy.fromiter(gen(), count=count * 6, dtype=numpy.float32)

        self.pos1 = self.ctx.buffer(data1.tobytes())
        self.particles1 = VAO("particles1", mode=mgl.POINTS)
        self.particles1.buffer(self.pos1, '3f 3f', ['in_position', 'in_velocity'])

        self.pos2 = self.ctx.buffer(data2.tobytes())
        self.particles2 = VAO("particles2", mode=mgl.POINTS)
        self.particles2.buffer(self.pos2, '3f 3f', ['in_position', 'in_velocity'])

        # Set initial start buffers
        self.particles = self.particles1
        self.pos = self.pos2
