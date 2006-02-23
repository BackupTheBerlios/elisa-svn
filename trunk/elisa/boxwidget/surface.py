from bindings import testgl_impl

class Surface(object):
   
    """
    class of Surface
    """
    
    def __init__(self):
        self._surface_impl = testgl_impl._testGL_Surface_Impl()
        self._surfacelist = []
        self._parentsurface = None
        self._x = 0
        self._y = 0
        self._z = 0
        self._width = 100
        self._height = 100
        self._alphalevel = 0
        self._background_image_path = None
        self._window = None
        self._visible = True
        
        self._surface_impl.set_size(self._width, self._height)

    def _get_surface_impl(self):
        return self._surface_impl

    def get_rect(self):
        """
        return surface rectangle
        """
        
    def set_alpha_level(self, level):
        """
        set the alpha level in percent of the widget [0 to 100%] of opacity
        """
        self._alphalevel = level
        self._surface_impl.set_alpha_level(level)

    def set_background_from_file(self, path_and_file_name=None):
        """
        set widget background image
        """
        self._background_image_path = path_and_file_name
        self._surface_impl.set_background_from_file(path_and_file_name)
        
    def get_background_file(self):
        """
        return path and filename of background image
        """
        return self._background_image_path
        
    def set_size(self, width, height):
        """
        define the size in 2D plan
        """
        self._width = width
        self._height = height
        self._surface_impl.set_size(width, height)
    
    def get_size(self):
        """
        return current size
        """
        return (self._width, self._height)

    def set_location(self, x, y, z):
        """
        set location of widget (relative to parent)
        """
        self._x = x
        self._y = y
        self._z = z
        (ax, ay, az) = self.get_absolute_location()
        self._surface_impl.set_location(ax, ay, az)
        
        for child in self._surfacelist: child._refresh_location()
    
    def _refresh_location(self):
        self.set_location(self._x, self._y, self._z)
    
    def get_location(self):
        """ 
        get 3D location (relative to parent)
        """ 
        return (self._x, self._y, self._z)
    
    def get_absolute_location(self):
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
        self._surface_impl.set_back_color(red, green, blue)
        
    def refresh(self):
        """
        refresh surface
        """
        for surface in self._surfacelist:
            surface.refresh()
                    
    def add_surface(self, surface):
        if surface not in self._surfacelist:
            self._surfacelist.append(surface)  
            self.get_window()._get_window_impl().add_surface(surface._get_surface_impl())
            surface._set_parent(self);
            surface._set_window(self.get_window())
        
        #re-set location for apply location offset on child surface
        self._refresh_location()
        
        #Call AddSurface on child widget
        for s in surface._get_child_surface():
            surface.add_surface(s)

    def remove_surface(self, surface):
        if surface in self._surfacelist:
            self._surfacelist.remove(surface)
        
        
        _mainwindow = self.get_window()
        if _mainwindow != None:
            _mainwindow._get_window_impl().remove_surface(surface._get_surface_impl())
                
        #remove child surface also
        #copy needeed because list in modified by recursive fct
        _child = self._surfacelist[:]
        for s in _child:
            surface.remove_surface(s)
    
    def _get_child_surface(self):
        return self._surfacelist
        
    def _set_parent(self, parent):
        self._parentsurface = parent
        
    def get_parent(self):
        return self._parentsurface

    def on_event(self, event):
        """
        called if new event is fire
        if return False, event will not fired to next event
        """
        return True
        
    def _set_window(self, window):
        self._window = window
        
    def get_window(self):
        return self._window
        
    def hide(self):
        self._visible = False
        
    def show(self):
        self._visible = True
        
    def visible(self):
        return self._visible
