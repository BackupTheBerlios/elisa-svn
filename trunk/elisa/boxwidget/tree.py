from elisa.boxwidget import surface, events, treelevel
from elisa.framework import message_bus, common

class Tree(surface.Surface):

    def __init__(self, menutree_root, name):
        surface.Surface.__init__(self, name)

        self._appli = common.get_application()
        self._drawing_next_level = False
        self._drawing_previous_level = False
        self._level_to_draw = None
        self.hide()
        
        self._treelevel_surface_list = []
        _root_treelevel_surface = treelevel.TreeLevel(menutree_root.get_items(), "treelevel rank 0")
        self._treelevel_surface_list.append(_root_treelevel_surface)
        self._current_level_id = 0
        self.draw_level(_root_treelevel_surface)
        self._y_init = 0
        self.add_surface(_root_treelevel_surface)
    
    def get_current_level_id(self):
        return self._current_level_id()
        
    def on_message(self, receiver, message, sender):
        self._logger.debug('Tree.on_event(' + str(message) + ')', self)
        if self.visible(True) and not self._drawing_next_level and not self._drawing_previous_level :
            selected_treeitem_surface = self.get_current_level_surface().get_selected_item()
            selected_treeitem_data = selected_treeitem_surface.get_menuitem_data()
            
            if isinstance(message, events.InputEvent):
                if message.get_simple_event() == events.SE_UP:
                    self.select_previous_level()
                if message.get_simple_event() == events.SE_DOWN:
                    self.select_next_level()
                if message.get_simple_event() == events.SE_OK:
                    selected_treeitem_data.fire_action(selected_treeitem_surface)
##             elif isinstance(message, message_bus.ActionMessage):
##                 if sender == _selected_treeitem_data:
##                     if message.get_action() == 'SHOW_PICTURE':
##                         self._appli.set_background_from_surface(_selected_treeitem_surface)
##                     if message.get_action() == 'SHOW_MOVIE': pass
##                         #
##                         #self._appli.set_background_from_surface(_selected_treeitem_surface)
                                    
                    
        return surface.Surface.on_message(self, receiver, message, sender)
        
    def select_previous_level(self):
        self._logger.debug('Tree.select_previous_level()', self)
        current_treelevel_surface = self.get_current_level_surface()
        selected_menuitem_surface = current_treelevel_surface.get_selected_item()
        selected_menuitem_data = selected_menuitem_surface.get_menuitem_data()
        
        if self._current_level_id > 0:
            self._current_level_id -= 1
            selected_menuitem_data.fire_unselected()
            self.remove_surface(current_treelevel_surface)
            self._treelevel_surface_list.remove(current_treelevel_surface)
            self._drawing_previous_level = True
    
    def select_next_level(self):
        self._logger.debug('Tree.select_next_level()', self)
        treeitem_surface = self.get_current_level_surface().get_selected_item()
        next_level_data = treeitem_surface.get_menuitem_data().get_items()
        if next_level_data != []:
            self._current_level_id += 1
            name = "treelevel rank " + str(self._current_level_id)
            next_level_surface = treelevel.TreeLevel(next_level_data, name)
            self._treelevel_surface_list.append(next_level_surface)
            self._drawing_next_level = True
            self._level_to_draw = next_level_surface
            
    def set_location(self, x, y, z):
        surface.Surface.set_location(self, x, y, z)
    
    def set_initial_location(self, x, y, z):
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
            
    def get_current_level_surface(self):
        return self._treelevel_surface_list[self._current_level_id]
