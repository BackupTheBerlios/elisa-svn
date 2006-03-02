from extern.testGL.common import constants
from extern.testGL.zAPI.zRenderer import zOpenGLSurface
from extern.testGL.zAPI.zDrawing import zRectangle3D
from extern.testGL.zAPI.zDrawing import zPoint3D

class Control(object):
   
    def __init__(self):
        self._Surface = zOpenGLSurface.OpenGLSurface()       
        self._SurfaceRectangle = zRectangle3D.Rectangle3D()
        self.SetSize(10, 50)
        self._Text="Control"
        self._BackgroundImagePath = None
        self._BackColorR = 0.0
        self._BackColorG = 0.0
        self._BackColorB = 0.0
        self._Alpha = 255.0
        self._Rotate = zPoint3D.Point3D()
        self._Visible = True
        self._Form = None
        
    def _SetForm(self, in_form):
        self._Form = in_form
    
    def set_background_from_surface(self, surface):
        surface.GetSurface().add_surface_with_same_texture( self.GetSurface())   
        
    def GetForm(self):
        return self._Form
        
    def Show(self):
        self._Visible = True
        if self.GetForm() != None:
            self.GetForm().ReorderControls()
    
    def Hide(self):
        self._Visible = False
    
    def Visible(self):
        return self._Visible
        
    def GetRect(self):
        return self._SurfaceRectangle
        
    def SetAlpha(self, level):
        self._Alpha = level
        self._Surface.SetAlpha(level)
       
    def SetText(self, v):
        #print "set text to " + str(v) + " on " + str(self._Surface)
        self._Text=v
    
    def GetText(self):
        return self._Text
        
    def GetSurface(self):
        return self._Surface
        
    def SetSurface(self, surface):
        self._Surface = surface
        
    def SetBackgroundImageFromFile(self, PathAndFileName, UseAlpha=False):
        self._BackgroundImagePath = PathAndFileName
        self._Surface.SetBackgroundImageFromFile(PathAndFileName, UseAlpha)
    
    def SetBackgroundImageFromBuffer(self, buffer, width, height, UseAlpha=False, UseExistingTexture = True):
        if UseExistingTexture == False: self._Surface.RecreateTexture()
        self._Surface.SetBackgroundImageFromBuffer2( buffer, width, height, UseAlpha)
        
    def GetBackgroundImage(self):
        return self._BackgroundImage   
        
    def SetSize(self, Width, Height):
        self._SurfaceRectangle.SetSize( Width, Height)
        self._Surface.SetSize( Width, Height)
       
    def GetSize(self):
        return self._SurfaceRectangle.GetSize()

    def SetLocation(self, x, y, z):
        if z != self._SurfaceRectangle.GetDeep() :
            constants.GetForm()._SortzOderDrawing()

        self._SurfaceRectangle.SetLocation(x, y, z)
        self._Surface.SetLocation(x, y, z)
    
    def GetLocation(self):
        return self._SurfaceRectangle.GetLocation() 
    
    def Draw(self):
        self._Surface.Render()
    
    def SetBackColor(self, Red, Green, Blue):
        self._BackColorR = Red
        self._BackColorG = Green
        self._BackColorB = Blue
        self._Surface.SetBackColor(Red, Green, Blue)

    def OnUnload(self): pass
