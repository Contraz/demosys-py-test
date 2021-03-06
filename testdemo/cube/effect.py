import moderngl as mgl
# import math
from demosys.effects import effect
from demosys import geometry
from demosys.opengl import FBO


class CubeEffect(effect.Effect):
    """Simple effect drawing a textured cube"""
    def __init__(self):
        self.cube_shader1 = self.get_shader('cube/cube_multi_fade.glsl')
        self.cube_shader2 = self.get_shader('cube/cube_texture_light.glsl')
        self.quad_shader = self.get_shader('quad_fs_uvscale.glsl', local=False)

        self.texture1 = self.get_texture('cube/texture.png')
        self.texture2 = self.get_texture('cube/GreenFabric.png')

        self.cube = geometry.cube(4.0, 4.0, 4.0)

        v = 100.0
        r = (-v, v)

        self.points = geometry.points_random_3d(50_000, range_x=r, range_y=r, range_z=r, seed=7656456)
        self.quad = geometry.quad_fs()
        self.fbo = FBO.create((512, 512), depth=True)

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.enable(mgl.DEPTH_TEST)
        self.ctx.enable(mgl.CULL_FACE)

        mv_m = self.create_transformation(rotation=(time * 1.2, time * 2.1, time * 0.25),
                                          translation=(0.0, 0.0, -8.0))
        normal_m = self.create_normal_matrix(mv_m)
        proj_m = self.create_projection(fov=60.0, ratio=1.0)

        with self.fbo:
            shader = self.cube_shader1
            shader.uniform("m_proj", proj_m.astype('f4').tobytes())
            shader.uniform("m_mv", mv_m.astype('f4').tobytes())
            shader.uniform("m_normal", normal_m.astype('f4').tobytes())
            self.texture1.use(location=0)
            self.texture2.use(location=1)
            shader.uniform("texture0", 0)
            shader.uniform("texture1", 1)
            shader.uniform("time", time)
            self.cube.draw(shader)

        # Test camera
        self.sys_camera.projection.update(fov=75, near=0.1, far=1000)
        # self.sys_camera.set_position(10.0, 0.0, 10.0)
        # self.sys_camera.set_position(math.sin(time) * 10,
        #                                  math.sin(time * 10),
        #                                  math.cos(time) * 10)
        # view_m = self.sys_camera.look_at(pos=[0.0, 0.0, 0.0])

        view_m = self.sys_camera.view_matrix
        normal_m = self.create_normal_matrix(view_m)

        shader = self.cube_shader2
        shader.uniform("m_proj", self.sys_camera.projection.tobytes())
        shader.uniform("m_mv", view_m.astype('f4').tobytes())
        shader.uniform("m_normal", normal_m.astype('f4').tobytes())
        self.fbo.color_buffers[0].use(location=0)
        # self.texture1.use()
        shader.uniform("texture0", 0)
        shader.uniform("time", time)
        shader.uniform("lightpos", (0.0, 0.0, 0.0))
        self.points.draw(shader)

        self.fbo.clear(red=0.5, green=0.5, blue=0.5, alpha=1.0, depth=1.0)
