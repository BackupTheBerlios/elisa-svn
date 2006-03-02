from configobj import ConfigObj
from elisa.framework.log import Logger

CONFIG_FILE = "elisa.conf"

class Config:
    """ Elisa's configuration system

    Each configuration is stored in a text file. The configuration is
    structured in sections. There's at least one section called
    'general'. Each plugin has its own section (ex: 'plugin.foo').
    

    """
    
    def __init__(self, config_file=CONFIG_FILE):
        self._filename = config_file
        self._config = ConfigObj(config_file)
        self._logger = Logger()

    def get_filename(self):
        return self._filename
                    
    def get_option(self, key, section='general', default=None):
        """ Fetch the option value stored in the given section, at the
        given key. Return a default value if the key is not found.
        """
        return self.get_section(section).get(key, default)

    def set_option(self, key, value, section='general'):
        """ Store an option value under key id at the given section.
        """
        self._config[section][key] = value

    def del_option(self, key, section_name='general'):
        """ Remove the option identified by key under the specified
        section.
        """
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
        return self._config.get(section_name, {})

    def set_section(self, section_name, section_data):
        """
        Store section_data in a new section identified by section_name
        in the config
        """
        self._config[section_name] = section_data

    def del_section(self, section_name):
        """ Remove the section identified by section_name
        """
        if self._config.has_key(section_name):
            del self._config[section_name]

