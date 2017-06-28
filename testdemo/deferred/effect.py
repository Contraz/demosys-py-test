from demosys.effects import effect
from demosys.opengl import geometry
from OpenGL import GL
from pyrr import matrix44
from demosys.deferred import DeferredRenderer
import math


class MyDeferred(DeferredRenderer):
    geo_shader = None
    cube = None

    def render_geometry(self, cam_matrix, projection):
        """Fill geometry buffer"""
        # Moved to effect.draw for now


class DeferredEffect(effect.Effect):
    """Generated default effect"""
    def __init__(self):
        self.renderer = MyDeferred(self.window_width, self.window_height)
        self.cube = geometry.cube(width=8.0, height=8.0, depth=8.0)
        self.floor = geometry.cube(width=200.0, height=0.5, depth=200.0)
        self.geo_shader_texture = self.get_shader("deferred/geometry_texture.glsl")
        self.geo_shader_color = self.get_shader("deferred/geometry_color.glsl")
        self.texture = self.get_texture("deferred/wood.jpg", anisotropy=8.0, mipmap=True)

        self.renderer.add_point_light(position=[0.0, 0.0, 0.0], radius=40.0)

    @effect.bind_target
    def draw(self, time, frametime, target):

        self.renderer.point_lights[0].position = [math.sin(time) * 25,
                                                  0,
                                                  math.cos(time) * 25]

        m_cam = self.sys_camera.view_matrix

        GL.glEnable(GL.GL_DEPTH_TEST)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glFrontFace(GL.GL_CCW)

        # Matrices for cube
        m_mv = self.create_transformation(
            rotation=[time, time / 2, time / 3],
            translation=[0.0, 0.0, -5.0])
        m_mv = matrix44.multiply(m_mv, m_cam)
        m_normal = self.create_normal_matrix(m_mv)

        # Draw cube geometry
        with self.renderer.gbuffer:
            with self.cube.bind(self.geo_shader_texture) as s:
                s.uniform_mat4("m_proj", self.sys_camera.projection.matrix)
                s.uniform_mat4("m_mv", m_mv)
                s.uniform_mat3("m_normal", m_normal)
                s.uniform_sampler_2d(0, "texture0", self.texture)
            self.cube.draw()

            m_floor = matrix44.create_from_translation([0.0, -15.0, 0.0])
            m_floor = matrix44.multiply(m_floor, m_cam)
            m_normal = self.create_normal_matrix(m_floor)
            with self.floor.bind(self.geo_shader_color) as s:
                s.uniform_mat4("m_proj", self.sys_camera.projection.matrix)
                s.uniform_mat4("m_mv", m_floor)
                s.uniform_mat3("m_normal", m_normal)
                s.uniform_4f("color", 1.0, 1.0, 1.0, 1.0)
            self.floor.draw()

        GL.glDisable(GL.GL_DEPTH_TEST)

        self.renderer.render_lights(m_cam, self.sys_camera.projection)
        self.renderer.combine()

        # Debug stuff
        # self.renderer.render_lights_debug(m_cam, self.sys_camera.projection)
        self.renderer.draw_buffers(self.sys_camera.projection.near,
                                   self.sys_camera.projection.far)

        self.renderer.clear()
