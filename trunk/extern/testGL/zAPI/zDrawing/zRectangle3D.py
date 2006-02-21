import pygame
from pygame.locals import *
from zPoint3D import Point3D

class Rectangle3D(object):

    def __init__(self, left=0, top=0, zorder = 0 , width=0, height=0, deep = 0):
    
        self._rect = pygame.Rect(left, top, width, height)
        self._z = zorder;
        self._deep = deep;
        self._z = 0
      
    def GetPygameRect(self):
        return self._rect
          
    def SetSize(self, width, height):
        self._rect.width = width
        self._rect.height = height
        
    def SetLocation(self, x, y, z):
        self._rect.left = x
        self._rect.top = y
        self._z = z
        
    def GetHeight(self):
        return self._Height
        
    def GetWidth(self):
        return self._Width
    
    def Get2DLocation(self):
        return self._rect.left, self._rect.top
      
    def GetLocation(self):
        return self._rect.left, self._rect.top, self._z
        
    def GetSize(self):
        return self._rect.width, self._rect.height, self._deep
    
    def Get2DSize(self):
        return self._rect.size
    
    def GetDeep(self):
        return self._z
                
    def __str__(self):
        return 'Rectangle3D based on ' + self._rect
