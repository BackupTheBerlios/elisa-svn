import surface, treeitem, event, surface, fontsurface

class TreeLevel(surface.Surface):

    def __init__(self, in_menulevel):
        surface.Surface.__init__(self)
            
        self._menuleveldata = in_menulevel
        
        #list composed of sublist [item,surface]
        #rank are the same as visual rank
        self._surfaceitems = []
        self.SetAlphaLevel(0)
        self._currentrank = 0
        self._BackImage = surface.Surface()
        self._BackImage.SetBackgroundFromFile("testGL/themes/mce/COMMON.BUTTON.LEFT.FOCUS.PNG")
        self._BackImage.SetSize(550,40)
        self._BackImage.SetLocation(20,30,2.1)
        self.AddSurface(self._BackImage)
        self._font = None
        if self._menuleveldata.ItemLabelVisible():
            self._font = fontsurface.FontSurface()
            self._font.SetFontSize(36)
            self._font.Hide()
            self.AddSurface(self._font)
        
        _i = 10
        for item in self._menuleveldata.GetItemList():
            s = treeitem.TreeItem(item, self._font)
            s.SetSize(128, 128)
            s.SetLocation(_i, -12, 2.2)
            _i += 150
            s.SetBackgroundFromFile(item.GetPicturePathAndFilename())
            self.AddSurface(s)
            self._surfaceitems.append(s)
            self._currentrank = 0

        current_itemsurface = self._surfaceitems[self._currentrank]
        current_itemdata = current_itemsurface.GetMenuItemData()
        current_itemsurface.SetStatus(1)
        current_itemdata.CallSelectedCallback()
        

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
           itemsurface = self._surfaceitems[self._currentrank]
           itemdata = itemsurface.GetMenuItemData()
           itemsurface.SetStatus(0)
           itemdata.CallUnselectedCallback()
           
           self._currentrank += 1
           itemsurface = self._surfaceitems[self._currentrank]
           itemdata = itemsurface.GetMenuItemData()
           itemsurface.SetStatus(1)
           itemdata.CallSelectedCallback()
    
    def SelectPreviousItem(self):
        if self._currentrank > 0:
            itemsurface = self._surfaceitems[self._currentrank]
            itemdata = itemsurface.GetMenuItemData()
            itemsurface.SetStatus(0)
            itemdata.CallUnselectedCallback()
           
            self._currentrank -= 1
            itemsurface = self._surfaceitems[self._currentrank]
            itemdata = itemsurface.GetMenuItemData()
            itemsurface.SetStatus(1)
            itemdata.CallSelectedCallback()

    def GetSelectedItem(self):
        return self._surfaceitems[self._currentrank]
