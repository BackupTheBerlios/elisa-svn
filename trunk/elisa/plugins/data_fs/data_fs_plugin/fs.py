from elisa.framework.plugin import Plugin
from elisa.framework.extension_points import IDataAccess
from elisa.framework.menu import MenuTree, MenuItem
import os, re

class DataFSPlugin(Plugin):

    __implements__ = IDataAccess

    name = 'fs'

    hidden_file_pattern = re.compile(".*/\..*")

    def load_location(self, name, item_filter=None, folder_icon_path=None, item_focus=None,
                      item_action=None, item_icon_path=None, action_menu=None):
        if not os.path.isdir(name):
            return
        
        self.item_filter = item_filter
        self.folder_icon_path = folder_icon_path
        self.item_action = item_action
        self.item_icon_path = item_icon_path
        self.action_menu = action_menu
        self.item_focus = item_focus
        os.path.walk(name, self._load_sub_directory, None)

    def _load_sub_directory(self, app, dir_name, filenames):
        """
        Create the tree menu for a given directory full name
        
        """    
        for filename in filenames:
            path = os.path.join(dir_name, filename)
            path = os.path.abspath(path)

            if self.hidden_file_pattern.match(path):
                continue

            if os.path.isdir(path) or self.item_filter(path):
                item = MenuItem(short_name=os.path.basename(path))
                if os.path.isdir(path):
                    icon_path = self.folder_icon_path
                else:
                    icon_path = self.item_icon_path or path
                    item.set_action_callback(self.item_action)
                    item.set_focus_callback(self.item_focus)
                    
                item.set_target_path(path)
                item.set_icon_path(icon_path)

                if self.item_filter(path) and self.action_menu:
                    self.action_menu(item)
                
                master = self.get_master_plugin()
                parent = master.get_item_with_target(os.path.dirname(path))
                if not parent:
                    parent = master
                parent.add_item(item)
