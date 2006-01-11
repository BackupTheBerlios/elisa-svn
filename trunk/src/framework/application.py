class BoxApplication(object):
    """
    Main box appication class
    """
    
    def __init__(self, in_renderer = None):
        """
        constructor
        @param in_renderer : renderer object used. if None, une default renderer
        @type in_renderer : L{render.RendererBase}
        """
        
    def AddPlugin(self, in_plugin, in_treelevel = 0):
        """
        add plugin to the main tree box menu
        @param in_plugin: plugin to add. by deflaut, plugin is added to root menu (root tree level)
        @type in_plugin: L{plugin.PluginTree}
        @param in_treelevel: tree level where plugin is added. default 0
        @type in_treelevel: number
        """
        
    def Run(self):
        """
        run main application loop
        """
