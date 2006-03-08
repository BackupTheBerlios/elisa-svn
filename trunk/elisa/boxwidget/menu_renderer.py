from elisa.skins.default_skin.default_menu_widget import DefaultMenuWidget
from elisa.skins.default_skin.treeitem import TreeItem
from elisa.framework.menu import MenuTree

class MenuRenderer(object):

    def __init__(self, skin='default'):
        self._menu_tree = MenuTree('root')
        #self._menu_widget = Tree(self._menu_tree, "main menu renderer")
        self._menu_widget = None
        self._skin = skin
        self._menuitem_to_surface = {}
        self.surface_to_menuitem = {}
    
    def add_menu_item(self, menu_item, parent=None):
        if parent == None:
            self._menu_tree.add_item(menu_item)   
            
        #FIXME : tree data is not updatable yet
        # self._menu_widget.refesh_data()
            
    def get_menu_widget(self):
        #FIXME: created here because I can't refresh data after creation
        if self._menu_widget == None:
            if self._skin == "MCE":
                self._menu_widget = MCEButton()
            else:
                self._menu_widget = DefaultMenuWidget(self._menu_tree, "main menu renderer")
            
        return self._menu_widget
        
    def add_menuitem_surface(self, menuitem, surface):
        self._menuitem_to_surface[menuitem] = surface
        self.surface_to_menuitem[surface] = menuitem
        
    def remove_menuitem(self, menuitem):
        surface = self._menuitem_to_surface[menuitem]
        del self._menuitem_to_surface[menuitem]
        del self.surface_to_menuitem[surface]

    def get_menuitem_from_surface(self, surface):
        if surface in self.surface_to_menuitem:
            return self.surface_to_menuitem[surface]
        return None
        
    def get_surface_from_menuitem(self, menuitem):
        if menuitem in self._menuitem_to_surface:
            return self._menuitem_to_surface[menuitem]
        return None
