from elisa.boxwidget.bindings import testgl_impl
from elisa.boxwidget import texture
from elisa.player.player import Player
from elisa.framework.log import Logger
from elisa.framework.message_bus import MessageBus
from elisa.framework import common

import elisa.utils.misc
import time

class Surface(object):  
    """
    class of Surface
    """
    
    def __init__(self, name='Surface'):
        self._logger = Logger()
        self._name=name
        self._logger.debug('Surface.__init__()', self)
        self._message_bus = MessageBus()
        self._message_bus.register(self, self.on_message)
        self._surface_impl = testgl_impl._testGL_Surface_Impl()
        self._surface_list = []
        self._parentsurface = None
        self._x = 0
        self._y = 0
        self._z = 0
        self._width = 100
        self._height = 100
        self._alphalevel = 100
        self._background_image_path = None
        self._window = None
        self._visible = True
        self._visible_r = True
        self._background_is_movie = False
        self._texture = None
        self._appli = common.get_application()
        
        self._surface_impl.set_size(self._width, self._height)

    def get_texture(self):
        return self._texture
        
    def set_texture(self, texture):
        self._texture = texture
        if texture != None:
            self._surface_impl.set_texture(texture._get_surface_impl())  
 
    def pretty_print(self, deep = 0):
        """ Textual representation of the tree. This method is recursive
        """
        representation = " " * deep + "- %s (%s items)" % (self._name,
                                              len(self._surface_list))
        deep += 1
        for surface in self._surface_list:
            representation += "\n" + surface.pretty_print(deep)
        return representation
    
    def on_message(self, receiver, message, sender):
        """
        called if new event is fire
        if return False, event will not fired to next event
        """
        self._logger.debug('Surface.on_message(' + str(message) + ')', self)
        return True
    
    def close(self):
        for surface in self._surface_list:
            surface.close()

    def _get_surface_impl(self):
        self._logger.debug('Surface._get_surface_impl()', self)
        return self._surface_impl

    def set_alpha_level(self, level, apply_to_child=False):
        """
        set the alpha level in percent of the widget [0 to 100%] of opacity
        """
        self._logger.debug('Surface.set_alpha_level(' + str(level) + ')', self)
        self._alphalevel = level
        self._surface_impl.set_alpha_level(level)
        
        if apply_to_child == True:
            for s in self._surface_list:
                s.set_alpha_level(level, apply_to_child)
            

    def get_alpha_level(self):
        return self._alphalevel
        
    def set_background_from_file(self, path_and_file_name=None):
        """
        set widget background image
        """
        self._logger.debug('Surface.set_background_from_file()', self)
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
         self._surface_impl.set_background_from_buffer(buffer, width, height, flip)
    
    def get_background_file(self):
        """
        return path and filename of background image
        """
        self._logger.debug('Surface.get_background_file()', self)
        return self._background_image_path
        
    def set_size(self, width, height):
        """
        define the size in 2D plan
        """
        self._logger.debug('Surface.set_size()', self)
        self._width = width
        self._height = height
        self._surface_impl.set_size(width, height)
    
    def get_size(self):
        """
        return current size
        """
        self._logger.debug('Surface.get_size()', self)
        return (self._width, self._height)

    def set_location(self, x, y, z):
        """
        set location of widget (relative to parent)
        """
        self._logger.debug_verbose('Surface.set_location()', self)
        self._x = x
        self._y = y
        self._z = z
        (ax, ay, az) = self.get_absolute_location()
        self._surface_impl.set_location(ax, ay, az)
        
        for child in self._surface_list: child._refresh_location()
    
    def _refresh_location(self):
        self._logger.debug_verbose('Surface._refresh_location()', self)
        self.set_location(self._x, self._y, self._z)
    
    def set_background_from_surface(self, surface):
        self._surface_impl.set_background_from_surface(surface._get_surface_impl())
    
    def get_location(self):
        """ 
        get 3D location (relative to parent)
        """ 
        self._logger.debug('Surface.get_location()', self)
        return (self._x, self._y, self._z)
    
    def get_absolute_location(self):
        self._logger.debug_verbose('Surface.get_absolute_location()', self)
        _cx = self._x
        _cy = self._y
        _cz = self._z
                
        if self._parentsurface != None and isinstance(self._parentsurface, Surface) :
            (_tx, _ty, _tz) = self._parentsurface.get_absolute_location()
            _cx += _tx
            _cy += _ty
            _cz += _tz
            
        return (_cx, _cy, _cz)

    def set_back_color(self, red, green, blue):
        """
        set widget backcolor
        """
        self._logger.debug('Surface.set_back_color(()', self)
        self._surface_impl.set_back_color(red, green, blue)
        
    def refresh(self):
        """
        refresh surface
        """
        self._logger.debug_verbose('Surface.refresh()', self)
        
        #if self._background_is_movie == True and self._player != None:
        #    _frame = self._player.get_current_frame()
        #    _videowidth = self._player.get_video_width()
        #    _videoheight = self._player.get_video_height() 
        #    if _frame != None and _videoheight != None and _videowidth != None:
        #        self.set_background_from_buffer(_frame, _videowidth, _videoheight, True)
            
        for surface in self._surface_list:
            surface.refresh()
                    
    def add_surface(self, surface):
        self._logger.debug('Surface.add_surface(' + str(surface) + ')', self)
        if surface not in self._surface_list:
            self._surface_list.append(surface) 
        
        _mainwindow = self.get_window()
        surface._set_parent(self);
        surface._set_window(_mainwindow)
        if _mainwindow != None:
            _mainwindow._get_window_impl().add_surface(surface._get_surface_impl())
            
        #re-set location for apply location offset on child surface
        self._refresh_location()
        
        #Call AddSurface on child widget for set window, and parent
        for s in surface._get_child_surface():
            surface.add_surface(s)

    def get_surface_list(self):
        return self._surface_list
        
    def remove_surface(self, surface):
        self._logger.debug('Surface.remove_surface(' + str(surface) + ')', self)
        if surface in self._get_child_surface():
            self._surface_list.remove(surface)
            surface.on_removed()
        
        _mainwindow = self.get_window()
        if _mainwindow != None:
            _mainwindow._get_window_impl().remove_surface(surface._get_surface_impl())
                
        #remove child surface also
        #copy needeed because list in modified by recursive fct
        _child = surface._get_child_surface()[:]
        for s in _child:
            surface.remove_surface(s)
    
    def on_removed(self): pass
    
    def _get_child_surface(self):
        self._logger.debug_verbose('Surface._get_child_surface()', self)
        return self._surface_list
        
    def _set_parent(self, parent):
        self._logger.debug_verbose('Surface._set_parent()', self)
        self._parentsurface = parent
        
    def get_parent(self):
        self._logger.debug_verbose('Surface.get_parent()', self)
        return self._parentsurface
        
    def _set_window(self, window):
        self._logger.debug_verbose('Surface._set_window()', self)
        self._window = window
        
    def get_window(self):
        self._logger.debug_verbose('Surface.get_window()', self)
        return self._window
        
    def hide(self, recursive = False):
        self._logger.debug('Surface.hide()', self)
        self._surface_impl.hide()
        self._visible = False
        if recursive == True:
            self._visible_r = False
            for s in self._surface_list:
                s.hide(True)
        
    def show(self, recursive = False):
        self._logger.debug('Surface.show()', self)
        self._surface_impl.show()
        self._visible = True
        if recursive == True:
            self._visible_r = True
            for s in self._surface_list:
                s.show(True)
        
    def visible(self, recursive = False):
        self._logger.debug('Surface.visible()', self)
        if recursive == True:
            return self._visible_r
        return self._visible

    def set_name(self, name):
        self._name=name
        self._logger.debug('Surface.set_name()', self)
        
    def get_name(self):
        self._logger.debug('Surface.get_name()', self)
        return self._name
        
    def __repr__(self):
        #FIXME str(self) make recursive call
        return self._name #+ str(self)
