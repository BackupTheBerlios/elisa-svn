
from elisa.framework import menu, config, log
from elisa.utils import exception_hook
import os
import time

import pkg_resources
from elisa.framework.plugin import InterfaceOmission, Plugin
import elisa.framework.config

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
        self.set_exception_hook()
        self._plugin_tree_list = []

    def set_exception_hook(self):
        config = elisa.framework.config.Config()
        mail_section = config.get_section('mail')

        enable = int(mail_section.get('enable', '0'))
        if enable:
            mail_from = mail_section.get('mail_from', 'elisa@localhost')
            mail_to = mail_section.get('mail_to', ['phil@localhost'])
            mail_subject = "Elisa error"
            smtp_server = mail_section.get('smtp_server', 'localhost')

            exception_hook.set_exception_hook(mail_from, mail_to, mail_subject, smtp_server)

    def load_plugins(self, plugin_names=None):
        """ Add the plugins given their name. If no argument supplied,
        we load the plugins referenced in the 'general' section of the config

        """

        logger = log.Logger()
        config = elisa.framework.config.Config()
        
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
        config = elisa.framework.config.Config()
        config.write()
        
