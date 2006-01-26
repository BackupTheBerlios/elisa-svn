from testGL.common import constants
from testGL.zAPI.zRenderer import zRendererFactory
from testGL.zAPI.zDrawing import zRectangle3D
from testGL.zAPI.zDrawing import zPoint3D

class Control(object):
   
    def __init__(self):
        self._Surface = zRendererFactory.SurfaceFactory()        
        self._SurfaceRectangle = zRectangle3D.Rectangle3D()
        self.SetSize(10, 50)
        self._Text="Control"
        self._BackgroundImagePath = None
        self._BackColorR = 0.0
        self._BackColorG = 0.0
        self._BackColorB = 0.0
        self._Alpha = 255.0
        self._Rotate = zPoint3D.Point3D()

    def GetRect(self):
        return self._SurfaceRectangle
        
    def SetAlpha(self, level):
        self._Alpha = level
        self._Surface.SetAlpha(level)
       
    def SetText(self, v):
        self._Text=v
    
    def GetText(self):
        return self._Text
        
    def GetSurface(self):
        return self._Surface
        
    def SetSurface(self, surface):
        self._Surface = surface
        
    def SetBackgroundImage(self, PathAndFileName, UseAlpha=False):
        self._BackgroundImagePath = PathAndFileName
        self._Surface.SetBackgroundImageFromFile(PathAndFileName, UseAlpha)
    
    def SetBackgroundImageFromBuffer(self, buffer, width, height, UseAlpha=False):
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
