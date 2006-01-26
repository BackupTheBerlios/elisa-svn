from testGL.common import constants
from testGL.zAPI.zForms import zOpenGLVideo
from testGL.zAPI.zForms import zSDLVideo

def Video():
    if constants.GetVideoMode() == 'OpenGL':
        return zOpenGLVideo.OpenGLVideo()
        
    return zSDLVideo.SDLVideo()
