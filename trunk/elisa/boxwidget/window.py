from elisa.boxwidget import surface, eventsmanager
from elisa.boxwidget.bindings import testgl_impl
from elisa.framework.log import Logger

from twisted.internet import reactor, task

class Window(object):
    """
    Main window boxwidget class
    """
    
    def __init__(self):
        self._logger = Logger()
        self._logger.debug('Window.__init__()', self)
        self._window_impl = testgl_impl._testGL_Window_Impl()
        self._events_manager = eventsmanager.EventsManager()
        self._focusedsurface = None
        self._Fps = 50
        self._surfacelist = []
        self._background_image_path = None
    
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
        
        for current_event in self._events_manager.get_event_queue():
            e = current_event.get_simple_event()
            #self._FireEventToAllWidget(currentevent)
            if e == event.SE_QUIT:
                self.close()
        
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

    def set_background_from_file(self, path_and_file_name=None):
        """
        set window background image
        """
        self._logger.debug('Surface.set_background_from_file(' + str(path_and_file_name) + ')', self)
        self._background_image_path = path_and_file_name
        self._window_impl.set_background_from_file(path_and_file_name)
        