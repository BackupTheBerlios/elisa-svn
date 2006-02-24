from elisa.boxwidget import surface, treeitem, events, surface, fontsurface

class TreeLevel(surface.Surface):

    def __init__(self, menu_level_data):
        surface.Surface.__init__(self)
            
        self._menu_level_data = menu_level_data
        
        #list composed of sublist [item,surface]
        #rank are the same as visual rank
        self._surface_items = []
        self.set_alpha_level(0)
        self._current_rank = 0
        self._back_image = surface.Surface()
        self._back_image.set_background_from_file("extern/testGL/themes/mce/COMMON.BUTTON.LEFT.FOCUS.PNG")
        self._back_image.set_size(550,40)
        self._back_image.set_location(20,30,2.1)
        self.add_surface(self._back_image)
        self._font = None
        if self._menu_level_data.item_label_visible():
            self._font = fontsurface.font_surface()
            self._font.set_font_size(36)
            self._font.hide()
            self.add_surface(self._font)
        
        _i = 10
        for item in self._menu_level_data.get_item_list():
            s = treeitem.TreeItem(item, self._font)
            s.set_size(128, 128)
            s.set_location(_i, -12, 2.2)
            _i += 150
            s.set_background_from_file(item.get_picture_path_and_filename())
            self.add_surface(s)
            self._surface_items.append(s)
            self._current_rank = 0

        current_itemsurface = self._surface_items[self._current_rank]
        current_itemdata = current_itemsurface.get_menu_item_data()
        current_itemsurface.set_status(1)
        current_itemdata.call_selected_callback()
        

    def get_menu_level_data(self):
        return self._menu_level_data
        
    def on_event(self, event):
        _parent = self.get_parent()
        if _parent != None and _parent.get_current_level_surface() == self:
            if event.get_simple_event() == events.SE_LEFT:
                self.select_previous_item()
            if event.get_simple_event() == events.SE_RIGHT:
                self.select_next_item()
            
        return surface.Surface.on_event(self, in_event)
        
    def select_next_item(self):
        if self._current_rank < len(self._surface_items) - 1:
           itemsurface = self._surface_items[self._current_rank]
           itemdata = itemsurface.get_menu_item_data()
           itemsurface.set_status(0)
           itemdata.call_unselected_callback()
           
           self._current_rank += 1
           itemsurface = self._surface_items[self._current_rank]
           itemdata = itemsurface.get_menu_item_data()
           itemsurface.set_status(1)
           itemdata.call_selected_callback()
    
    def select_previous_item(self):
        if self._current_rank > 0:
            itemsurface = self._surface_items[self._current_rank]
            itemdata = itemsurface.get_menu_item_data()
            itemsurface.set_status(0)
            itemdata.call_unselected_callback()
           
            self._current_rank -= 1
            itemsurface = self._surface_items[self._current_rank]
            itemdata = itemsurface.get_menu_item_fata()
            itemsurface.set_status(1)
            itemdata.call_selected_callback()

    def get_selected_item(self):
        return self._surface_items[self._current_rank]
