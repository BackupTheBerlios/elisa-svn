
from framework.plugin import IPlugin, PluginTree
import os


class PicturesPluginTree(PluginTree):
    """
    pictures plugin_tree
    """

    __implements__ = IPlugin

    
    name = "pictures"
    default_config = {'root_directory':'/tmp'}

    def __init__(self):
        PluginTree.__init__(self)
        self._levels = {}
        
        self.load_root_directory()
        

    def load_root_directory(self):
        """
        Create the whole directory tree menu from the root directory
        (which is referenced in the plugin's config.
        
        """
        pass
