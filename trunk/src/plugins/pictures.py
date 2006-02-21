from framework import plugin, menu, common
import os


class PluginTreePictures(plugin.PluginTree):
    """
    radio plugin_tree
    """
    
    name = "pictures"
    default_config = {'root_directory':'/tmp'}

    def __init__(self):
        plugin.PluginTree.__init__(self)
        self._levels = {}
        
        self.load_root_directory()
        

    def load_root_directory(self):
        """
        Create the whole directory tree menu from the root directory
        (which is referenced in the plugin's config.
        
        """
        root = self.get_config()['root_directory']

        self.root_level = menu.MenuLevel("picture_root_level")
        item1 = menu.MenuItem("pictures")
        item1.SetPicturePathAndFilename("icons/camera.png")
        self.root_level.AddItem(item1)
        self.SetRootLevel(self.root_level)

        app = common.GetApplication()
        os.path.walk(root, self._load_sub_directory, app)

        if self._levels:
            print self._levels
            level2 = menu.MenuLevel("folder level")
            level2.ShowItemLabel()
            #self.AddLevel(level2, self.root_level, item1)
            

    def _load_sub_directory(self, app, dir_name, filenames):
        """
        Create the tree menu for a given directory full name
        
        """

        for filename in filenames:
            path = os.path.join(dir_name, filename)

            if os.path.isdir(path):

                depth = self._get_depth_from_root(path)
                level = menu.MenuLevel(path)
                level.ShowItemLabel()
                level.HidePreviousMenu()
                level.SetUnselectedCallback(app.RestoreBackground,None)
                self.add_level(level, depth)
                
            else:
                depth = self._get_depth_from_root(dir_name)

                item = menu.MenuItem(path)
                item.SetPicturePathAndFilename(path)
                item.SetSelectedCallback(app.ShowImageFile,path)

                self.add_item(item, depth)
                                

    def _get_depth_from_root(self, path):
        root = self.get_config()['root_directory']
        depth = 0

        # strip the ending /
        if path.endswith(os.path.sep):
            path = path[:-1]

        # skip the root path
        path = path[len(root):]

        idx = path.find(os.path.sep)
        while idx != -1:
            path = path[idx+1:]
            idx = path.find(os.path.sep)
            depth += 1

        return depth


    def add_item(self, item, depth):
        item_name = item.GetShortname()
        
        for level in self._levels[depth]:
            if item_name.startswith(level._levelname):
                #print 'Adding %s in %s' % (item_name, level._levelname)
                level.AddItem(item)
                return

    def add_level(self, level, depth):

        try:
            self._levels[depth].append(level)
        except KeyError:
            self._levels[depth] = [level,]
        
    """
                
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
        
    """
