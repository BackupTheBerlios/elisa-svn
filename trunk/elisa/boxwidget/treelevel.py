from elisa.boxwidget import surface, treeitem, events, surface, fontsurface

class TreeLevel(surface.Surface):

    def __init__(self, menuitem_list, name="TreeLevel"):
        surface.Surface.__init__(self, name)
            
        self._menuitem_list = menuitem_list
        
        #list composed of sublist [item,surface]
        #rank are the same as visual rank
        self._surface_items = []
        self.set_alpha_level(0)
        self._current_rank = 0
        self._back_image = surface.Surface('treelevel backimage')
        self._back_image.set_background_from_file("extern/testGL/themes/mce/COMMON.BUTTON.LEFT.FOCUS.PNG")
        self._back_image.set_size(550,40)
        self._back_image.set_location(20,30,2.1)
        self.add_surface(self._back_image)
        self._font = None
        self._font = fontsurface.FontSurface('treelevel font')
        self._font.set_font_size(36)
        self._font.hide()
        self.add_surface(self._font)
        
        _i = 10
        for item in self._menuitem_list:
            s = treeitem.TreeItem(item, self._font)
            s.set_size(128, 128)
            s.set_location(_i, -12, 2.2)
            _i += 150
            s.set_background_from_file(item.get_picture_path())
            if item.get_items == []:
                s.hide_down_arrow()
            self.add_surface(s)
            self._surface_items.append(s)
            self._current_rank = 0

        current_itemsurface = self._surface_items[self._current_rank]
        current_itemdata = current_itemsurface.get_menuitem_data()
        current_itemsurface.set_status(1)
        #current_itemdata.call_selected_callback()
        

    def get_menuitem_list(self):
        return self._menuitem_list
        
    def on_event(self, event):
        _parent = self.get_parent()
        if _parent != None and _parent.get_current_level_surface() == self:
            if event.get_simple_event() == events.SE_LEFT:
                self.select_previous_item()
            if event.get_simple_event() == events.SE_RIGHT:
                self.select_next_item()
            
        return surface.Surface.on_event(self, event)
        
    def select_next_item(self):
        if self._current_rank < len(self._surface_items) - 1:
           itemsurface = self._surface_items[self._current_rank]
           itemsurface.set_status(0)
           #itemdata = itemsurface.get_menu_item_data()
           #itemdata.call_unselected_callback()
           
           self._current_rank += 1
           itemsurface = self._surface_items[self._current_rank]
           itemsurface.set_status(1)
           #itemdata = itemsurface.get_menu_item_data()
           #itemdata.call_selected_callback()
    
    def select_previous_item(self):
        if self._current_rank > 0:
            itemsurface = self._surface_items[self._current_rank]
            itemsurface.set_status(0)
            #itemdata = itemsurface.get_menu_item_data()
            #itemdata.call_unselected_callback()
           
            self._current_rank -= 1
            itemsurface = self._surface_items[self._current_rank]
            itemsurface.set_status(1)
            #itemdata = itemsurface.get_menu_item_data()
            #itemdata.call_selected_callback()

    def get_selected_item(self):
        return self._surface_items[self._current_rank]
