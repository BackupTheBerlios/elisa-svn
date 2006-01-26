from testGL.common import constants
import pygame
from pygame.locals import *
from testGL.zAPI.zRenderer import zBaseClass

class SDLSurface(zBaseClass.SurfaceBase):

    def __init__(self):
        zBaseClass.SurfaceBase.__init__(self)
        self._Screen = pygame.display.get_surface()
        self._Surface = None
        self._Refresh = True
        self._ImageFileName = None
        self._UpdateSDLSurface()
        
    def Render(self):
        zBaseClass.SurfaceBase.Render(self)
        if self._Refresh == True:
            renderer = common.GetForm()._GetRenderer()
            self._UpdateSDLSurface()
            self._Refresh = False
            self._Screen.blit(self._Surface, self.GetRect().Get2DLocation() )
            pygame.display.flip()
                
    def _UpdateSDLSurface(self):
        if self._ImageFileName == None:
            self._Surface = pygame.Surface(self.GetRect().GetPygameRect().size)
            self._Surface.fill((self.GetBackColor()[0], self.GetBackColor()[1], self.GetBackColor()[2]))
        else:
            s = pygame.image.load(self._ImageFileName)
            self._Surface = pygame.transform.scale(s, self.GetRect().GetPygameRect().size)        

    def SetSize(self, Width, Height):
        zBaseClass.SurfaceBase.SetSize(self, Width, Height)
        self._Refresh = True
        
    def SetBackColor(self, Red, Green, Blue):
        zBaseClass.SurfaceBase.SetBackColor(self, Red, Green, Blue)
        self._Refresh = True
        
    def SetLocation(self, x, y, z):
        zBaseClass.SurfaceBase.SetLocation(self, x, y, z)
        self._Refresh = True

    def SetBackgroundImageFromFile(self, FileName, UseAlpha=False):
        zBaseClass.SurfaceBase.SetBackgroundImageFromFile(self, FileName, UseAlpha)
        if FileName == None:
            self._ImageFileName = None
        else:
            self._ImageFileName = FileName
            self._Refresh = True
