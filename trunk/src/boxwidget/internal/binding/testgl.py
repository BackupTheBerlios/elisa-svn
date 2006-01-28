from boxwidget.internal import windowbase, surfacebase, eventsmanagerbase, videosurfacebase
from boxwidget import event
from testGL.zAPI.zForms import zForm,zPictureBox,zOpenGLVideo
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

    def SetBackgroundFromFile(self, PathAndFileName=None):
        windowbase._WindowBase.SetBackgroundFromFile(self, PathAndFileName)
        self.GetNativeSurface().SetBackgroundImageFromFile(PathAndFileName)
        
    def Close(self):
        self.GetNativeSurface().DisplayStats()
        windowbase._WindowBase.Close(self)
     
    def AddSurfaceToNativeWindow(self, in_surface):
        self.GetNativeSurface().AddControl(in_surface.GetNativeSurface())
        (_tx, _ty, _tz) = in_surface.GetAbsoluteLocation()
        in_surface.GetNativeSurface().SetLocation(_tx, _ty, _tz)

    def RemoveSurfaceFromNativeWindow(self, in_surface):
        self.GetNativeSurface().RemoveControl(in_surface.GetNativeSurface())
        
class zSurface(surfacebase._SurfaceBase):
    """
    surface binding class for testGL render engine
    """   
    def __init__(self):
        surfacebase._SurfaceBase.__init__(self)
        self.SetNaviteSurface(zPictureBox.PictureBox())
        
    def SetSize(self, Width, Height):  
        surfacebase._SurfaceBase.SetSize(self, Width, Height)
        self.GetNativeSurface().SetSize(Width, Height)
        
    def SetLocation(self, x, y, z):
        #if parent defined, location of widget is relative
        surfacebase._SurfaceBase.SetLocation(self, x, y, z)
        (_tx, _ty, _tz) = self.GetAbsoluteLocation()
        self.GetNativeSurface().SetLocation(_tx, _ty, _tz)
    
    def SetBackColor(self, Red, Green, Blue):
        self.GetNativeSurface().SetBackColor(Red, Green, Blue)

    def SetBackgroundFromFile(self, PathAndFileName=None):
        surfacebase._SurfaceBase.SetBackgroundFromFile(self, PathAndFileName)
        self.GetNativeSurface().SetBackgroundImageFromFile(PathAndFileName, True)
        
    def SetAlphaLevel(self, in_level):
        surfacebase._SurfaceBase.SetAlphaLevel(self, in_level)
        self.GetNativeSurface().SetAlpha(in_level*2.55)
        
    def Hide(self):
        surfacebase._SurfaceBase.Hide(self)
        self.GetNativeSurface().Hide()

    def Show(self):
        surfacebase._SurfaceBase.Show(self)
        self.GetNativeSurface().Show()

class zVideoSurface(videosurfacebase._VideoSurfaceBase):

    def __init__(self):
        videosurfacebase._VideoSurfaceBase.__init__(self)
        self.SetNaviteSurface(zOpenGLVideo.OpenGLVideo())
        
    def SetVideoFile(self, in_videofile):
        videosurfacebase._VideoSurfaceBase.SetVideoFile(self, in_videofile)
        self.GetNativeSurface().SetURI("file://" + str(in_videofile))
        
    def Play(self):
        videosurfacebase._VideoSurfaceBase.Play(self)
        self.GetNativeSurface().Play()
        
    def SetSize(self, Width, Height):  
        videosurfacebase._VideoSurfaceBase.SetSize(self, Width, Height)
        self.GetNativeSurface().SetSize(Width, Height)
        
    def SetLocation(self, x, y, z):
        #if parent defined, location of widget is relative
        videosurfacebase._VideoSurfaceBase.SetLocation(self, x, y, z)
        (_tx, _ty, _tz) = self.GetAbsoluteLocation()
        self.GetNativeSurface().SetLocation(_tx, _ty, _tz)
    
    def SetBackColor(self, Red, Green, Blue):
        self.GetNativeSurface().SetBackColor(Red, Green, Blue)

    def SetBackgroundFromFile(self, PathAndFileName=None):
        videosurfacebase._VideoSurfaceBase.SetBackgroundFromFile(self, PathAndFileName)
        self.GetNativeSurface().SetBackgroundImageFromFile(PathAndFileName, True)
        
    def SetAlphaLevel(self, in_level):
        videosurfacebase._VideoSurfaceBase.SetAlphaLevel(self, in_level)
        self.GetNativeSurface().SetAlpha(in_level*2.55)

    def Hide(self):
        videosurfacebase._VideoSurfaceBase.Hide(self)
        self.GetNativeSurface().Hide()

    def Show(self):
        videosurfacebase._VideoSurfaceBase.Show(self)
        self.GetNativeSurface().Show()
        
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
                return event.Event(event.DEV_KEYBOARD, event.KEY_SPACE, event.SE_MENU)
            if in_pyevent.key == pygame.K_ESCAPE:
                return event.Event(event.DEV_KEYBOARD, event.KEY_ESCAPE, event.SE_QUIT)
                
        return None
