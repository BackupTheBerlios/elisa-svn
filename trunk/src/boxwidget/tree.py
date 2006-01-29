import surface, event, treelevel

class Tree(surface.SurfaceGroup):

    def __init__(self, in_rootlevel):
        surface.SurfaceGroup.__init__(self)
        
        self._rootlevel = in_rootlevel
        self._DrawingNextLevel = False
        self._DrawingPreviousLevel = False
        self._leveltodraw = None

        self.SetAlphaLevel = 10
        self._surfaceitems = []
        _rootlevelsurface = treelevel.TreeLevel(in_rootlevel)
        self._surfaceitems.append(_rootlevelsurface)
        self._currentlevelID = 0
        self.DrawLevel(_rootlevelsurface)
        self._y_init = 0
        self.AddSurface(_rootlevelsurface)
    
    def GetCurrentLevelID(self):
        return self._currentlevelID()
        
    def OnEvent(self, in_event):
        if self.VisibleGroup() == True:
            if in_event.GetSimpleEvent() == event.SE_UP:
                self.SelectPreviousLevel()
            if in_event.GetSimpleEvent() == event.SE_DOWN:
                self.SelectNextLevel()
            if in_event.GetSimpleEvent() == event.SE_OK:
                _treeitemsurface = self.GetCurrentLevelSurface().GetSelectedItem()
                _treeitemsurface.GetMenuItemData().CallActionCallback()
            
        return surface.SurfaceGroup.OnEvent(self, in_event)
        
    def SelectPreviousLevel(self):
        _treelevelsurface = self.GetCurrentLevelSurface()
        _treeleveldata = _treelevelsurface.GetMenuLevelData()
        if self._currentlevelID > 0:
            self._currentlevelID -= 1
            _treeleveldata.CallUnselectedCallback()
            self.RemoveSurface(_treelevelsurface)
            self._surfaceitems.remove(_treelevelsurface)
            self._DrawingPreviousLevel = True
    
    def SelectNextLevel(self):
        _treeitemsurface = self.GetCurrentLevelSurface().GetSelectedItem()
        _nextleveldata = _treeitemsurface.GetMenuItemData().GetLevel()
        if _nextleveldata != None:
            _nextlevelsurface = treelevel.TreeLevel(_nextleveldata)
            self._currentlevelID += 1
            self._surfaceitems.append(_nextlevelsurface)
            self._DrawingNextLevel = True
            self._leveltodraw = _nextlevelsurface
    
    def SetLocation(self, x, y, z):
        surface.SurfaceGroup.SetLocation(self, x, y, z)
    
    def SetInitialLocation(self, x, y, z):
        self._y_init = y
        self.SetLocation(x, y, z)
           
    def Refresh(self):
        _step = 10
        if self._DrawingNextLevel == True:
            _ymin = self._y_init - 130 * self._currentlevelID
            (_x,_y,_z) = self.GetLocation()
            if _y > _ymin:
                #print str(_y) + " min:" + str(_ymin)
                _y = _y - _step
                if _y <= _ymin: _y = _ymin
                self.SetLocation(_x, _y, _z)
            else:
                self.DrawLevel(self._leveltodraw)
                self._DrawingNextLevel = False
        elif self._DrawingPreviousLevel == True:
            if self._currentlevelID > 0 : 
                _ymin = self._y_init + 130 * (self._currentlevelID -2)
            else:
                _ymin = self._y_init
                
            (_x,_y,_z) = self.GetLocation()
            #print str(_y) + " min:" + str(_ymin)
            if _y < _ymin:
                _y = _y +_step
                if _y >= _ymin: _y =  self._y_init - 130 * (self._currentlevelID)
                #print str(_y) + " min:" + str(_ymin)
                self.SetLocation(_x, _y, _z)
            else:
                self._DrawingPreviousLevel = False
        
        surface.SurfaceGroup.Refresh(self)
        
    def DrawLevel(self, in_level):
        in_level.SetLocation(0,130 * self._currentlevelID, 3)
        in_level.SetSize(300, 40)
        self.AddSurface(in_level)
        in_level.GetMenuLevelData().CallSelectedCallback()
            
    def GetCurrentLevelSurface(self):
        return self._surfaceitems[self._currentlevelID]
