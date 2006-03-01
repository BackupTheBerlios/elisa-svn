
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
        self.set_short_name("videos")
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

            is_dir = os.path.isdir(path)
            is_movie = elisa.utils.misc.file_is_movie(path)
            
            # FIXME: do not work with directory with same name in different level
            if is_dir or is_movie:
                item = MenuItem(short_name=os.path.basename(path))

                if os.path.isdir(path):
                    picture_path = 'elisa/skins/default_skin/default_pictures/folder.png'
                else:
                    picture_path = 'elisa/skins/default_skin/default_pictures/movie.png'
                item.set_picture_path(picture_path)

                if is_movie:
                    self.add_action_menu(item)
                
                parent = self.get_item_with_name(os.path.basename(dir_name))
                if not parent:
                    parent = self
                parent.add_item(item)

                    
    def _match_hidden(self, path):
        return re.match(".*/\..*", path)

    def add_action_menu(self, menu_item):
        
        play = MenuItem(short_name="Play")
        play.set_picture_path('elisa/skins/default_skin/default_pictures/rightarrow.png')

        remove = MenuItem(short_name="Remove")
        remove.set_picture_path('elisa/skins/default_skin/default_pictures/trash.png')

        menu_item.add_item(play)
        menu_item.add_item(remove)
