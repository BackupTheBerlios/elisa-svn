class _SurfaceBase(object):
   
    """
    Base class of Surface
    """
    
    def __init__(self):
        self._surfacelist = []
        self._parentsurface = None
        self._x = 0
        self._y = 0
        self._z = 0
        self._alphalevel = 0
        self._backgroundimagepath = None
        self._window = None
        self._visible = True

    def GetRect(self):
        """
        return surface rectangle
        """
        
    def SetAlphaLevel(self, in_level):
        """
        set the alpha level in percent of the widget [0 to 100%] of opacity
        """
        self._alphalevel = in_level

    def SetBackgroundFromFile(self, in_pathandfilename=None):
        """
        set widget background image
        """
        self._backgroundimagepath = in_pathandfilename
        
    def GetBackgroundFile(self):
        """
        return path and filename of background image
        """
        
    def SetSize(self, Width, Height):
        """
        define the size in 2D plan
        """
    
    def GetSize(self):
        """
        return current size
        """

    def SetLocation(self, x, y, z):
        """
        set location of widget (relative to parent)
        """
        self._x = x
        self._y = y
        self._z = z
        
        for in_child in self._surfacelist: in_child._RefreshLocation()
    
    def _RefreshLocation(self):
        self.SetLocation(self._x, self._y, self._z)
    
    def GetLocation(self):
        """ 
        get 3D location (relative to parent)
        """ 
        return (self._x, self._y, self._z)
    
    def GetAbsoluteLocation(self):
        _cx = self._x
        _cy = self._y
        _cz = self._z
        
        #print "self>" + str(self) + " / " + str(self.GetLocation())
        
        _parent = self.GetParent()
        if _parent != None:
            #print "IN parent>" + str(_parent) + " / " + str(_parent.GetAbsoluteLocation())
            (_tx, _ty, _tz) = _parent.GetAbsoluteLocation()
            _cx += _tx
            _cy += _ty
            _cz += _tz
            
        return (_cx, _cy, _cz)
        
    def Draw(self):
        """
        draw widget
        """
    
    def SetBackColor(self, Red, Green, Blue):
        """
        set widget backcolor
        """
        
    def Refresh(self):
        """
        refresh surface
        @return: True if no error, False if error.
        """
        for in_surface in self._surfacelist:
            in_surface.Refresh()
            
        return True

    def GetNativeSurface(self):
        """
        return native surface object (from binded engine)
        @return: object
        """
        return self._NativeSurface
        
    def SetNaviteSurface(self, in_nativesurface):
        """
        set native surface object (from binded engine)
        """
        self._NativeSurface =  in_nativesurface
        
    def AddSurface(self, in_surface):
        if in_surface not in self._surfacelist:
            self._surfacelist.append(in_surface)
            
        in_surface._SetParent(self)  
        _mainwindow = self.GetWindow()
        #if new surface is added to another surface visible (added to main form)
        #I fire OnAddSurface event
        if _mainwindow != None:
            _mainwindow.AddSurfaceToNativeWindow(in_surface)
            in_surface._SetWindow(self.GetWindow())
        
        #re-set location for apply location offset on child surface
        self.SetLocation(self._x, self._y, self._z)
        
        #Call AddSurface on child widget
        for s in in_surface._GetChildSurface():
            in_surface.AddSurface(s)

    def RemoveSurface(self, in_surface):
        if in_surface in self._surfacelist:
            self._surfacelist.remove(in_surface)
        
        _mainwindow = self.GetWindow()
        if _mainwindow != None:
            _mainwindow.RemoveSurfaceFromNativeWindow(in_surface)
                
        #remove child surface also
        #copy needeed because list in modified by recursive fct
        _child = in_surface._GetChildSurface()[:]
        for s in _child:
            in_surface.RemoveSurface(s)
    
    def _GetChildSurface(self):
        return self._surfacelist
        
    def _SetParent(self, in_parent):
        self._parentsurface = in_parent
        
    def GetParent(self):
        return self._parentsurface

    def OnEvent(self, in_event):
        """
        called if new event is fire
        if return False, event will not fired to next event
        """
        return True
        
    def _SetWindow(self, in_window):
        self._window = in_window
        
    def GetWindow(self):
        return self._window
        
    def Hide(self):
        self._visible = False
        
    def Show(self):
        self._visible = True
        
    def Visible(self):
        return self._visible
