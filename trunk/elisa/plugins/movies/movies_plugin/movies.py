
from elisa.framework.plugin import IPlugin, TreePlugin
from elisa.framework.menu import MenuTree, MenuItem
import elisa.utils.misc

import os
import re

class MoviesTreePlugin(TreePlugin):
    """
    movies plugin_tree
    """

    __implements__ = IPlugin

    
    name = "movies"
    default_config = {'root_directory':'sample_data/movies'}

    def __init__(self, application):
        TreePlugin.__init__(self, application)
        self.set_short_name("Movies menu")
        self.load_root_directory()

    def load_root_directory(self):
        """
        Create the whole directory tree menu from the root directory
        (which is referenced in the plugin's config.
        
        """
        root = self.get_config().get('root_directory')
        os.path.walk(root, self._load_sub_directory, None)

    def _load_sub_directory(self, app, dir_name, filenames):
        """
        Create the tree menu for a given directory full name
        
        """
        for filename in filenames:
            path = os.path.join(dir_name, filename)

            if self._match_hidden(path):
                continue
            
            #FIXME: do not work with directory with same name in different level
            if os.path.isdir(path) or elisa.utils.misc.file_is_movie(path):
                item = MenuItem(short_name=os.path.basename(path))

                if os.path.isdir(path):
                    picture_path = 'elisa/skins/default_skin/default_pictures/folder.png'
                else:
                    picture_path = 'elisa/skins/default_skin/default_pictures/movie.png'
                item.set_picture_path(picture_path)
                
                parent = self.get_item_with_name(os.path.basename(dir_name))
                if not parent:
                    parent = self
                parent.add_item(item)
                    
    def _match_hidden(self, path):
        return re.match(".*/\..*", path)
