import surfacebase

#Video state

class _VideoSurfaceBase(surfacebase._SurfaceBase):

    VS_PLAY = "VS_PLAY"
    VS_STOP = "VS_STOP"
    VS_PAUSE = "VS_PAUSE"

    def __init__(self):
        surfacebase._SurfaceBase.__init__(self)
        self._videofilename = None
        self._videostatus = _VideoSurfaceBase.VS_STOP
        
        
    def SetVideoFile(self, in_videofile):
        self._videofilename = in_videofile
        
    def Play(self):
        self._videostatus = _VideoSurfaceBase.VS_PLAY
        
    def GetStatus(self):
        return self._videostatus
