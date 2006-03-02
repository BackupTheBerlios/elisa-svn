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
        
        self._surface_items = []
        self.set_alpha_level(0)
        self._current_rank = 0
        self._items_surface = surface.Surface('group items surface')
        self._items_surface.set_alpha_level(0)
        self._items_surface.set_location(0,0,0.01)
        self.add_surface(self._items_surface)
        
        #self._left_arrow_surface = surface.Surface('treelevel left arrow')
        #self._left_arrow_surface.set_back_color(255,255,255)
        #self._left_arrow_surface.set_location(-20, 0, 2.3)
        #self._left_arrow_surface.set_size(20,100)
        #self._left_arrow_surface.set_background_from_file("elisa/skins/default_skin/default_pictures/leftarrow.png")
        #self.add_surface(self._left_arrow_surface)
        
        #self._right_arrow_surface = surface.Surface('treelevel right arrow')
        #self._right_arrow_surface.set_back_color(255,255,255)
        #self._right_arrow_surface.set_location(600, 0, 2.3)
        #self._right_arrow_surface.set_size(20,100)
        #self._right_arrow_surface.set_background_from_file("elisa/skins/default_skin/default_pictures/rightarrow.png")
        #self.add_surface(self._right_arrow_surface)
        
        self._font = None
        self._font = fontsurface.FontSurface('treelevel font')
        self._font.set_font_size(36)
        self._font.hide()
        self._items_surface.    add_surface(self._font)
        
        self._move_items_offset = 0
        self._fist_item = 0
        
        _i = 10
        for item in self._menuitem_list:
            s = treeitem.TreeItem(item, self._font)
            s.set_size(128, 128)
            s.set_location(_i, -12, 2.2)
            _i += 150
            s.set_background_from_file(item.get_picture_path())
            self._items_surface.add_surface(s)
            self._surface_items.append(s)
            self._current_rank = 0

        current_itemsurface = self._surface_items[self._current_rank]
        current_itemdata = current_itemsurface.get_menuitem_data()
        current_itemsurface.set_status(1)
        #current_itemdata.call_selected_callback()
        
        #self.update_row()
        

    def get_menuitem_list(self):
        return self._menuitem_list
       
    def get_itemsurface_from_menuitem(self, menuitem):
        """return item surface from menuitem object in current surface only
        """
        for surface_item in self._surface_items:
            if surface_item.get_menuitem_data() == menuitem:
                return surface_item
        return None
            
    def on_event(self, event):
        _parent = self.get_parent()
        if _parent != None and _parent.get_current_level_surface() == self:
            if event.get_simple_event() == events.SE_LEFT:
                self.select_previous_item()
            if event.get_simple_event() == events.SE_RIGHT:
                self.select_next_item()
            
        return surface.Surface.on_event(self, event)
    
    
    def update_row(self):
        if len(self._surface_items) > 3 and self._current_rank < len(self._surface_items)-1:
            self._right_arrow_surface.set_alpha_level(100)
        else:
            self._right_arrow_surface.set_alpha_level(0)
            
        if self._current_rank > 3:
            self._left_arrow_surface.set_alpha_level(100)
        else:
            self._left_arrow_surface.set_alpha_level(0)
            
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
           
           if self._current_rank > 3:
               self._move_items_offset -= 150
               self._fist_item += 1
           
           #self.update_row()
    
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
            
            #print "cur_rank:%s"%self._current_rank
            #print "first_items:%s"%self._fist_item
            if self._current_rank < self._fist_item:
                self._move_items_offset += 150
                self._fist_item -= 1
            
            #self.update_row()

    def refresh(self):
        _pas = 20
        
        if self._move_items_offset < 0:
            #print "off_start=%s"%self._move_items_offset
            (x, y, z) = self._items_surface.get_location()
            #print "x=%s"%x
            if self._move_items_offset + _pas > 0:
                _new_x = x + self._move_items_offset
                self._move_items_offset = 0
            else:
                _new_x = x - _pas
                self._move_items_offset += _pas
            #print "_new_x=%s"%_new_x    
            self._items_surface.set_location(_new_x, y, z)
            #print "off_end=%s"%self._move_items_offset
        elif self._move_items_offset > 0:
            #print "off_start=%s"%self._move_items_offset
            (x, y, z) = self._items_surface.get_location()
            #print "x=%s"%x
            if self._move_items_offset - _pas < 0:
                _new_x = x + self._move_items_offset
                self._move_items_offset = 0
            else:
                _new_x = x + _pas
                self._move_items_offset -= _pas
            #print "_new_x=%s"%_new_x    
            self._items_surface.set_location(_new_x, y, z)
            #print "off_end=%s"%self._move_items_offset
        
        
        surface.Surface.refresh(self)
            
    def get_selected_item(self):
        return self._surface_items[self._current_rank]
