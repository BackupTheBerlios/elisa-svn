import pygame
from pygame.locals import *
from testGL.zAPI import zGstreamer
from testGL.zAPI.zForms import zControl

class SDLVideo(zControl.Control, zGstreamer.GstPlayer):
    
    def __init__(self):
        zGstreamer.GstPlayer.__init__(self, "video/x-raw-yuv,bpp=24,depth=24,format=(fourcc)YV12")
        zControl.Control.__init__(self)
        self._overlay = None
        
    def Draw(self):
        Frame = self.GetCurrentFrame()
        w,h,d = self.GetSize()
        video_width, video_height = self.GetVideoSize()
        #print video_width, video_height
        if Frame != None and video_width == w and video_height == h and self._overlay != None:
            w,h,d = self.GetSize()
            y = 0
            u = w*h
            v = w * h * 5 / 4
            data = Frame.data
            e = len(Frame.data)
            self._overlay.display((Frame.data[y:u],Frame.data[v:e],Frame.data[u:v]))
        else:
            zControl.Control.Draw(self)

    def SetSize(self, Width, Height):
        zControl.Control.SetSize(self, Width, Height)
        self._overlay = pygame.Overlay(YV12_OVERLAY, (Width,Height))
        self._overlay.set_location(self.GetRect().GetPygameRect())
        caps = "video/x-raw-yuv,bpp=24,depth=24,format=(fourcc)YV12,width="+str(Width)+",height="+str(Height)
        self.SetCaps(caps)

    def SetLocation(self, x, y, z):
        zControl.Control.SetLocation(self, x, y, z)
        self._overlay.set_location(self.GetRect().GetPygameRect())
