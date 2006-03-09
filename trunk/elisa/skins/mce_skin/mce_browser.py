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
        
        for menuitem in self._menuitem_list:
            s = TreeItem(menuitem)
            self.add(s)
             
    def animate_before_hide(self):
        self._animate_hide_in_progress = True        
        
    def animate_before_show(self):
        surface.Surface.show(self,True)
        self._animate_show_in_progress = True
        
    def get_current_menuitem(self):
        return self._menuitem_list[self._current_level_rank-1]
