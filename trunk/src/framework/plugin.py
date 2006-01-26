import menu

class PluginBase(object):
    
    "Plugin Base Class"
    
    def __init__(self):
        """
        Constructor
        """

class PluginTree(PluginBase):
    
    "tree navigation Plugin Class"
    
    def __init__(self):
        """
        Constructor
        """
        self._maintree = None
        
    def SetMenuTree(self, in_tree):
        self._maintree = in_tree
        
    def GetMenuTree(self):
        return self._maintree

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
        
