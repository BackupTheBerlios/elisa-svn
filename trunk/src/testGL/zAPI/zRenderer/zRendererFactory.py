from testGL.common import constants
from testGL.zAPI.zRenderer import zOpenGLRenderer
from testGL.zAPI.zRenderer import zOpenGLSurface
from testGL.zAPI.zRenderer import zSDLRenderer
from testGL.zAPI.zRenderer import zSDLSurface

def RendererFactory():
    VideoMode = constants.GetVideoMode()
    if VideoMode == 'OpenGL':
        return zOpenGLRenderer.OpenGLRenderer()
    else:
        return zSDLRenderer.SDLRenderer()
        
def SurfaceFactory():
    VideoMode = constants.GetVideoMode()
    if VideoMode == 'OpenGL':
        return zOpenGLSurface.OpenGLSurface()
    else:
        return zSDLSurface.SDLSurface()
