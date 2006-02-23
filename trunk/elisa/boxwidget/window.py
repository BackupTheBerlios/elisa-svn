from twisted.internet import reactor, task
import surface
from bindings import testgl_impl


class Window(object):
    """
    Main window boxwidget class
    """
    
    def __init__(self):
        self._window_impl = testgl_impl._testGL_Window_Impl()
        self._focusedsurface = None
        self._Fps = 50
        self._surfacelist = []
    
    def _get_window_impl(self):
        return self._window_impl
        
    def add_surface(self, surface):
        if surface not in self._surfacelist:
            self._surfacelist.append(surface)
        self._window_impl.add_surface(surface._get_surface_impl())
        surface._set_parent(self);
        surface._set_window(self);
    
    def remove_surface(self, surface):
        if surface in self._surfacelist:
            self._surfacelist.remove(surface)
        self._window_impl.remove_surface(surface._get_surface_impl())
                   
    def run(self):
        """
        run main application loop
        """     
        self._WidgetLoopingCall =  task.LoopingCall(self.refresh)
        self._WidgetLoopingCall.start(1.0 / self._Fps)
        self.on_load()
        reactor.run()        

    def refresh(self):
        """
        refresh complete window (draw current frame)
        @return: False if loop stop required, True if noting.
        """
        for surface in self._surfacelist:
            surface.refresh()
        self._window_impl.refresh()
        
    def close(self):
        """
        close window
        """
        reactor.stop()
  
    def on_load(self):
        """
        called just before main loop starting
        """
