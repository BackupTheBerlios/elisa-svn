from elisa.skins.default_skin.default_menu_widget import DefaultMenuWidget
from elisa.skins.default_skin import default_skin_pictures
from elisa.skins.mce_skin import mce_skin_pictures
from elisa.skins.mce_skin.mce_button_menu import MCEButtonMenu
from elisa.skins.default_skin.treeitem import TreeItem
from elisa.framework.menu import MenuTree

class MenuRenderer(object):

    def __init__(self, skin='default'):
        self._skin = skin
    
    def init_root_level(self, root_menuitems_list):
        self._root_menuitem_list = root_menuitems_list
        #self._menu_widget = Tree(self._root_menuitem_list, "main menu renderer")
        self._menu_widget = None
        self._skin_pictures = None
        self._menuitem_to_surface = {}
        self.surface_to_menuitem = {}
        
        if self._skin == 'mce':
            self._skin_pictures = mce_skin_pictures.MCESkinPictures()
            self._menu_widget = MCEButtonMenu(self._root_menuitem_list)
        else:
            self._skin_pictures = default_skin_pictures.DefaultSkinPictures()
            self._menu_widget = DefaultMenuWidget(self._root_menuitem_list, "main menu renderer")
    
    def get_skin_pictures(self, picture_name):
        return self._skin_pictures.get_picture(picture_name)
                
    def get_menu_widget(self):    
        return self._menu_widget
        
    def add_menuitem_surface(self, menuitem, surface):
        self._menuitem_to_surface[menuitem] = surface
        self.surface_to_menuitem[surface] = menuitem
        
    def remove_menuitem(self, menuitem):
        surface = self._menuitem_to_surface[menuitem]
        del self._menuitem_to_surface[menuitem]
        del self.surface_to_menuitem[surface]

    def get_menuitem_from_surface(self, surface):
        return self.surface_to_menuitem.get(surface)
        
    def get_surface_from_menuitem(self, menuitem):
        return self._menuitem_to_surface.get(menuitem)
