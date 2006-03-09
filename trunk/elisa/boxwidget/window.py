from elisa.boxwidget import surface, eventsmanager, events, texture
from elisa.boxwidget.bindings import testgl_impl
from elisa.framework.log import Logger
from elisa.framework.message_bus import MessageBus
import elisa.utils.misc

from twisted.internet import reactor, task

class Window(object):
    """
    Main window boxwidget class
    """
    
    def __init__(self):
        self._logger = Logger()
        self._logger.debug('Window.__init__()', self)
        self._message_bus = MessageBus()
        self._message_bus.register(self, self.on_message)
        self._window_impl = testgl_impl._testGL_Window_Impl()
        self._events_manager = eventsmanager.EventsManager()
        self._focusedsurface = None
        self._Fps = 50
        self._surface_list = []
        self._background_image_path = None
        self._background_is_movie = False
        self._texture = None
    
    def _get_window_impl(self):
        self._logger.debug('Window.(_get_window_impl)', self)
        return self._window_impl
        
    def add_surface(self, surface):
        self._logger.debug('Window.add_surface()', self)
        if surface not in self._surface_list:
            self._surface_list.append(surface)
            
        surface._set_parent(self)
        surface._set_window(self)
        self._window_impl.add_surface(surface._get_surface_impl())
        
        #Call AddSurface on child widget for set window, and parent
        for s in surface._get_child_surface():
            surface.add_surface(s)

    
    def remove_surface(self, surface):
        self._logger.debug('Window.remove_surface()', self)
        if surface in self._surface_list:
            self._surface_list.remove(surface)
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
        self._logger.debug_verbose('Window.refresh()', self)
        
        self._events_manager.process_input_events()
        self._message_bus.dispatch_messages()
        
        for surface in self._surface_list:
            surface.refresh()
        self._window_impl.refresh()
   
    def on_message(self, receiver, message, sender):
        """
        called if new event is fire
        if return False, event will not fired to next event
        """
        self._logger.debug('Window.on_message(' + str(message) + ')', self)
        if isinstance(message, events.InputEvent):
            e = message.get_simple_event()
            if e == events.SE_QUIT:
                self.close()
                
        return True
             
    def close(self):
        """
        close window
        """
        #FIXME : close also added surface
        self._logger.debug('Window.close()', self)
        reactor.stop()

        for surface in self._surface_list:
            surface.close()
  
    def on_load(self):
        """
        called just before main loop starting
        """
        self._logger.debug('Window.on_load()', self)

    def set_background_from_file(self, path_and_file_name=None):
        """
        set widget background image
        """
        self._logger.debug('Window.set_background_from_file()', self)
        self._background_image_path = path_and_file_name
               
        if elisa.utils.misc.file_is_movie(path_and_file_name):
            p = self._appli.get_player_manager().get_player(path_and_file_name)
            p.play()
            self.set_texture(p.get_texture())
            self._background_is_movie = True
        else:
            _texture = texture.Texture()
            _texture.init_texture_from_picture(path_and_file_name)
            self.set_texture(_texture)
            self._background_is_movie = False

    def background_is_movie(self):
        return self._background_is_movie
        
    def set_background_from_buffer(self, buffer, width, height, flip):
         self._window_impl.set_background_from_buffer(buffer, width, height, flip)
    
    def get_background_file(self):
        """
        return path and filename of background image
        """
        self._logger.debug('Window.get_background_file()', self)
        return self._background_image_path
        
    def set_back_color(self, red, green, blue):
        """
        set widget backcolor
        """
        self._logger.debug('Window.set_back_color(()', self)
        self._window_impl.set_back_color(red, green, blue)
        
    def get_texture(self):
        return self._texture
        
    def set_texture(self, texture):
        self._texture = texture
        if texture != None:
            self._window_impl.set_texture(texture._get_surface_impl())  
