from twisted.internet import reactor, task
from boxwidget import window
from boxwidget.internal import factory
import menu, config

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
        self._config = config.Config()
        
        factory._SetRenderer(self._config.Get("RenderEngine"))
        self._Fps = 50
        self._plugintreelist = []
        self._rootlevel = menu.MenuLevel("root")
        self._MainWindow = window.Window()
        self._WidgetLoopingCall =  task.LoopingCall(self.Refresh)
        self._WidgetLoopingCall.start(1.0 / self._Fps)
        
    
    
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
        _plugin_root_level = in_plugin.GetMenuTree().GetTreeList()[0]
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
        reactor.run()
        
