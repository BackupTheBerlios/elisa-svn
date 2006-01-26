import surface

class TreeItem(surface.Surface): 

    def __init__(self, in_menuitemdata):
        surface.Surface.__init__(self)
        self.SetStatus(0)
        self._menuitemdata = in_menuitemdata
        
    def GetMenuItemData(self):
        return self._menuitemdata
        
    def SetStatus(self, in_status):
        self._status = in_status
        
        if in_status == 0:
            self.SetAlphaLevel(50)
        else:
            self.SetAlphaLevel(100)
