class RendererBase(object):
    
    """
    Main renerder base Class
    
    This class start the main loop and draw the main menu.
    """
    
    def __init__(self, in_pluginlist):
        """
        Constructor
        @param in_pluginlist: list of plugin in the root menu
        @type in_pluginlist: list of L{plugin.PluginBase} object
        """
        
    def RenderLoop(self):
        """
        start main loop and render the menu
        """
        
    def HideMenu(self):
        """
        hide all menu with a transition
        """
        
    def ShowMenu(self):
        """
        show complete menu with transition
        """
        
    def CollapseMenu(self):
        """
        collapse menu for free render area
        """
        
    def ExpandMenu(self):
        """
        expand menu to complete view
        """
        
    def SetFramerate(self):
        """
        set the maximal framerate of render engine
        """

class Renderer(RendererBase):

    """
    default renderer class (with default skin
    """
    def __init__(self, in_pluginlist):
        RendererBase.__init__(self, in_pluginlist)
