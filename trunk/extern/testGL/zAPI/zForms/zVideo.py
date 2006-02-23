from extern.testGL.common import constants
from extern.testGL.zAPI.zForms import zOpenGLVideo

def Video():
    if constants.GetVideoMode() == 'OpenGL':
        return zOpenGLVideo.OpenGLVideo()
        
    return zSDLVideo.SDLVideo()
