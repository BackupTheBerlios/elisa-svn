from configobj import ConfigObj
from elisa.framework.log import Logger

CONFIG_FILE = "elisa.conf"

config = None

class _Config(object):
    
    def __init__(self):

        self._config = ConfigObj(CONFIG_FILE)
        self._logger = Logger()

        self._logger.info('loading configuration')
                    
    def get_option(self, key, section='general', default=None):
        return self.get_section(section).get(key, default)

    def set_option(self, key, value, section='general'):
        self._config[section][key] = value

    def del_option(self, key, section_name='general'):
        section = self.get_section(section_name)
        if section and section.has_key(key):
            del section[key]
        self.set_section(section_name, section)

    def write(self):
        """
        save the config in a text file (handled by ConfigObj)
        
        """
        self._logger.info('saving config...')
        self._config.write()

    def get_section(self, section_name):
        """
        @return the ConfigObj section identified by section_name
        """
        return self._config.get(section_name,{})

    def set_section(self, section_name, section_data):
        """
        Store section_data in a new section identified by section_name
        in the config
        """
        self._config[section_name] = section_data

    def del_section(self, section_name):
        if self._config.has_key(section_name):
            del self._config[section_name]

    # deprecated
        
    def Get(self, key, section=None, default=None):
        raise DeprecationWarning, 'use get_option() method!'
    
    def SetDefaultConfig(self):
        raise DeprecationWarning, 'use create_default_config() method!'


def Config():
    global config
    if not config:
        config = _Config()
    return config
