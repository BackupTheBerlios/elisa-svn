
from elisa.framework import config, log, menu, message_bus, common
from elisa.framework.plugin import InterfaceOmission, Plugin
from elisa.utils import exception_hook
from elisa.boxwidget import window, tree, surface_player
from elisa.player import player

from sets import Set

import os
import pkg_resources

class Application(window.Window):
    """
    Main box application class
    """
     
    def __init__(self, config_filename=config.CONFIG_FILE):
        common._set_application(self)
        self.set_config(config_filename)
        self.set_exception_hook()
        
        logger = log.Logger()
        config = self.get_config()
        
        logger.set_level(config.get_option('log_level'))
        console_log_output = int(config.get_option('console_log_output'))
        if console_log_output:
            logger.enable_console_output()
        else:
            logger.disable_console_output()

        logger.info("Using config file : %s" % config.get_filename())


        window.Window.__init__(self)
        self._plugin_tree_list = []
        self._player_manager = player.PlayerManager()
        self._player_surface = surface_player.SurfacePlayer(None)
        self._player_surface.set_location(0, 0, 0)
        self._player_surface.set_size(800, 600)
        self._player_surface.set_back_color(0, 0, 0)
        self.add_surface(self._player_surface)

    def set_background_from_surface(self, surface):
        """show same background in fullscreen than _surface (video or picture)
        """
        self._player_surface.set_background_from_surface(surface)
        self._player_surface.set_back_color(255.0, 255.0, 255.0)

    def set_background_from_menuitem(self, menuitem):
        """show same background in fullscreen than _surface (video or picture)
        """
        surface = self._treewidget.get_current_level_surface().get_itemsurface_from_menuitem(menuitem)
        self.set_background_from_surface(surface)
        
    def set_config(self, filename):
        self._config = config.Config(filename)
    
    def get_config(self):
        """ Return the application's config which is a `config.Config`
        instance.
        """
        return self._config

    def set_exception_hook(self):
        """ Override the default system exception hook with our
        EmailTracebackHook.
        """
        mail_section = self.get_config().get_section('mail')

        enable = int(mail_section.get('enable', '0'))
        if enable:
            mail_from = mail_section.get('mail_from', 'elisa@localhost')
            mail_to = mail_section.get('mail_to', ['phil@localhost'])
            mail_subject = "Elisa error"
            smtp_server = mail_section.get('smtp_server', 'localhost')

            exception_hook.set_exception_hook(mail_from, mail_to,
                                              mail_subject, smtp_server)

    def load_plugins(self, plugin_names=None):
        """ Add the plugins given their name. If no argument supplied,
        we load the plugins referenced in the 'general' section of the config

        """

        logger = log.Logger()
        
        if not plugin_names:
            plugin_names = self.get_config().get_option('plugins', default=[])

        for entrypoint in pkg_resources.iter_entry_points('elisa.plugins'):
            if entrypoint.name not in plugin_names:
                continue
            try:
                plugin_class = entrypoint.load()
            except InterfaceOmission, omission:
                log.info(omission)
                continue
            except AssertionError, error:
                log.error(error)
                continue
            
            assert issubclass(plugin_class, Plugin), \
                   '%r is not a valid Plugin!' % plugin_class

            self.register_plugin(plugin_class(self))
            logger.info("Loaded the plugin '%s'" % entrypoint.name)

        loaded = [ plugin.get_name() for plugin in self._plugin_tree_list ]
        s1 = Set(loaded)
        s2 = Set(plugin_names)
        if not s2.issubset(s1):
            logger.info("Plugins not found : %s" % ', '.join(list(s2-s1)))
        

    def create_menu(self):
        """Create menu from plugin list
        """
        self._tree_data = menu.MenuTree('root')

        for tree in self._plugin_tree_list:
            new_item = tree.as_menu_item()
            # TODO: set the plugin's icon
            #       use pkg_resources to find icon's path
            path = 'elisa/skins/default_skin/default_pictures/%s.png' % tree.get_name()
            new_item.set_picture_path(path)
            self._tree_data.add_item(new_item)

    def register_plugin(self, in_plugin):
        """ Add the given plugin instance to our internal plugins list.
        """
        self._plugin_tree_list.append(in_plugin)
        
    def run(self):
        """ Execute the application. Start main loop.
        """
        self._treewidget = tree.Tree(self._tree_data, "main menu Tree")
        self._treewidget.set_size(500, 100)
        self._treewidget.set_initial_location(105.0, 450.0, 2.0)
        self.add_surface(self._treewidget)
        
        window.Window.run(self)

    def refresh(self):
        window.Window.refresh(self)
        message_bus.MessageBus().dispatch_messages()
            
    def close(self):
        """ Close the application. Good idea to save the configuration
        here, since it's probable it has been updated.
        """
        window.Window.close(self)
        self.get_config().write()
