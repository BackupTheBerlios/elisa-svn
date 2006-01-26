import surface, treeitem, event

class TreeLevel(surface.Surface):

    def __init__(self, in_menulevel):
        surface.Surface.__init__(self)
        
        self.SetBackgroundImage("testGL/themes/mce/COMMON.BUTTON.LEFT.FOCUS.PNG")
            
        self._menuleveldata = in_menulevel
        
        #list composed of sublist [item,surface]
        #rank are the same as visual rank
        self._surfaceitems = []
        self._currentrank = 0
        
        _i = 10
        for item in in_menulevel.GetItemList():
            s = treeitem.TreeItem(item)
            s.SetSize(64, 64)
            s.SetLocation(_i, -12, 2.1)
            _i += 70
            s.SetBackgroundImage(item.GetPicturePathAndFilename())
            self.AddSurface(s)
            self._surfaceitems.append(s)
            self._currentrank = 0

        self._surfaceitems[self._currentrank].SetStatus(1)

    def GetMenuLevelData(self):
        return self._menuleveldata
        
    def OnEvent(self, in_event):
        _parent = self.GetParent()
        if _parent != None and _parent.GetCurrentLevelSurface() == self:
            if in_event.GetSimpleEvent() == event.SE_LEFT:
                self.SelectPreviousItem()
            if in_event.GetSimpleEvent() == event.SE_RIGHT:
                self.SelectNextItem()
            
        return surface.Surface.OnEvent(self, in_event)
        
    def SelectNextItem(self):
        if self._currentrank < len(self._surfaceitems) - 1:
           self._surfaceitems[self._currentrank].SetStatus(0)
           self._currentrank += 1
           self._surfaceitems[self._currentrank].SetStatus(1)
    
    def SelectPreviousItem(self):
        if self._currentrank > 0:
           self._surfaceitems[self._currentrank].SetStatus(0)
           self._currentrank -= 1
           self._surfaceitems[self._currentrank].SetStatus(1)

    def GetSelectedItem(self):
        return self._surfaceitems[self._currentrank]
