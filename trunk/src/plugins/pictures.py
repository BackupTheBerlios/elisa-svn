from framework import plugin, menu

class PluginTreePictures(plugin.PluginTree):
    """
    radio plugin_tree
    """
    
    def __init__(self):
        
        
        level1 = menu.MenuLevel("picture_root_level")
        item1 = menu.MenuItem("root")
        item1.SetPicturePathAndFilename("icons/camera.png")
        level1.AddItem(item1)
        
        level2 = menu.MenuLevel("folder level")
        item11 = menu.MenuItem("nature")
        item11.SetPicturePathAndFilename("icons/folder.png")
        level2.AddItem(item11)     
        item12 = menu.MenuItem("animals")
        item12.SetPicturePathAndFilename("icons/folder.png")
        level2.AddItem(item12)

        
        level3 = menu.MenuLevel("nature pictures level")
        item31 = menu.MenuItem("house")
        item31.SetPicturePathAndFilename("sample_data/pictures/nature/house.jpg")
        level3.AddItem(item31) 

        item32 = menu.MenuItem("mountain")
        item32.SetPicturePathAndFilename("sample_data/pictures/nature/mountain.jpg")
        level3.AddItem(item32) 
        
        item33 = menu.MenuItem("tree")
        item33.SetPicturePathAndFilename("sample_data/pictures/nature/tree.jpg")
        level3.AddItem(item33) 
        
        item34 = menu.MenuItem("wall")
        item34.SetPicturePathAndFilename("sample_data/pictures/nature/wall.jpg")
        level3.AddItem(item34) 
        
        level4 = menu.MenuLevel("animals pictures level")
        item41 = menu.MenuItem("house")
        item41.SetPicturePathAndFilename("sample_data/pictures/animals/duck.jpg")
        level4.AddItem(item41) 

        item42 = menu.MenuItem("mountain")
        item42.SetPicturePathAndFilename("sample_data/pictures/animals/lambs.jpg")
        level4.AddItem(item42) 
        
        item43 = menu.MenuItem("tree")
        item43.SetPicturePathAndFilename("sample_data/pictures/animals/dogs.jpg")
        level4.AddItem(item43) 
        
        item44 = menu.MenuItem("wall")
        item44.SetPicturePathAndFilename("sample_data/pictures/animals/hippo.jpg")
        level4.AddItem(item44) 
        
        tree = menu.MenuTree(level1)
        tree.AddLevel(level2, level1, item1)
        tree.AddLevel(level3, level2, item11)
        tree.AddLevel(level4, level2, item12)
        
        self.SetMenuTree(tree)
