from elisa.boxwidget import surface, fontsurface, events

class MCEBrowser(surface.Surface):

    def __init__(self, menuitem_list, name="mce browser"):
        surface.Surface.__init__(self, name)
        self._menuitem_list = menuitem_list
        self.set_size(0.0, 0.0)
        self._animate_hide_in_progress = False
        self._animate_show_in_progress = False
             
    def animate_hide(self):
        self._animate_hide_in_progress = True        
        
    def animate_show(self):
        surface.Surface.show(self,True)
        self._animate_show_in_progress = True
