from extern.testGL.zAPI import zGstreamer
from extern.testGL.zAPI.zForms import zControl

class OpenGLVideo(zControl.Control, zGstreamer.GstPlayer):

    def __init__(self):
        zControl.Control.__init__(self)
        zGstreamer.GstPlayer.__init__(self,"video/x-raw-rgb,bpp=24,depth=24")      
        self.GetSurface().SetTextureOrder(1)
        
    def Draw(self):
        Frame = self._MySink.GetCurrentFrame()
        if self._videowidth == None:
            self._videowidth = self._MySink.GetWidth()
        if self._videoheight == None:
            self._videoheight = self._MySink.GetHeight() 
        if Frame != None and self._videoheight != None and self._videowidth != None:
            self.GetSurface().SetBackgroundImageFromBuffer(Frame, self._videowidth, self._videoheight, )
        zControl.Control.Draw(self)

    def OnUnload(self):
        self.Stop()
