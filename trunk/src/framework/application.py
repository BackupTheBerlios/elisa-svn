
from framework import menu, config, common, log
import os
import time

import pkg_resources
from framework.plugin import InterfaceOmission, Plugin
import framework.config

"""
TODO:

- coding conventions
- backport the old Application (depending on boxwidget)

"""

class Application:
    """
    Main box application class
    """

    def __init__(self):
        self._plugin_tree_list = []
    
    def load_plugins(self, plugin_names=None):
        """ Add the plugins given their name. If no argument supplied,
        we load the plugins referenced in the 'general' section of the config

        """

        logger = log.Logger()
        config = framework.config.Config()
        
        if not plugin_names:
            plugin_names = config.get_option('plugins',default=[])

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
            
            assert issubclass(plugin_class,Plugin), '%r is not a valid Plugin!' % plugin_class

            self.register_plugin(plugin_class())
            logger.info("Loaded the plugin '%s'" % entrypoint.name)

    def register_plugin(self, in_plugin):
        self._plugin_tree_list.append(in_plugin)
        
    def run(self):
        logger = log.Logger()

        while 1:
            try:
                logger.info("i'm running")
                time.sleep(0.5)
            except:
                self.close()
                break
            
    def close(self):
        config = framework.config.Config()
        config.write()
        
