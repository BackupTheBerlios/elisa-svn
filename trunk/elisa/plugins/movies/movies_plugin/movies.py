
from elisa.framework.plugin import IPlugin, TreePlugin, ExtensionPoint
from elisa.framework.extension_points import IDataAccess
from elisa.framework.menu import MenuItem

import elisa.utils.misc

class MoviesTreePlugin(TreePlugin):
    """
    movies plugin_tree

    TODO:

    - create the thumbnail of each video item and display it instead of the dummy "movie"
      icon.
      
    """

    __implements__ = IPlugin

    data_access = ExtensionPoint(IDataAccess)

    
    name = "movies"
    default_config = {'locations':['sample_data/movies',]}

    def __init__(self, _application):
        TreePlugin.__init__(self, _application)
        self.set_short_name("videos")

        folder_image = 'elisa/skins/default_skin/pictures/folder.png'
        movie_image = 'elisa/skins/default_skin/pictures/movie.png'
        locations = self.get_config().get('locations')
        
        for data_loader in self.data_access:
            for location in locations:
                data_loader.load_location(location,
                                          item_filter=elisa.utils.misc.file_is_movie,
                                          folder_icon_path=folder_image,
                                          item_icon_path=movie_image,
                                          item_action=self.play_movie,
                                          #item_focus=self.focus_update,
                                          action_menu=self.add_action_menu)

    def add_action_menu(self, menu_item):
        
        play = MenuItem(short_name="Play")
        play.set_icon_path('elisa/skins/default_skin/pictures/rightarrow.png')
        play.set_action_callback(self.play_parent_movie)
        
        remove = MenuItem(short_name="Remove")
        remove.set_icon_path('elisa/skins/default_skin/pictures/trash.png')

        menu_item.add_item(play)
        menu_item.add_item(remove)

    def play_movie(self, menu_item):
        menu_renderer = self.get_application().get_menu_renderer()

        # display video on menu item
        surface = menu_renderer.get_surface_from_menuitem(menu_item)
        surface.set_background_from_file(menu_item.get_target_path())

        # Go full screen
        #surface.fullscreen()
        self.get_application().set_background_texture(surface.get_texture())


        # mute all other playing menu items
        manager = self.get_application().get_player_manager()
        player = manager.get_player(surface.get_background_file())
        manager.mute_all_except(player)

        player.un_mute()

    def play_parent_movie(self, menu_item):
        menu_renderer = self.get_application().get_menu_renderer()
        parent_item = menu_item.get_parent()
        self.play_movie(parent_item)
        
