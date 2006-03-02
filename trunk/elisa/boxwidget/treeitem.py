from elisa.boxwidget import surface

class TreeItem(surface.Surface): 

    def __init__(self, menuitem_data, font = None):
        surface.Surface.__init__(self, menuitem_data.get_short_name())
        self._menuitem_data = menuitem_data
        self._arrow_surface = surface.Surface(self._menuitem_data.get_short_name() + str(' arrow'))
        self._arrow_surface.set_back_color(255,255,255)
        self._arrow_surface.set_location(14,128,2.3)
        self._arrow_surface.set_size(100,20)
        self._arrow_surface.set_background_from_file("elisa/skins/default_skin/default_pictures/downarrow.png")
        self.add_surface(self._arrow_surface)
        self._font = font
        self.set_status(0)

    def show_label(self):
        if self._font != None and self.visible()==True:
            self._font.show()
            (_x,_y,_z) = self.get_location()
            self._font.set_text(self._menuitem_data.get_short_name())
            (_xf,_yf,_zf) = self._font.get_size()
            self._font.set_location(_x + 64 - _xf/2 , _y + 88, 2.4)
            
    def hide_label(self):
        if self._font != None: self._font.hide()

    def show_down_arrow(self):
        self._arrow_surface.set_alpha_level(100)
    
    def hide_down_arrow(self):
        self._arrow_surface.set_alpha_level(0)
            
    def get_menuitem_data(self):
        return self._menuitem_data
        
    def set_status(self, in_status):
        self._status = in_status
        
        if in_status == 0:
            self.set_alpha_level(35)
            self.hide_down_arrow()
            self.hide_label()
        else:
            self.set_alpha_level(100)
            if self._menuitem_data.get_items() != []: 
                self.show_down_arrow()
            self.show_label()
