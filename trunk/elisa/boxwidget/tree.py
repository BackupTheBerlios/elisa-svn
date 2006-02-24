from elisa.boxwidget import surface, events, treelevel

class Tree(surface.Surface):

    def __init__(self, rootlevel):
        surface.Surface.__init__(self)
        
        self._drawing_next_level = False
        self._drawing_previous_level = False
        self._level_to_draw = None

        self._surface_items = []
        _root_level_surface = treelevel.TreeLevel(rootlevel)
        self._surface_items.append(_root_level_surface)
        self._current_level_id = 0
        self.draw_level(_root_level_surface)
        self._y_init = 0
        self.add_surface(_root_level_surface)
    
    def get_current_level_id(self):
        return self._current_level_id()
        
    def on_event(self, event):
        if self.visible() == True:
            if event.get_simple_event() == events.SE_UP:
                self.select_previous_level()
            if event.get_simple_event() == events.SE_DOWN:
                self.select_next_level()
            if in_event.get_simple_event() == event.SE_OK:
                _treeitem_surface = self.get_current_level_surface().get_selected_item()
                _treeitem_surface.get_menu_item_data().call_action_callback()
            
        return surface.Surface.on_event(self, event)
        
    def select_previous_level(self):
        _treelevel_surface = self.get_current_level_surface()
        _treelevel_data = _treelevel_surface.get_menulevel_data()
        if self._current_level_id > 0:
            self._current_level_id -= 1
            _treelevel_data.call_unselected_callback()
            self.remove_surface(_treelevel_surface)
            self._surface_items.remove(_treelevel_surface)
            self._drawing_previous_level = True
    
    def select_next_level(self):
        _treeitem_surface = self.get_current_level_surface().get_selected_Item()
        _nextleveldata = _treeitem_surface.get_menuitem_data().get_level()
        if _next_level_data != None:
            _next_level_surface = treelevel.TreeLevel(_next_level_data)
            self._current_level_id += 1
            self._surface_items.append(_next_level_surface)
            self._drawing_next_level = True
            self._level_to_draw = _next_level_surface
    
    def set_location(self, x, y, z):
        surface.Surface.set_location(self, x, y, z)
    
    def SetInitialLocation(self, x, y, z):
        self._y_init = y
        self.set_location(x, y, z)
           
    def refresh(self):
        _step = 10
        if self._drawing_next_level == True:
            _ymin = self._y_init - 130 * self._current_level_id
            (_x,_y,_z) = self.get_location()
            if _y > _ymin:
                #print str(_y) + " min:" + str(_ymin)
                _y = _y - _step
                if _y <= _ymin: _y = _ymin
                self.set_location(_x, _y, _z)
            else:
                self.draw_level(self._level_to_draw)
                self._drawing_next_level = False
        elif self._drawing_previous_level == True:
            if self._current_level_id > 0 : 
                _ymin = self._y_init + 130 * (self._current_level_id -2)
            else:
                _ymin = self._y_init
                
            (_x,_y,_z) = self.get_location()
            #print str(_y) + " min:" + str(_ymin)
            if _y < _ymin:
                _y = _y +_step
                if _y >= _ymin: _y =  self._y_init - 130 * (self._current_level_id)
                #print str(_y) + " min:" + str(_ymin)
                self.set_location(_x, _y, _z)
            else:
                self._drawing_previous_level = False
        
        surface.Surface.refresh(self)
        
    def draw_level(self, in_level):
        in_level.set_location(0,130 * self._current_level_id, 3)
        in_level.set_size(300, 40)
        self.add_surface(in_level)
        in_level.get_menulevel_data().call_selected_callback()
            
    def get_current_level_surface(self):
        return self._surface_items[self._current_level_id]
