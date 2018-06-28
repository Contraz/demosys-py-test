import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = False

SCREENSHOT_PATH = os.path.join(PROJECT_DIR, 'screenshots')

# Profile: any, core, compat
OPENGL = {
    "version": (4, 1),
    "profile": "core",
    "forward_compat": True,
}

WINDOW = {
    "size": (1280, 768),
    "vsync": True,
    "resizable": True,
    "fullscreen": False,
    "title": "demosys-py",
    "cursor": True,
}

MUSIC = os.path.join(PROJECT_DIR, 'resources/music/tg2035.mp3')
TIMER = 'demosys.timers.Timer'
# TIMER = 'demosys.timers.RocketTimer'
# TIMER = 'demosys.timers.RocketMusicTimer'
# TIMER = 'demosys.timers.MusicTimer'

ROCKET = {
    'mode': 'project',
    'rps': 60,
    'project': os.path.join(PROJECT_DIR, 'resources', 'cube.xml'),
    'files': os.path.join(PROJECT_DIR, 'resources', 'tracks'),
}

# What effects to load
EFFECTS = (
    # 'testdemo.bouncingcubes',
    'testdemo.bouncingcubes_instanced',
    # 'testdemo.cube',
    # 'testdemo.deferred',
    # 'demosys.deferred',
    # 'testdemo.feedback',
    # 'testdemo.multilayer',
    'testdemo.rockettest',
)

SHADER_DIRS = (
    os.path.join(PROJECT_DIR, 'resources/shaders'),
)

SHADER_FINDERS = (
    'demosys.core.shaderfiles.finders.FileSystemFinder',
    'demosys.core.shaderfiles.finders.EffectDirectoriesFinder',
)

# Hardcoded paths to shader dirs
TEXTURE_DIRS = (
    os.path.join(PROJECT_DIR, 'resource/textures'),
)

# Finder classes
TEXTURE_FINDERS = (
    'demosys.core.texturefiles.finders.FileSystemFinder',
    'demosys.core.texturefiles.finders.EffectDirectoriesFinder'
)

# Tell demosys how to find shaders split into multiple files
SHADERS = {
    'vertex_shader_suffix': ('vert', '_vs.glsl', '.glslv'),
    'fragment_shader_suffix': ('frag', '_fs.glsl', '.glslf'),
    'geometry_shader_suffix': ('geom', '_gs.glsl', '.glslg'),
}
