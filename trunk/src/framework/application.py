from boxwidget import window, tree, event, videosurface
from boxwidget.internal import factory
from framework import menu, config, common, log
import os

import pkg_resources
from framework.plugin import InterfaceOmission, Plugin


_config = config.Config()
factory._SetRenderer(_config.Get("RenderEngine"))

"""
TODO:

- coding conventions

"""

class Application(window.Window):
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
        
        self._videosurface = None
        self._videofilename = None

        self._plugintreelist = []
        self._rootlevel = menu.MenuLevel("root")

    def CreateVideoSurface(self):
        if self._videosurface != None: self.RemoveSurface(self._videosurface)
        self._videosurface = videosurface.VideoSurface()
        self._videosurface.SetSize(800.0,600.0)
        self._videosurface.SetLocation(0.0 ,0.0 , -0.01)
        self._videosurface.SetBackColor(255.0, 255.0, 255.0)
        self._videosurface.Hide()
        self.AddSurface(self._videosurface)
        
    def RestoreBackground(self):
        #JUST PUT BACKGROUND TO BLACK
        self.SetBackgroundFromFile(None)
        self.SetBackColor(0,0,0)
        if self._videosurface != None and self._videosurface.GetStatus() in (videosurface.VideoSurface.VS_PLAY, videosurface.VideoSurface.VS_PAUSE):
            self._videosurface.Show()   

    def load_plugins(self, plugin_names=None):
        """ Add the plugins given their name. If no argument supplied,
        we load the plugins referenced in the 'general' section of the config

        """

        logger = log.Logger()
        
        if not plugin_names:
            plugin_names = _config.get_option('plugins',default=[])

        for entrypoint in pkg_resources.iter_entry_points("elisa.plugins"):
            if entrypoint.name not in plugin_names:
                continue
            try:
                plugin_class = entrypoint.load()
            except InterfaceOmission, omission:
                log.info(omission)
                continue
            except AssertionError, error:
                log.error(error)
                continue

           assert issubclass(plugin_class,Plugin), '%r is not a valid Plugin!' % plugin_class
           self.AddPlugin(plugin_class())

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
    
    #FIXME : Crash when try another video when on is playing
    def StartVideoFile(self, in_filename):
        if os.path.exists(in_filename):
            if in_filename != self._videofilename: self.CreateVideoSurface()
            self._videofilename = in_filename
            self._videosurface.Stop()
            self._videosurface.SetVideoFile(in_filename)
            self._treewidget.HideGroup()
            self._videosurface.Play()
            self._videosurface.Show()
    
    def ShowImageFile(self, in_filename):
        if self._videosurface != None: self._videosurface.Hide()
        self.SetBackgroundFromFile(in_filename)
        
    def Run(self):
        
        #Create widget menu
        self._treewidget = tree.Tree(self._rootlevel)
        self._treewidget.SetSize(500, 100)
        self._treewidget.SetInitialLocation(105.0, 450.0, 2.0)
        self.AddSurface(self._treewidget)
        
        window.Window.Run(self)

    def Close(self):
        _config.write()
        window.Window.Close(self)
        
    def OnEvent(self, in_event):
        if in_event.GetSimpleEvent() == event.SE_MENU:
            self.ToogleMenu()

        return window.Window.OnEvent(self, in_event)
        
    def ToogleMenu(self):
        if self._treewidget.VisibleGroup()==True:
            self._treewidget.HideGroup()
        else:
            self._treewidget.ShowGroup()
