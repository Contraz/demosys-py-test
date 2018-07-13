import math

import moderngl as mgl
from pyrr import matrix44

from demosys.effects import effect
from demosys import geometry
from demosys.deferred import DeferredRenderer


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
        self.texture = self.get_texture("deferred/wood.jpg", mipmap=True)

        self.renderer.add_point_light(position=[0.0, 0.0, 0.0], radius=40.0)

    @effect.bind_target
    def draw(self, time, frametime, target):

        self.renderer.point_lights[0].position = [math.sin(time) * 25,
                                                  0,
                                                  math.cos(time) * 25]

        m_cam = self.sys_camera.view_matrix
        self.sys_camera.projection.update(near=1.0, far=250.0)

        self.ctx.enable(mgl.DEPTH_TEST)
        self.ctx.enable(mgl.CULL_FACE)
        self.ctx.front_face = 'ccw'

        # Matrices for cube
        m_mv = self.create_transformation(
            rotation=[time, time / 2, time / 3],
            translation=[0.0, 0.0, -5.0])
        m_mv = matrix44.multiply(m_mv, m_cam)
        m_normal = self.create_normal_matrix(m_mv)

        # Draw cube geometry
        with self.renderer.gbuffer:
            self.geo_shader_texture.uniform("m_proj", self.sys_camera.projection.tobytes())
            self.geo_shader_texture.uniform("m_mv", m_mv.astype('f4').tobytes())
            self.geo_shader_texture.uniform("m_normal", m_normal.astype('f4').tobytes())
            self.texture.use(location=0)
            self.geo_shader_texture.uniform("texture0", 0)
            self.cube.draw(self.geo_shader_texture)

            m_floor = matrix44.create_from_translation([0.0, -15.0, 0.0])
            m_floor = matrix44.multiply(m_floor, m_cam)
            m_normal = self.create_normal_matrix(m_floor)

            self.geo_shader_color.uniform("m_proj", self.sys_camera.projection.tobytes())
            self.geo_shader_color.uniform("m_mv", m_floor.astype('f4').tobytes())
            self.geo_shader_color.uniform("m_normal", m_normal.astype('f4').tobytes())
            self.geo_shader_color.uniform("color", (1.0, 1.0, 1.0, 1.0))
            self.floor.draw(self.geo_shader_color)

        self.renderer.render_lights(m_cam, self.sys_camera.projection)
        self.renderer.combine()

        # Debug stuff
        self.renderer.render_lights_debug(m_cam, self.sys_camera.projection)
        self.renderer.draw_buffers(self.sys_camera.projection.near,
                                   self.sys_camera.projection.far)

        self.renderer.clear()
