import moderngl as mgl

from demosys.effects import effect
from demosys import geometry
# from pyrr import matrix44


class BouncingCube:
    def __init__(self, index, cube, position, rotation):
        self.index = index
        self.cube = cube
        self.position = position
        self.rotation = rotation


class SimpleCubeEffect(effect.Effect):
    """Generated default effect"""
    """Modified by helgrima to include multiple cubes"""

    def __init__(self):
        self.shader = self.get_shader("cube_plain.glsl", local=True)

        self.cube = geometry.cube(10.0, 1.0, 10.0)

        size, spacing = 32, 11.0
        self.cubes = []

        for i in range(size):
            for j in range(size):
                self.cubes.append(
                    BouncingCube((i, j), self.cube, (i * -spacing, 0, j * -spacing), (0, 0, 0)))

    @effect.bind_target
    def draw(self, time, frametime, target):
        self.ctx.enable(mgl.DEPTH_TEST)

        self.shader.uniform("m_proj", self.sys_camera.projection.tobytes())
        self.shader.uniform("m_camera", self.sys_camera.view_matrix.astype('f4').tobytes())

        for cube in self.cubes:
            self.shader.uniform("pos", cube.position)
            self.shader.uniform("time", time * (cube.index[0] * cube.index[1]) + 1)

            cube.cube.draw(self.shader)
