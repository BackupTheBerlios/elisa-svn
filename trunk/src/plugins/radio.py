from framework import plugin, menu, common

class PluginTreeRadio(plugin.PluginTree):
    """
    radio plugin_tree
    """

    name = "radios"
    
    def __init__(self):
        plugin.PluginTree.__init__(self)
        
        app = common.GetApplication()
        
        level1 = menu.MenuLevel("radio_root_level")
        item1 = menu.MenuItem("radios")
        item1.SetPicturePathAndFilename("icons/kmix.png")
        level1.AddItem(item1)
        
        level2 = menu.MenuLevel("movies level")
        level2.ShowItemLabel()
        item11 = menu.MenuItem("radios")
        item11.SetPicturePathAndFilename("icons/folder.png")
        level2.AddItem(item11)     
        item12 = menu.MenuItem("music files")
        item12.SetPicturePathAndFilename("icons/folder.png")
        level2.AddItem(item12)
        
        level3 = menu.MenuLevel("nature pictures level")
        level3.ShowItemLabel()
        item31 = menu.MenuItem("NRJ")
        item31.SetPicturePathAndFilename("icons/kmix.png")
        level3.AddItem(item31) 

        item32 = menu.MenuItem("europe 1")
        item32.SetPicturePathAndFilename("icons/kmix.png")
        level3.AddItem(item32) 
        
        item33 = menu.MenuItem("le mouv")
        item33.SetPicturePathAndFilename("icons/kmix.png")
        level3.AddItem(item33) 
        
        item34 = menu.MenuItem("couleur 3")
        item34.SetPicturePathAndFilename("icons/kmix.png")
        level3.AddItem(item34) 
        
        self.SetRootLevel(level1)
        self.AddLevel(level2, level1, item1)
        self.AddLevel(level3, level2, item11)
