from boxwidget import window, tree
from boxwidget.internal import factory
import menu, config, common

_config = config.Config()
factory._SetRenderer(_config.Get("RenderEngine"))


class BoxApplication(window.Window):
    """
    Main box appication class
    """
    
    def __init__(self):
        """
        constructor
        @param in_renderer : renderer object used. default renderer in "testGL"
        @type in_renderer : string
        """
        common._SetApplication(self)
        window.Window.__init__(self)
          
        self._plugintreelist = []
        self._rootlevel = menu.MenuLevel("root")

    def RestoreBackground(self):
        #FIXME : JUST PUT BACKGROUND TO BLACK
        self.SetBackgroundImage(None)
        self.SetBackColor(0,0,0)

    def AddPlugin(self, in_plugin):
        """
        add plugin to the main tree box menu
        @param in_plugin: plugin to add. by deflaut, plugin is added to root menu (root tree level)
        @type in_plugin: L{plugin.PluginTree}
        @param in_treelevel: tree level where plugin is added. default 0
        @type in_treelevel: number
        """
        self._plugintreelist.append(in_plugin)
        _plugin_root_level = in_plugin.GetTreeList()[0]
        self._rootlevel.AddItem(_plugin_root_level.GetItemList()[0])
        
    def Refresh(self):            
        window.Window.Refresh(self)
            
    def Run(self):
        
        #Create widget menu
        _treewidget = tree.Tree(self._rootlevel)
        _treewidget.SetSize(500, 100)
        _treewidget.SetLocation(120.0, 150.0, 2.0)
        self.AddSurface(_treewidget)
        
        window.Window.Run(self)
        
 
    def ToogleMenu(self):
        if _treewidget.Visible()==True:
            _treewidget.Hide()
        else:
            _treewidget.Show()
