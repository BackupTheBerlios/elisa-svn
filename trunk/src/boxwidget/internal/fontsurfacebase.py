import surfacebase

#Video state

class _FontSurfaceBase(surfacebase._SurfaceBase):

    def __init__(self):
        surfacebase._SurfaceBase.__init__(self)
        self._fontsize = 32
        
    def SetFontSize(self, in_size):
        self._fontsize = in_size

    def GetFontSize(self):
        return self._fontsize
        
    def SetText(self, in_text):
        self._text = in_text
        
    def GetText(self):
        return self._text
