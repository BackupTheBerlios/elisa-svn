from configobj import ConfigObj

CONFIG_FILE = "elisa.conf"

DEFAULT = {'resolution': (800, 600),
           'plugins': ('pictures','dvd'),
           'RenderEngine': 'testGL'}

config = None

class _Config(object):
    
    def __init__(self):
        print 'loading configuration'
        self._config = ConfigObj(CONFIG_FILE)
        if not self._config:
            self.create_default_config()
                    
    def get_option(self, key, section='general', default=None):
        return self._config[section].get(key, default)

    def set_option(self, key, section='general', value):
        self._config[section][key] = value

    def write(self):
        """
        save the config in a text file (handled by ConfigObj)
        
        """
        print 'saving config...'
        self._config.write()

    def get_section(self, section_name):
        """
        @return the ConfigObj section identified by section_name
        """
        return self._config.get(section_name)

    def add_section(self, section_name, section_data):
        """
        Store section_data in a new section identified by section_name
        in the config
        """
        self._config[section_name] = section_data

    def create_default_config(self):
        self._config['general'] = DEFAULT


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
