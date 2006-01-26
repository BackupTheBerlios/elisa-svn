import menu

class PluginBase(object):
    
    "Plugin Base Class"
    
    def __init__(self):
        """
        Constructor
        """

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
        
