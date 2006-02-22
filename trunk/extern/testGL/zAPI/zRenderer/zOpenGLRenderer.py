from extern.testGL.common import constants
from OpenGL.GL import *
from OpenGL.GLU import *
from extern.testGL.zAPI.zRenderer import zBaseClass
from extern.testGL.zAPI.zRenderer import zOpenGLSurface

class OpenGLRenderer(zBaseClass.RendererBase):
    
    def __init__(self):
        self._BackgroundSurface = None
        self._CameraZposition = -500.0
        self._AspectRatio = 1.0;
        self._width, self._height = constants.GetWindowSize()
        self._DrawBackground = False
        
    def init(self):
        
        glMatrixMode(GL_MODELVIEW)
        glShadeModel(GL_FLAT)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    	#glHint( GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST )
    	glClearColor(0.0, 0.0, 0.0, 0.0)
        if self._height>0:     
            self._AspectRatio = self._width / float(self._height);
    
        glMatrixMode(GL_PROJECTION)
    	glLoadIdentity()
        glViewport(0, 0, self._width, self._height)
        gluPerspective(45,self._AspectRatio,1,self._CameraZposition)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0,0.0,-self._CameraZposition,0.0,0.0,0.0,0.0,1.0,0.0)
        
        xmin, ymin = self.LocalToWorld(0, 0)
        xmax, ymax = self.LocalToWorld(self._width, self._height)
        self._world_width = xmax - xmin
        self._world_height = -(ymax - ymin)

    def GetWorldSize(self):
        return self._world_width, self._world_height
        
    def LocalToWorld(self, x, y):	
		matrix = glGetDoublev(GL_MODELVIEW_MATRIX)
		proj = glGetDoublev(GL_PROJECTION_MATRIX)
		viewport = glGetIntegerv (GL_VIEWPORT)
		Worldx, Worldy, Worldz = gluUnProject ( x, y, 1, matrix, proj, viewport)
		return -Worldx, Worldy
		
    def ClearScreen(self):
         glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
         
    def DrawBackground(self) :
        if self._DrawBackground == True:
            
            glPushMatrix()
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            
            self._BackgroundSurface.Render()           
            
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)
            glPopMatrix() 
    
    def SetBackColor(self, Red, Green, Blue):
        zBaseClass.RendererBase.SetBackColor(self, Red, Green, Blue)
        glClearColor(Red, Green, Blue, 0.0)
        
    def SetBackgroundImageFromFile(self, PathAndFileName):
        zBaseClass.SurfaceBase.SetBackgroundImageFromFile(self, PathAndFileName)
        if self._BackgroundSurface == None:
            self._BackgroundSurface = zOpenGLSurface.OpenGLSurface(False)
            self._BackgroundSurface.SetSize(2.0, 2.0)
            self._BackgroundSurface.SetLocation(-1.0, 1.0, 1.0)
            self._BackgroundSurface.SetBackColor(255.0, 255.0, 255.0)
        self._BackgroundSurface.SetBackgroundImageFromFile(PathAndFileName)
        
        if PathAndFileName == None:
            self._DrawBackground = False
        else:
            self._DrawBackground = True

