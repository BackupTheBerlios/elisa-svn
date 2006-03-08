
from elisa.framework import config, log, menu, message_bus, common
from elisa.framework.plugin import InterfaceOmission, Plugin
from elisa.utils import exception_hook
from elisa.boxwidget import window, surface_player, menu_renderer
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
        self._plugins = {}
        self._plugin_tree_list = []
        self._player_manager = player.PlayerManager()
        
        self._background_surface = surface_player.SurfacePlayer(None)
        self._background_surface.set_location(0, 0, 0)
        self._background_surface.set_size(800, 600)
        self._background_surface.set_back_color(0, 0, 0)
        self.add_surface(self._background_surface)
        
        self._menu_renderer = None

    def set_background_texture(self, texture):
        self._background_surface.set_back_color (255, 255, 255)
        self._background_surface.set_texture(texture)

    def get_menu_renderer(self):
        return self._menu_renderer
        
    def get_player_manager(self):
        return self._player_manager
        
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

    def load_plugins(self):

        for entry_point in ( 'plugins.data', 'plugins',):
            self.load_plugins_for_entry_point('elisa.%s' % entry_point)

    def load_plugins_for_entry_point(self, entry_point_name='elisa.plugins'):
        """ Add the plugins given their entry point name.
        """

        logger = log.Logger()

        # drop the first part of the entry_point name
        # elisa.plugins => plugins
        conf_plugins_name = '.'.join(entry_point_name.split('.')[1:])
        
        plugin_names = self.get_config().get_option(conf_plugins_name, default=[])
        
        for entrypoint in pkg_resources.iter_entry_points(entry_point_name):
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

            self.register_plugin(entry_point_name, plugin_class(self))
            logger.info("Loaded the plugin '%s'" % entrypoint.name)

        loaded = [ ]
        for entry_point, plugins in self.get_plugins().iteritems():
            loaded.extend(plugins)
        loaded = [ p.get_name() for p in loaded ]
        
        s1 = Set(loaded)
        s2 = Set(plugin_names)
        if not s2.issubset(s1):
            logger.info("Plugins not found : %s" % ', '.join(list(s2-s1)))
            
    def create_menu(self):
        """Create menu from plugin list
        """
        self._menu_renderer = menu_renderer.MenuRenderer()

        main_plugins = self.get_plugins()['elisa.plugins']
        plugin_names = self.get_config().get_option('plugins', default=[])
        
        # re-order plugins list to match the order in config
        mapped_plugins = dict([ (p.get_name(), p) for p in main_plugins ])
        self._plugin_tree_list = [ mapped_plugins[name] for name in plugin_names ]

        for tree in self._plugin_tree_list:
            new_item = tree.as_menu_item()
            # TODO: set the plugin's icon
            #       use pkg_resources to find icon's path
            path = 'elisa/skins/default_skin/default_pictures/%s.png' % tree.get_name()
            new_item.set_icon_path(path)
            self._menu_renderer.add_menu_item(new_item)
   
    def register_plugin(self, entry_point_name, plugin):
        """ Add the given plugin instance to our internal plugins list.
        """
        try:
            self._plugins[entry_point_name].append(plugin)
        except KeyError:
            self._plugins[entry_point_name] = [plugin, ]
        #self._plugin_tree_list.append(plugin)

    def get_plugins(self):
        return self._plugins
        
    def run(self):
        """ Execute the application. Start main loop.
        """
        self._menu_widget = self._menu_renderer.get_menu_widget()
        self._menu_widget.set_size(500, 100)
        self._menu_widget.set_initial_location(105.0, 450.0, 2.0)
        self.add_surface(self._menu_widget)
        
        window.Window.run(self)

    def refresh(self):
        self._player_manager.refresh()
        window.Window.refresh(self)
        message_bus.MessageBus().dispatch_messages()
            
    def close(self):
        """ Close the application. Good idea to save the configuration
        here, since it's probable it has been updated.
        """
        self._player_manager.close()
        window.Window.close(self)
        self.get_config().write()
        
