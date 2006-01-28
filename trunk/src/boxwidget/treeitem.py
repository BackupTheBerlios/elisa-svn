import surface

class TreeItem(surface.Surface): 

    def __init__(self, in_menuitemdata, in_font = None):
        surface.Surface.__init__(self)
        self._menuitemdata = in_menuitemdata
        self._arrowsurface = surface.Surface()
        self._arrowsurface.SetBackColor(255,255,255)
        self._arrowsurface.SetLocation(14,128,2.3)
        self._arrowsurface.SetSize(100,20)
        self._arrowsurface.SetBackgroundFromFile("icons/downarrow.png")
        self.AddSurface(self._arrowsurface)
        self._font = in_font
        self.SetStatus(0)

    def ShowLabel(self):
        if self._font != None and self.Visible()==True:
            self._font.Show()
            (_x,_y,_z) = self.GetLocation()
            self._font.SetText(self._menuitemdata.GetShortname())
            (_xf,_yf,_zf) = self._font.GetSize()
            self._font.SetLocation(_x + 64 - _xf/2 , _y + 88, 2.4)
            
    def HideLabel(self):
        if self._font != None: self._font.Hide()

    def ShowDownArrow(self):
        self._arrowsurface.SetAlphaLevel(100)
    
    def HideDownArrow(self):
        self._arrowsurface.SetAlphaLevel(0)
            
    def GetMenuItemData(self):
        return self._menuitemdata
        
    def SetStatus(self, in_status):
        self._status = in_status
        
        if in_status == 0:
            self.SetAlphaLevel(35)
            self.HideDownArrow()
            self.HideLabel()
        else:
            self.SetAlphaLevel(100)
            if self._menuitemdata.GetLevel() != None: self.ShowDownArrow()
            self.ShowLabel()
