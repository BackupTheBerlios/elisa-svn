from twisted.internet import reactor, task
from boxwidget import window, tree
from boxwidget.internal import factory
import menu, config, common

class BoxApplication(object):
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
        self._config = config.Config()
        
        factory._SetRenderer(self._config.Get("RenderEngine"))
        self._Fps = 50
        self._plugintreelist = []
        self._rootlevel = menu.MenuLevel("root")
        self._MainWindow = window.Window()
        self._WidgetLoopingCall =  task.LoopingCall(self.Refresh)
        self._WidgetLoopingCall.start(1.0 / self._Fps)
        

    def RestoreBackground(self):
        #FIXME : JUST PUT BACKGROUND TO BLACK
        self._MainWindow.SetBackgroundImage(None)
        self._MainWindow.SetBackColor(0,0,0)
    
    def MainWindow(self):
        return self._MainWindow

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
        if self._MainWindow.Closing():
            reactor.stop()
        self._MainWindow.Refresh()
            
    def Run(self):
        """
        run main application loop
        """
        self._MainWindow.OnLoad()
        
        #Create widget menu
        _treewidget = tree.Tree(self._rootlevel)
        _treewidget.SetSize(500, 100)
        _treewidget.SetLocation(120.0, 150.0, 2.0)
        self.MainWindow().AddSurface(_treewidget)
        
        reactor.run()
        
