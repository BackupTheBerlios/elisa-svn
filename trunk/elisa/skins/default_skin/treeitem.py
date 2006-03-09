from elisa.boxwidget import surface
from elisa.framework import common

class TreeItem(surface.Surface): 

    def __init__(self, menuitem, font = None, enable_arrow = False):
        surface.Surface.__init__(self, menuitem.get_short_name())
        self._appli = common.get_application()
        self._focus = False
        self._menuitem = menuitem
        self._enable_arrow = enable_arrow
        
        if enable_arrow == True:
            self._arrow_surface = surface.Surface(self._menuitem.get_short_name() + str(' arrow'))
            self._arrow_surface.set_back_color(255,255,255)
            self._arrow_surface.set_location(14,128,2.3)
            self._arrow_surface.set_size(100,20)
            self._arrow_surface.set_background_from_file("elisa/skins/default_skin/pictures/downarrow.png")
            self.add_surface(self._arrow_surface)
        else:
            self._arrow_surface = None
            
        self._font = font
        self.set_focus(False)
        
        if self._appli.get_player_manager().uri_is_attached(menuitem.get_target_path()) == True:
            #Movie is playing
            p = self._appli.get_player_manager().get_player(menuitem.get_target_path())
            self.set_texture(p.get_texture())
        else:
            self.set_background_from_file(menuitem.get_icon_path())
            
    def show_label(self):
        if self._font != None and self.visible()==True:
            self._font.show()
            (_x,_y,_z) = self.get_location()
            self._font.set_text(self._menuitem.get_short_name())
            (_xf,_yf,_zf) = self._font.get_size()
            self._font.set_location(_x + 64 - _xf/2, _y + 88, 2.4)
            
    def hide_label(self):
        if self._font != None: self._font.hide()

    def show_down_arrow(self):
        if self._enable_arrow == True:
            self._arrow_surface.set_alpha_level(100)
    
    def hide_down_arrow(self):
         if self._enable_arrow == True:
            self._arrow_surface.set_alpha_level(0)
            
    def get_menuitem(self):
        return self._menuitem
    
    def has_focus(self):
        return self._focus
            
    def set_focus(self, focus):
        self._focus = focus

        menu_item = self.get_menuitem()
        menu_item.fire_focus_callback(menu_item, focus)
        
        if focus == False:
            self.set_alpha_level(35)
            self.hide_down_arrow()
            self.hide_label()
        else:
            self.set_alpha_level(100)
            if self._menuitem.get_items() != []: 
                self.show_down_arrow()
            self.show_label()
