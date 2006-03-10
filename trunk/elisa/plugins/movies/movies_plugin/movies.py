
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
        
        self.play = MenuItem(short_name="Play")
        self.play.set_target_path("play")
        self.play.set_icon_path('elisa/skins/default_skin/pictures/player_play.png')
        self.play.set_action_callback(self.play_parent_movie)

        self.pause = MenuItem(short_name="Pause")
        self.pause.set_target_path("pause")
        self.pause.set_icon_path('elisa/skins/default_skin/pictures/player_pause.png')
        self.pause.set_action_callback(self.pause_parent_movie)

        self.seekf = MenuItem(short_name="Seek+")
        self.seekf.set_icon_path('elisa/skins/default_skin/pictures/2rightarrow.png')
        self.seekf.set_action_callback(self.seekf_parent_movie)

        self.seekb = MenuItem(short_name="Seek-")
        self.seekb.set_icon_path('elisa/skins/default_skin/pictures/2leftarrow.png')
        self.seekb.set_action_callback(self.seekb_parent_movie)

        self.stop = MenuItem(short_name="Stop")
        self.stop.set_icon_path('elisa/skins/default_skin/pictures/stop.png')
        self.stop.set_action_callback(self.stop_parent_movie)
        
        remove = MenuItem(short_name="Remove")
        remove.set_icon_path('elisa/skins/default_skin/pictures/trash.png')

        menu_item.add_item(self.play)
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

        self.logger.info("Playing movie: %s" % player.get_uri())

        player.un_mute()

        _dock = manager.get_dock()
        _dock.add_item(self.pause)
        _dock.show(recursive=True)

##         # XXX: this is crap!
##         if menu_item.del_item_with_target("play"):
##             menu_item.insert_item(0, self.seekb)
##             menu_item.insert_item(1, self.pause)
##             menu_item.insert_item(2, self.seekf)
##             menu_item.insert_item(3, self.stop)

    def play_parent_movie(self, menu_item):
        self.play_movie(menu_item.get_parent())

    def pause_parent_movie(self, menu_item):
        self.pause_movie(menu_item.get_parent())
        
    def seekf_parent_movie(self, menu_item):
        self.seekf_movie(menu_item.get_parent())
        
    def seekb_parent_movie(self, menu_item):
        self.seekb_movie(menu_item.get_parent())
        
    def stop_parent_movie(self, menu_item):
        self.stop_movie(menu_item.get_parent())

    def get_player(self, menu_item):
        manager = self.get_application().get_player_manager()
        
        menu_renderer = self.get_application().get_menu_renderer()
        surface = menu_renderer.get_surface_from_menuitem(menu_item)

        if not surface:
            import pdb; pdb.set_trace()
        player = manager.get_player(surface.get_background_file())
        return player
    
    def pause_movie(self, menu_item):
        player = self.get_player(menu_item)
        player.pause()

        if menu_item.del_item_with_target("pause"):
            menu_item.insert_item(0, self.play)
        
    def seekf_movie(self, menu_item):
        player = self.get_player(menu_item)
        player.seek_forward(5)

    def seekb_movie(self, menu_item):
        player = self.get_player(menu_item)
        player.seek_backward(5)

    def stop_movie(self, menu_item):
        player = self.get_player(menu_item)
        player.stop()
