import surface

class TreeItem(surface.Surface): 

    def __init__(self, in_menuitemdata):
        surface.Surface.__init__(self)
        self._menuitemdata = in_menuitemdata
        self._arrowsurface = surface.Surface()
        self._arrowsurface.SetBackColor(255,255,255)
        self._arrowsurface.SetLocation(14,128,2.3)
        self._arrowsurface.SetSize(100,20)
        self._arrowsurface.SetBackgroundFromFile("icons/downarrow.png")
        self.AddSurface(self._arrowsurface)
        self.SetStatus(0)

    def ShowArrow(self):
        self._arrowsurface.SetAlphaLevel(100)
    
    def HideArrow(self):
        self._arrowsurface.SetAlphaLevel(0)
            
    def GetMenuItemData(self):
        return self._menuitemdata
        
    def SetStatus(self, in_status):
        self._status = in_status
        
        if in_status == 0:
            self.SetAlphaLevel(35)
            self.HideArrow()
        else:
            self.SetAlphaLevel(100)
            if self._menuitemdata.GetLevel() != None: self.ShowArrow()
