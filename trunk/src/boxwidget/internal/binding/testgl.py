from boxwidget.internal import windowbase, surfacebase, eventsmanagerbase
from boxwidget import event
from testGL.zAPI.zForms import zForm,zPictureBox
import pygame
from pygame.locals import *

class zWindow(windowbase._WindowBase):
    """
    windows binding class for testGL renderEngine
    """

    def __init__(self):
        windowbase._WindowBase.__init__(self)
        self.SetNaviteSurface(zForm.Form())
        self.GetNativeSurface().FpsEnable = False
    
    def Refresh(self):
        windowbase._WindowBase.Refresh(self)
        #testGL will refresh automaticly child widget
        self.GetNativeSurface().Refresh()

    def SetBackColor(self, Red, Green, Blue):
        self.GetNativeSurface().SetBackColor(Red, Green, Blue)

    def SetBackgroundImage(self, PathAndFileName):
        windowbase._WindowBase.SetBackgroundImage(self, PathAndFileName)
        self.GetNativeSurface().SetBackgroundImage(PathAndFileName)
        
    def Close(self):
        self.GetNativeSurface().DisplayStats()
        windowbase._WindowBase.Close(self)
     
    def AddSurfaceToNativeWindow(self, in_surface):
        windowbase._WindowBase.AddSurfaceToNativeWindow(self, in_surface)
        if in_surface.Visible() == True:
            self.GetNativeSurface().AddControl(in_surface.GetNativeSurface())
            (_tx, _ty, _tz) = in_surface.GetAbsoluteLocation()
            in_surface.GetNativeSurface().SetLocation(_tx, _ty, _tz)

    def RemoveSurfaceFromNativeWindow(self, in_surface):
        windowbase._WindowBase.RemoveSurfaceFromNativeWindow(self, in_surface)
        self.GetNativeSurface().RemoveControl(in_surface.GetNativeSurface())
        
class zSurface(surfacebase._SurfaceBase):
    """
    surface binding class for testGL render engine
    """   
    def __init__(self):
        surfacebase._SurfaceBase.__init__(self)
        self.SetNaviteSurface(zPictureBox.PictureBox())
        
    def SetSize(self, Width, Height):  
        self.GetNativeSurface().SetSize(Width, Height)
        
    def SetLocation(self, x, y, z):
        #if parent defined, location of widget is relative
        surfacebase._SurfaceBase.SetLocation(self, x, y, z)
        (_tx, _ty, _tz) = self.GetAbsoluteLocation()
        self.GetNativeSurface().SetLocation(_tx, _ty, _tz)
    
    def SetBackColor(self, Red, Green, Blue):
        self.GetNativeSurface().SetBackColor(Red, Green, Blue)

    def SetBackgroundImage(self, PathAndFileName):
        surfacebase._SurfaceBase.SetBackgroundImage(self, PathAndFileName)
        self.GetNativeSurface().SetBackgroundImage(PathAndFileName, True)
        
    def SetAlphaLevel(self, in_level):
        surfacebase._SurfaceBase.SetAlphaLevel(self, in_level)
        self.GetNativeSurface().SetAlpha(in_level*2.55)

class zEventsManager(eventsmanagerbase._EventsManagerBase):

    def __init__(self):
        eventsmanagerbase._EventsManagerBase.__init__(self)
        
    def GetEventQueue(self):
        for event in pygame.event.get():
            _boxevent = self.PyGameEventConverter(event)
            if _boxevent != None:
                self.PushEvent(_boxevent)
        
        return eventsmanagerbase._EventsManagerBase.GetEventQueue(self)
            
    def PyGameEventConverter(self, in_pyevent):
    
        if in_pyevent.type == pygame.QUIT:   
            return event.Event(event.DEV_SYSTEM, event.EVENT_QUIT, event.SE_QUIT)
        if in_pyevent.type == pygame.KEYDOWN:
            if in_pyevent.key == pygame.K_LEFT:
                return event.Event(event.DEV_KEYBOARD, event.KEY_LEFT, event.SE_LEFT)
            if in_pyevent.key == pygame.K_RIGHT:
                return event.Event(event.DEV_KEYBOARD, event.KEY_RIGHT, event.SE_RIGHT)
            if in_pyevent.key == pygame.K_UP:
                return event.Event(event.DEV_KEYBOARD, event.KEY_UP, event.SE_UP)
            if in_pyevent.key == pygame.K_DOWN:
                return event.Event(event.DEV_KEYBOARD, event.KEY_DOWN, event.SE_DOWN)
            if in_pyevent.key == pygame.K_RETURN:
                return event.Event(event.DEV_KEYBOARD, event.KEY_RETURN, event.SE_OK)
            if in_pyevent.key == pygame.K_SPACE:
                return event.Event(event.DEV_KEYBOARD, event.KEY_SPACE, event.SE_OK)
            if in_pyevent.key == pygame.K_ESCAPE:
                return event.Event(event.DEV_KEYBOARD, event.KEY_ESCAPE, event.SE_QUIT)
                
        return None
        
       
