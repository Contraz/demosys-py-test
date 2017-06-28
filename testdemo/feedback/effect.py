from demosys.effects import effect
from demosys.opengl import geometry
from OpenGL import GL
from OpenGL.arrays.vbo import VBO
from demosys.opengl import VAO
import numpy
import random
from pyrr import matrix44
from pyrr import vector3
import math


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
        # GL.glBlendFunc(GL.GL_ONE, GL.GL_ONE)

        m_proj = self.create_projection(90, 1, 1000)

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
        with self.particles.bind(self.feedback) as s:
            s.uniform_3fv("gravity_pos", gravity_pos)
            s.uniform_1f("gravity_force", gravity_force)
            s.uniform_1f("timedelta", frametime)

        GL.glEnable(GL.GL_RASTERIZER_DISCARD)
        GL.glBindBufferBase(GL.GL_TRANSFORM_FEEDBACK_BUFFER, 0, self.pos)
        GL.glBeginTransformFeedback(GL.GL_POINTS)
        self.particles.draw()
        GL.glEndTransformFeedback()
        GL.glDisable(GL.GL_RASTERIZER_DISCARD)

        # Draw particles
        with self.particles.bind(self.shader) as shader:
            # shader.uniform_mat4("m_proj", self.sys_camera.projection)
            shader.uniform_mat4("m_proj", m_proj)
            shader.uniform_mat4("m_mv", m_mv)
            shader.uniform_sampler_2d(0, "texture0", self.texture)
        self.particles.draw()

        # # Rotate and translate
        # m_mv = self.create_transformation(rotation=(time * 0.02 * gravity_force,
        #                                             time * 0.01 * gravity_force,
        #                                             time * 0.025 * gravity_force),
        #                                   translation=(0.0, 0.0, 0.0))
        #
        # # Apply the rotation and translation from the system camera
        # m_mv = matrix44.multiply(m_mv, self.sys_camera.view_matrix)
        #
        # # Create normal matrix from model-view
        # m_normal = self.create_normal_matrix(m_mv)
        #
        # GL.glDisable(GL.GL_BLEND)
        # GL.glEnable(GL.GL_DEPTH_TEST)
        # with self.cube.bind(self.cube_shader) as s:
        #     s.uniform_mat4("m_proj", m_proj)
        #     s.uniform_mat4("m_mv", m_mv)
        #     s.uniform_mat3("m_normal", m_normal)
        # self.cube.draw()

        # Swap buffers
        self.pos = self.pos1 if self.pos == self.pos2 else self.pos2
        self.particles = self.particles1 if self.particles == self.particles2 else self.particles2

    def init_particles(self):
        count = 100000
        area = 30.0
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
        # data1 = numpy.array(d, dtype=numpy.float32)
        # data2 = numpy.array(d, dtype=numpy.float32)

        self.pos1 = VBO(data1)
        self.particles1 = VAO("particles1", mode=GL.GL_POINTS)
        self.particles1.add_array_buffer(GL.GL_FLOAT, self.pos1)
        self.particles1.map_buffer(self.pos1, "in_position", 3)
        self.particles1.map_buffer(self.pos1, "in_velocity", 3)
        self.particles1.build()

        self.pos2 = VBO(data2)
        self.particles2 = VAO("particles2", mode=GL.GL_POINTS)
        self.particles2.add_array_buffer(GL.GL_FLOAT, self.pos2)
        self.particles2.map_buffer(self.pos2, "in_position", 3)
        self.particles2.map_buffer(self.pos2, "in_velocity", 3)
        self.particles2.build()

        # Set initial start buffers
        self.particles = self.particles1
        self.pos = self.pos2
