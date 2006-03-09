from elisa.boxwidget import surface, fontsurface, events

class MCEButtonMenu(surface.Surface):

    def __init__(self, root_menuitem_list, name="mce menu button"):
        surface.Surface.__init__(self, name)
        self._root_menuitem_list = root_menuitem_list
        self._current_level_id = 0
        self._level_count = 0
        self._drawing_next_level = False
        self._drawing_previous_level = False
        self._animate_hide_in_progress = False
        self._animate_show_in_progress = False
        
        self.set_size(0.0, 0.0)
        self.set_location(300.0, 250, 0.1)
        
        self._font_group = surface.Surface()
        self._font_group.set_size(0.0, 0.0)
        self.add_surface(self._font_group)
        
        self._button = surface.Surface()
        self._button.set_background_from_file("extern/testGL/themes/mce/COMMON.BUTTON.LEFT.FOCUS.PNG")
        self._button.set_size(250,36)
        self._button.set_location(0.0, 0.0, 0.2)
        self._button.set_back_color(255, 255, 255)
        self.add_surface(self._button)
        
        _y = 0
        for menuitem in self._root_menuitem_list:
            _ft = fontsurface.FontSurface(menuitem.get_short_name())
            _ft.set_text(menuitem.get_short_name())
            _ft.set_font_size(34)
            (_sh, _sw, _sd) = _ft.get_size()
            _ft.set_location(240.0 - _sh, _y, 0.3)
            _y += 50
            self._font_group.add_surface(_ft)
            self._level_count += 1
            
    def on_message(self, receiver, message, sender):
        self._logger.debug('Tree.on_event(' + str(message) + ')', self)
        if self.visible(True) and not self._drawing_next_level and not self._drawing_previous_level:
            
            if isinstance(message, events.InputEvent):
                if message.get_simple_event() == events.SE_UP:
                    self.select_previous_item()
                if message.get_simple_event() == events.SE_DOWN:
                    self.select_next_item()
                    
    def select_next_item(self):
        if self._current_level_id +1 < self._level_count and self._drawing_next_level == False and self._drawing_previous_level == False:
            self._drawing_next_level = True
            self._current_level_id += 1
    
    def select_previous_item(self):
        if self._current_level_id  > 0 and self._drawing_next_level == False and self._drawing_previous_level == False:
            self._drawing_previous_level = True
            self._current_level_id -= 1
        
    def refresh(self):
        surface.Surface.refresh(self)
        _step_scroll = 10
        _step_hide = 25
        if self._drawing_next_level == True:
            _ymin = - 50 * self._current_level_id
            (_x,_y,_z) = self._font_group.get_location()
            if _y > _ymin:
                #print str(_y) + " min:" + str(_ymin)
                _y = _y - _step_scroll
                if _y <= _ymin: _y = _ymin
                self._font_group.set_location(_x, _y, _z)
            else:
                self._drawing_next_level = False
        elif self._drawing_previous_level == True:
            if self._current_level_id > 0 : 
                _ymin = 50 * (self._current_level_id -2)
            else:
                _ymin = 0
                
            (_x,_y,_z) = self._font_group.get_location()
            #print str(_y) + " min:" + str(_ymin)
            if _y < _ymin:
                _y = _y +_step_scroll
                if _y >= _ymin: _y = - 50 * (self._current_level_id)
                #print str(_y) + " min:" + str(_ymin)
                self._font_group.set_location(_x, _y, _z)
            else:
                self._drawing_previous_level = False
        elif self._animate_hide_in_progress == True:
            (_x,_y,_z) = self.get_location()
            _alpha = self.get_alpha_level()
            _z += _step_hide
            _alpha -= 10
            if _z < 300:
                self.set_location(_x, _y, _z)
                if _alpha > 0:
                    self.set_alpha_level(_alpha, True)
                else:
                    self.set_alpha_level(0, True)             
            else:
                self.set_alpha_level(0, True)
                self._animate_hide_in_progress = False
                surface.Surface.hide(self,True)
        elif self._animate_show_in_progress == True:
            (_x,_y,_z) = self.get_location()
            _alpha = self.get_alpha_level()
            _z -= _step_hide
            _alpha += 10
            if _z > 0:
                self.set_location(_x, _y, _z)
                if _alpha <= 100:
                    self.set_alpha_level(_alpha, True)
                else:
                    self.set_alpha_level(100, True)             
            else:
                self.set_alpha_level(100, True)
                self.set_location(_x, _y, 0.1)
                self._animate_show_in_progress = False
                   
    def animate_hide(self):
        self._animate_hide_in_progress = True        
        
    def animate_show(self):
        surface.Surface.show(self,True)
        self._animate_show_in_progress = True
