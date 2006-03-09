from elisa.boxwidget import surface, fontsurface, events
from elisa.skins.default_skin.treeitem import TreeItem

class MCEBrowser(surface.Surface):

    def __init__(self, menuitem_list, name="mce browser"):
        surface.Surface.__init__(self, name)
        self._menuitem_list = menuitem_list
        self._current_level_rank = 1
        self.set_size(0.0, 0.0)
        self._animate_hide_in_progress = False
        self._animate_show_in_progress = False
        
        _i = 0
        for menuitem in self._menuitem_list:
            s = TreeItem(menuitem)
            s.set_size(128, 128)
            s.set_location(_i, -12, 2.2)
            _i += 150
            self.add_surface(s)
            
        self.animate_before_hide()
        
    def refresh(self):
        surface.Surface.refresh(self)
        _step_hide = 25
        
        if self._animate_show_in_progress == True:
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
                self._animate_show_in_progress = False
                surface.Surface.hide(self,True)
        elif self._animate_hide_in_progress == True:
            (_x,_y,_z) = self.get_location()
            _alpha = self.get_alpha_level()
            _z -= _step_hide
            _alpha += 10
            if _z > -100:
                self.set_location(_x, _y, _z)
                print _z
                if _alpha <= 100:
                    self.set_alpha_level(_alpha, True)
                else:
                    self.set_alpha_level(100, True)             
            else:
                self.set_alpha_level(100, True)
                self.set_location(_x, -100, 0.1)
                self._animate_hide_in_progress = False
             
    def animate_before_hide(self):
        self._animate_hide_in_progress = True        
        
    def animate_before_show(self):
        surface.Surface.show(self,True)
        self._animate_show_in_progress = True
        
    def get_current_menuitem(self):
        return self._menuitem_list[self._current_level_rank-1]
