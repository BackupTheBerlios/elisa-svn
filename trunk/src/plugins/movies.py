from framework import plugin, menu, common

class PluginTreeMovies(plugin.PluginTree):
    """
    radio plugin_tree
    """
    
    def __init__(self):
        plugin.PluginTree.__init__(self)
        
        app = common.GetApplication()
        
        level1 = menu.MenuLevel("movies_root_level")
        item1 = menu.MenuItem("movies")
        item1.SetPicturePathAndFilename("icons/movie.png")
        level1.AddItem(item1)
        
        level2 = menu.MenuLevel("movies level")
        level2.ShowItemLabel()
        item11 = menu.MenuItem("nemo")
        item11.SetPicturePathAndFilename("icons/folder.png")
        item11.SetActionCallback(app.StartVideoFile,"/home/yoyo/temp/nemo-fr.avi")
        level2.AddItem(item11)     
        item12 = menu.MenuItem("le roi lion")
        item12.SetPicturePathAndFilename("icons/folder.png")
        item12.SetActionCallback(app.StartVideoFile,"/home/yoyo/temp/Le-roi-lion.avi")
        level2.AddItem(item12)
        
        self.SetRootLevel(level1)
        self.AddLevel(level2, level1, item1)
