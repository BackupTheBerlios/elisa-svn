from twisted.internet import reactor, task
import surface
from bindings import testgl_impl

from elisa.framework.log import Logger


class Window(object):
    """
    Main window boxwidget class
    """
    
    def __init__(self):
        self._logger = Logger()
        self._logger.debug('Window.__init__()', self)
        self._window_impl = testgl_impl._testGL_Window_Impl()
        self._focusedsurface = None
        self._Fps = 50
        self._surfacelist = []
    
    def _get_window_impl(self):
        self._logger.debug('Window.(_get_window_impl)', self)
        return self._window_impl
        
    def add_surface(self, surface):
        self._logger.debug('Window.add_surface()', self)
        if surface not in self._surfacelist:
            self._surfacelist.append(surface)
            
        surface._set_parent(self)
        surface._set_window(self)
        self._window_impl.add_surface(surface._get_surface_impl())
        
        #Call AddSurface on child widget for set window, and parent
        for s in surface._get_child_surface():
            surface.add_surface(s)

    
    def remove_surface(self, surface):
        self._logger.debug('Window.remove_surface()', self)
        if surface in self._surfacelist:
            self._surfacelist.remove(surface)
        self._window_impl.remove_surface(surface._get_surface_impl())
                   
    def run(self):
        """
        run main application loop
        """   
        self._logger.debug('Window.run()', self)  
        self._WidgetLoopingCall =  task.LoopingCall(self.refresh)
        self._WidgetLoopingCall.start(1.0 / self._Fps)
        self.on_load()
        reactor.run()        

    def refresh(self):
        """
        refresh complete window (draw current frame)
        @return: False if loop stop required, True if noting.
        """
        #self._logger.debug('Window.refresh()', self)
        for surface in self._surfacelist:
            surface.refresh()
        self._window_impl.refresh()
        
    def close(self):
        """
        close window
        """
        self._logger.debug('Window.close()', self)
        reactor.stop()
  
    def on_load(self):
        """
        called just before main loop starting
        """
        self._logger.debug('Window.on_load()', self)
