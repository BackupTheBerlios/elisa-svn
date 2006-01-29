from framework import plugin, menu, common

class PluginTreePictures(plugin.PluginTree):
    """
    radio plugin_tree
    """
          
    def __init__(self):
        plugin.PluginTree.__init__(self)
        
        app = common.GetApplication()
                
        level1 = menu.MenuLevel("picture_root_level")
        item1 = menu.MenuItem("pictures")
        item1.SetPicturePathAndFilename("icons/camera.png")
        level1.AddItem(item1)
        
        level2 = menu.MenuLevel("folder level")
        level2.ShowItemLabel()
        item11 = menu.MenuItem("nature")
        item11.SetPicturePathAndFilename("icons/folder.png")
        level2.AddItem(item11)     
        item12 = menu.MenuItem("animals")
        item12.SetPicturePathAndFilename("icons/folder.png")
        level2.AddItem(item12)

        
        level3 = menu.MenuLevel("nature pictures level")
        level3.ShowItemLabel()
        level3.HidePreviousMenu()
        level3.SetUnselectedCallback(app.RestoreBackground,None)
        item31 = menu.MenuItem("house")
        item31.SetPicturePathAndFilename("sample_data/pictures/nature/house.jpg")
        item31.SetSelectedCallback(app.ShowImageFile,"sample_data/pictures/nature/house.jpg")
        level3.AddItem(item31) 

        item32 = menu.MenuItem("mountain")
        item32.SetPicturePathAndFilename("sample_data/pictures/nature/mountain.jpg")
        item32.SetSelectedCallback(app.ShowImageFile,"sample_data/pictures/nature/mountain.jpg")
        level3.AddItem(item32) 
        
        item33 = menu.MenuItem("tree")
        item33.SetPicturePathAndFilename("sample_data/pictures/nature/tree.jpg")
        item33.SetSelectedCallback(app.ShowImageFile,"sample_data/pictures/nature/tree.jpg")
        level3.AddItem(item33) 
        
        item34 = menu.MenuItem("wall")
        item34.SetPicturePathAndFilename("sample_data/pictures/nature/wall.jpg")
        item34.SetSelectedCallback(app.ShowImageFile,"sample_data/pictures/nature/wall.jpg")
        level3.AddItem(item34) 
        
        level4 = menu.MenuLevel("animals pictures level")
        level4.ShowItemLabel()
        level4.HidePreviousMenu()
        level4.SetUnselectedCallback(app.RestoreBackground,None)
        item41 = menu.MenuItem("duck")
        item41.SetPicturePathAndFilename("sample_data/pictures/animals/duck.jpg")
        item41.SetSelectedCallback(app.ShowImageFile,"sample_data/pictures/animals/duck.jpg")
        level4.AddItem(item41) 

        item42 = menu.MenuItem("lambs")
        item42.SetPicturePathAndFilename("sample_data/pictures/animals/lambs.jpg")
        item42.SetSelectedCallback(app.ShowImageFile,"sample_data/pictures/animals/lambs.jpg")
        level4.AddItem(item42) 
        
        item43 = menu.MenuItem("dogs")
        item43.SetPicturePathAndFilename("sample_data/pictures/animals/dogs.jpg")
        item43.SetSelectedCallback(app.ShowImageFile,"sample_data/pictures/animals/dogs.jpg")
        level4.AddItem(item43) 
        
        item44 = menu.MenuItem("hippo")
        item44.SetPicturePathAndFilename("sample_data/pictures/animals/hippo.jpg")
        item44.SetSelectedCallback(app.ShowImageFile,"sample_data/pictures/animals/hippo.jpg")
        level4.AddItem(item44) 
        
        self.SetRootLevel(level1)
        self.AddLevel(level2, level1, item1)
        self.AddLevel(level3, level2, item11)
        self.AddLevel(level4, level2, item12)
        
