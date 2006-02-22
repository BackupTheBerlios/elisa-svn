from extern.testGL.zAPI.zDrawing import zRectangle3D

class SurfaceBase(object):
        
    def __init__(self):
        self._BackColorR = 255
        self._BackColorG = 255
        self._BackColorB = 255
        self._Alpha = 255
        self._SurfaceRectangle = zRectangle3D.Rectangle3D()
        self._SurfaceRectangle.SetSize(10, 10)
        self._SurfaceRectangle.SetLocation(0.0, 0.0, 0.0)
        
    def SetBackColor(self, Red, Green, Blue):
        self._BackColorR = Red
        self._BackColorG = Green
        self._BackColorB = Blue
     
    def SetAlpha(self, level):
        self._Alpha = level
        
    def GetRect(self):
        return self._SurfaceRectangle
    
    def GetBackColor(self):
        return self._BackColorR, self._BackColorG, self._BackColorB
    
    def GetBackColorWithAlpha(self):
        return self._BackColorR, self._BackColorG, self._BackColorB, self._Alpha
            
    def SetSize(self, Width, Height):
        self._SurfaceRectangle.SetSize( Width, Height)
       
    def GetSize(self):
        return self._SurfaceRectangle.GetSize()

    def SetLocation(self, x, y, z):
        self._SurfaceRectangle.SetLocation(x, y, z)
        
    def SetTextureOrder(self, order): pass
        
    def SetBackgroundImageFromFile(self, FileName, UseAlpha=False): pass

    def SetBackgroundImageFromBuffer(self, buffer, width, height, UseAlpha=False): pass
    
    def LoadTexture(self): pass
    
    def Render(self): pass
        
    def ApplyRotation(self, Rotate): pass

class RendererBase(SurfaceBase):

    def __init__(self):
        Surface.__init__(self)
        
    def init(self): pass

    def ClearScreen(self): pass
    
    def DrawBackground(self): pass
    
    def Blit(self, pyrect) : pass
    
    def BeforeRender(self): pass
            
    def AfterRender(self): pass
