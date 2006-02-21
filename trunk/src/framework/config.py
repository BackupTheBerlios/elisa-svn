from configobj import ConfigObj

CONFIG_FILE = "elisa.conf"

config = None

class _Config(object):
    
    def __init__(self):
        print 'loading configuration'
        self._config = ConfigObj(CONFIG_FILE)
        if not self._config:
            self.SetDefaultConfig()
                    
    def Get(self, key, section=None, default=None):
        if not section:
            section = 'general'
        return self._config[section].get(key, default)

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
        
    def SetDefaultConfig(self):
        self._config['general'] = {'resolution': (800, 600),
                                   'plugins': ('pictures','dvd'),
                                   'RenderEngine': 'testGL'}
        

def Config():
    global config
    if not config:
        config = _Config()
    return config
