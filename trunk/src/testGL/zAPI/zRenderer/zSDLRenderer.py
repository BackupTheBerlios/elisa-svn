from testGL.common import constants
import pygame
from pygame.locals import *
from testGL.zAPI.zRenderer import zBaseClass
from testGL.zAPI.zRenderer import zSDLSurface

class SDLRenderer(zBaseClass.RendererBase):

    def __init__(self):
        zBaseClass.RendererBase.__init__(self)
        self._Screen = pygame.display.get_surface()
        self._BackGroundSurface = None;
            
        
    def SetBackgroundImage(self, PathAndFileName):
        if PathAndFileName == None:
            self._BackGroundSurface = None
            
        surface = pygame.image.load(PathAndFileName)
        self._BackGroundSurface = pygame.transform.scale(surface, common.GetWindowSize())
        self.RefeshBackground()
        

    def RefeshBackground(self):
        self._Screen.blit(self._BackGroundSurface, (0,0)) 
        pygame.display.flip()
        
    def Blit(self, pyrect) :
        if self._Screen != None and self._BackGroundSurface != None :
            screen.blit(self._BackGroundSurface, pyrect)
