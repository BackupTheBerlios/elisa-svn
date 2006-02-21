from framework import plugin, menu

class PluginTreeDvd(plugin.PluginTree):
    """
    dvd plugin_tree
    """

    name = "dvd"

    def __init__(self):
        plugin.PluginTree.__init__(self)
        
        item1 = menu.MenuItem("DVD")
        item11 = menu.MenuItem("Play")
        item12 = menu.MenuItem("Eject")
        
        item1.SetPicturePathAndFilename("icons/dvd.png")
        item11.SetPicturePathAndFilename("icons/dvd.png")
        item12.SetPicturePathAndFilename("icons/dvd.png")
        
        level1 = menu.MenuLevel("dvd_root_level")
        level1.AddItem(item1)
        
        level2 = menu.MenuLevel("dvd level")
        level2.AddItem(item11)
        level2.AddItem(item12)
        
        self.SetRootLevel(level1)
        self.AddLevel(level2, level1, item1)
       
