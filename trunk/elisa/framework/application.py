
from elisa.framework import config, log, menu
from elisa.framework.plugin import InterfaceOmission, Plugin
from elisa.utils import exception_hook
from elisa.boxwidget import window, tree

import os
import pkg_resources

"""
TODO:

- coding conventions
- backport the old Application (depending on boxwidget)

"""

class Application(window.Window):
    """
    Main box application class
    """

    def __init__(self, config_file_name=config.CONFIG_FILE):
        window.Window.__init__(self)
        self._config = None
        self._tree_data = menu.MenuTree('root')
        self.set_config(config_file_name)
        self.set_exception_hook()
        self._plugin_tree_list = []

    def set_config(self, config_file_name):
        """ Load the config stored in the file `config_file_name`
        """
        logger = log.Logger()
        logger.info("Using config file : %s" % config_file_name)
        self._config = config.Config(config_file_name)

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

        for entrypoint in pkg_resources.iter_entry_points("elisa.plugins"):
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

    def create_menu(self):
        """Create menu from plugin list
        """
        
        #only one plugin for the moment.
        #for plugin in self._plugin_tree_list:
        self._tree_data = self._plugin_tree_list[0]

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
            
    def close(self):
        """ Close the application. Good idea to save the configuration
        here, since it's probable it has been updated.
        """
        window.Window.close(self)
        self.get_config().write()
