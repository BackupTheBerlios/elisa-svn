import surface, event, treelevel

class Tree(surface.Surface):

    def __init__(self, in_rootlevel):
        surface.Surface.__init__(self)
        
        self._rootlevel = in_rootlevel
        self.Hide()
        
        self.SetAlphaLevel = 10
        self._surfaceitems = []
        _rootlevelsurface = treelevel.TreeLevel(in_rootlevel)
        self._surfaceitems.append(_rootlevelsurface)
        self._currentlevelID = 0
        self.DrawLevel(_rootlevelsurface)
        
        self.AddSurface(_rootlevelsurface)

    def GetCurrentLevelID(self):
        return self._currentlevelID()
        
    def OnEvent(self, in_event):
        if in_event.GetSimpleEvent() == event.SE_UP:
            self.SelectPreviousLevel()
        if in_event.GetSimpleEvent() == event.SE_DOWN:
            self.SelectNextLevel()
            
        return surface.Surface.OnEvent(self, in_event)
        
    def SelectPreviousLevel(self):
        _treeitemsurface = self.GetCurrentLevelSurface()
        if self._currentlevelID > 0:
            self._currentlevelID -= 1
            self.RemoveSurface(_treeitemsurface)
            self._surfaceitems.remove(_treeitemsurface)
    
    def SelectNextLevel(self):
        _treeitemsurface = self.GetCurrentLevelSurface().GetSelectedItem()
        _nextleveldata = _treeitemsurface.GetMenuItemData().GetLevel()
        if _nextleveldata != None:
            _nextlevelsurface = treelevel.TreeLevel(_nextleveldata)
            self._currentlevelID += 1
            self._surfaceitems.append(_nextlevelsurface)
            self.DrawLevel(_nextlevelsurface)
            

    def DrawLevel(self, in_level):
        in_level.SetLocation(0,130 * self._currentlevelID, 3)
        in_level.SetSize(300, 40)
        self.AddSurface(in_level)
            
    def GetCurrentLevelSurface(self):
        return self._surfaceitems[self._currentlevelID]
