from elisa.boxwidget import surface, fontsurface, events

class MCEButtonMenu(surface.Surface):

    def __init__(self, root_menuitem_list, name="mce menu button"):
        surface.Surface.__init__(self, name)
        self._root_menuitem_list = root_menuitem_list
        self._drawing_next_level = False
        self._drawing_previous_level = False
        
        self.set_alpha_level(0)
        self.set_location(300.0, 250, 0.1)
        
        self._font_group = surface.Surface()
        #self._font_group.set_alpha_level(0)
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
            _ft.set_location(10.0, _y, 0.3)
            _y += 50
            self._font_group.add_surface(_ft)
            
    def on_message(self, receiver, message, sender):
        self._logger.debug('Tree.on_event(' + str(message) + ')', self)
        if self.visible(True) and not self._drawing_next_level and not self._drawing_previous_level:
            
            if isinstance(message, events.InputEvent):
                if message.get_simple_event() == events.SE_UP:
                    self.select_previous_item()
                if message.get_simple_event() == events.SE_DOWN:
                    self.select_next_item()
                if message.get_simple_event() == events.SE_OK: pass
                    
    def select_next_item(self):
        self._drawing_next_level = True
    
    def select_previous_item(self):
        self._drawing_previous_level = True
        
    def refresh(self):
        surface.Surface.refresh(self)
        if self._drawing_next_level == True: pass
        elif self._drawing_previous_level == True: pass
        
        
