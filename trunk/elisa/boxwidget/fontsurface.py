from elisa.boxwidget.bindings import testgl_impl

from elisa.framework.log import Logger

class FontSurface(object):
    """
    font class
    """
    
    """
    class of Surface
    """
    
    def __init__(self, name='Surface'):
        self._logger = Logger()
        self._name=name
        self._logger.debug('Font.__init__()', self)
        self._font_impl = testgl_impl._testGL_Font_Impl()
        self._parentsurface = None
        self._x = 0
        self._y = 0
        self._z = 0
        self._width = 100
        self._height = 100
        self._alphalevel = 0
        self._window = None
        self._visible = True
        
        self._font_impl.set_size(self._width, self._height)

       
    def _get_child_surface(self):
        return []
            
    def fire_event(self, event): 
        #self._logger.debug('Font.fire_event()', self)
        return self.on_event(event)
    
    def on_event(self, event):
        """
        called if new event is fire
        if return False, event will not fired to next event
        """
        self._logger.debug('Font.on_event(' + str(event) + ')', self)
        return True
            
    def _get_surface_impl(self):
        self._logger.debug('Font._get_surface_impl()', self)
        return self._font_impl

    def set_alpha_level(self, level):
        """
        set the alpha level in percent of the widget [0 to 100%] of opacity
        """
        self._logger.debug('Font.set_alpha_level()', self)
        self._alphalevel = level
        self._font_impl.set_alpha_level(level)

    def set_size(self, width, height):
        """
        define the size in 2D plan
        """
        self._logger.debug('Font.set_size()', self)
        self._width = width
        self._height = height
        self._font_impl.set_size(width, height)
    
    def get_size(self):
        """
        return current size
        """
        self._logger.debug('Font.get_size()', self)
        return (self._width, self._height)

    def set_location(self, x, y, z):
        """
        set location of widget (relative to parent)
        """
        self._logger.debug('Font.set_location()', self)
        self._x = x
        self._y = y
        self._z = z
        (ax, ay, az) = self.get_absolute_location()
        self._font_impl.set_location(ax, ay, az)
        
        for child in self._surface_list: child._refresh_location()
    
    def _refresh_location(self):
        self._logger.debug('Font._refresh_location()', self)
        self.set_location(self._x, self._y, self._z)
    
    def get_location(self):
        """ 
        get 3D location (relative to parent)
        """ 
        self._logger.debug('Font.get_location()', self)
        return (self._x, self._y, self._z)
    
    def get_absolute_location(self):
        self._logger.debug('Font.get_absolute_location()', self)
        _cx = self._x
        _cy = self._y
        _cz = self._z
                
        if self._parentsurface != None and isinstance(self._parentsurface, Surface) :
            (_tx, _ty, _tz) = self._parentsurface.get_absolute_location()
            _cx += _tx
            _cy += _ty
            _cz += _tz
            
        return (_cx, _cy, _cz)
        
    def refresh(self):
        """
        refresh surface
        """
        #self._logger.debug('Font.refresh()', self)

    def _set_parent(self, parent):
        self._logger.debug('Font._set_parent()', self)
        self._parentsurface = parent
        
    def get_parent(self):
        self._logger.debug('Font.get_parent()', self)
        return self._parentsurface
        
    def _set_window(self, window):
        self._logger.debug('Font._set_window()', self)
        self._window = window
        
    def get_window(self):
        self._logger.debug('Font.get_window()', self)
        return self._window
        
    def hide(self):
        self._logger.debug('Font.hide()', self)
        self._font_impl.hide()
        self._visible = False
        
    def show(self):
        self._logger.debug('Font.show()', self)
        self._font_impl.show()
        self._visible = True
        
    def visible(self):
        self._logger.debug('Font.visible()', self)
        return self._visible

    def set_name(self, name):
        self._name=name
        self._logger.debug('Font.set_name()', self)
        
    def get_name(self):
        self._logger.debug('Font.get_name()', self)
        return self._name
        
    def set_font_size(self, size):
        self._font_impl.SetFontSize(size)
        
    def set_text(self, text):
        self._font_impl.SetText(text)
        
    def __repr__(self):
        #FIXME str(self) make recursive call
        return self._name #+ str(self)
