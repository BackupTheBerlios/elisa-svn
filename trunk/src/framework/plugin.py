from framework import menu, config

class PluginBase(object):
    
    "Plugin Base Class"

    default_config = {}
    name = "default"
    
    def __init__(self):
        """
        Constructor
        """
        self.load_config()

    def load_config(self):
        print 'Plugin %s is loading its config' % self.name
        _config = config.Config()
        section_name = "plugins.%s" % self.name

        section = _config.get_section(section_name)
        if not section:
            section = self.default_config
            _config.add_section(section_name,self.default_config)

        self.config = section

    def get_config(self):
        return self.config
    


class PluginTree(PluginBase,menu.MenuTree):
    
    "tree navigation Plugin Class"
    
    def __init__(self):
        """
        Constructor
        """
        PluginBase.__init__(self)
        menu.MenuTree.__init__(self)

class PluginCustom(PluginBase):
    
    "custom interface Plugin Class"
    
    def __init__(self):
        """
        Constructor
        """


class PluginScreenless(PluginBase):
    
    "screenless Plugin Class"
    
    def __init__(self):
        """
        Constructor
        """
        
