
from elisa.framework.plugin import IPlugin

class IDataAccess(IPlugin):

    def load_location(name, item_filter, folder_icon_path,
                      item_action, item_icon_path, action_menu=None):
        """
        Build a menu representing the data holded at the given location.

        - item_filter: boolean callable used to check wether a node of
          the tree is a leaf or not
        - folder_icon_path: item icon path for nodes
        - item_action: callable activated when a leaf receives an action message
        - item_icon_path: item icon path for leaves
        - action_menu: callable used to build sub-menus for leaves (optional)
        """
    
    
