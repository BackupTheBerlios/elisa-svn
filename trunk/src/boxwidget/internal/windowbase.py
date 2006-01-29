from twisted.internet import reactor, task
import surfacebase


class _WindowBase(surfacebase._SurfaceBase):
    """
    Main window boxwidget base class
    do not use directly
    """
    
    def __init__(self):
        surfacebase._SurfaceBase.__init__(self)
        "native binded widget framework window"
        self._SetWindow(self)
        self._focusedsurface = None
        self._Fps = 50
        
    def AddSurfaceToNativeWindow(self, in_surface):
        """
        Add surface to native window
        """

    def RemoveSurfaceFromNativeWindow(self, in_surface):
        """
        remove surface to native window
        """
    
    def Run(self):
        """
        run main application loop
        """
         
        self.OnLoad()
        self._WidgetLoopingCall =  task.LoopingCall(self.Refresh)
        self._WidgetLoopingCall.start(1.0 / self._Fps)
        reactor.run()        

    def Refresh(self):
        """
        refresh complete window (draw current frame)
        @return: False if loop stop required, True if noting.
        """
        surfacebase._SurfaceBase.Refresh(self)
        
    def Close(self):
        """
        close window
        """
        reactor.stop()
  
    def OnLoad(self):
        """
        called just before main loop starting
        """
        
    def _FireEventToAllWidget(self, in_event):
        """
        internal function who fire a event to all widget added to the window
        """
        self._RecusiveEventFire(self._GetChildSurface(), in_event)
        self.OnEvent(in_event)
            
    def _RecusiveEventFire(self, in_surfacelist, in_event):
        for s in in_surfacelist:
            if s.OnEvent(in_event) == False:
                break
            self._RecusiveEventFire(s._GetChildSurface(), in_event)
                 
    def SetFocusedSurface(self, in_surface):
        self._focusedsurface = in_surface

    def GetFocusedSurface(self):
        return self._focusedsurface 
