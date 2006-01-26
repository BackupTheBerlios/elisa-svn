from framework import plugin, menu

class PluginTreeMovies(plugin.PluginTree):
    """
    radio plugin_tree
    """
    
    def __init__(self):
        item1 = menu.MenuItem("radio")
        item11 = menu.MenuItem("NRJ")
        item12 = menu.MenuItem("europe1")
        item13 = menu.MenuItem("France inter")
        item21 = menu.MenuItem("play")
        item22 = menu.MenuItem("pause")
        
        item1.SetPicturePathAndFilename("icons/movie.png")
        item11.SetPicturePathAndFilename("icons/gnome-mime-audio-ac3.png")
        item12.SetPicturePathAndFilename("icons/gnome-mime-audio-ac3.png")
        item13.SetPicturePathAndFilename("icons/gnome-mime-audio-ac3.png")
        item21.SetPicturePathAndFilename("icons/gnome-mime-audio-ac3.png")
        item22.SetPicturePathAndFilename("icons/gnome-mime-audio-ac3.png")
        
        level1 = menu.MenuLevel("radio_root_level")
        level1.AddItem(item1)
        
        level2 = menu.MenuLevel("radiolist level")
        level2.AddItem(item11)
        level2.AddItem(item12)
        level2.AddItem(item13)
        
        level3 = menu.MenuLevel("radiolist level")
        level3.AddItem(item21)
        level3.AddItem(item22)
        
        tree = menu.MenuTree(level1)
        tree.AddLevel(level2, level1, item1)
        tree.AddLevel(level3, level2, item11)
        tree.AddLevel(level3, level2, item12)
        tree.AddLevel(level3, level2, item13)
        
        self.SetMenuTree(tree)
