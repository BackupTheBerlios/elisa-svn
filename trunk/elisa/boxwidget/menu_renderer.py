from elisa.skins.default_skin import tree

class MenuRenderer(object):

    def __init__(self, plugins_tree, skin='default'):
        self._menu_widget = tree.Tree(plugins_tree, "main menu renderer")
        
    def get_menu_widget(self):
        return self._menu_widget
