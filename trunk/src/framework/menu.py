class MenuItem(object):

    """
    manipulate menu item element
    """
    
    def __init__(self, in_shortname = "None", in_helpstring="", in_picturepath = None, in_callback = None ):
        self._shortname = in_shortname
        self._helpstring = in_helpstring
        self._picturepath = in_picturepath
        self._callback = in_callback
        self._level = None
        
    def SetShortname(self, in_shortname):
        """name used on menu if picture is not set"""
        self._shortname = in_shortname
    
    def GetShortname(self):
        "name used on menu if picture is not set"
        return self._shortname
    
    def SetLevel(self, in_level):
        """name used on menu if picture is not set"""
        self._level = in_level
    
    def GetLevel(self):
        "name used on menu if picture is not set"
        return self._level
        
    def SetHelpstring(self, in_helpstring):
        """helpstring shown on box when item is selected"""
        self._helpstring = in_helpstring
        
    def GetHelpstring(self):
        """helpstring shown on box when item is selected"""
        return self._helpstring
     
    def SetPicturePathAndFilename(self, in_picturepath):
        """complete path of picture shown in menu"""
        self._picturepath = in_picturepath
    
    def GetPicturePathAndFilename(self):
        """complete path of picture shown in menu"""
        return self._picturepath
    
    def SetCallback(self, in_callback):
        """callback called when menu item is selected"""
        self._callback = in_callback
        
    def GetCallback(self):
        """callback called when menu item is selected"""
        return self._callback
        
    def __repr__(self):
        return self._shortname + ":" + str(MenuItem)
           
class MenuLevel(object):

    """
    manipulate menu level element (group of L{menu.MenuItem} element)
    """
    
    def __init__(self, in_levelname = "level"):
        """
        constructor
        """
        self._levelname = in_levelname
        
        """
        levelist format is :
        [ [item, level attached], [item, level attached] ....]
        level attached is the next level under current item. default value is None
        """
        self._itemlist = []
        
    def __repr__(self):
        return self._levelname + ":" + str(MenuLevel)
        
    def AddItem(self, in_item):
        """
        add item to level
        """
        self._itemlist.append(in_item)
    
    def RemoveItem(self, in_item):
        """
        remove item from level
        """
    
    def GetItemList(self):
        """
        return item list
        """
        return self._itemlist
    
class MenuTree(object):

    """
    manipulate a tree element (hierachical group of L{menu.MenuLevel} element)
    """
    
    def __init__(self, in_rootlevel): 
        self._treelist = []
        self._treelist.append(in_rootlevel)
        self._rootlevel = in_rootlevel
    
    def AddLevel(self, in_newlevel, in_parentlevel, in_parentitem):
        """
        add item under a parent level
        """
        self._treelist.append(in_newlevel)
        in_parentitem.SetLevel(in_newlevel)
    
    def RemoveLevel(self, level):
        """
        remove level from tree
        """
        
    def GetChildLevel(self, level):
        """
        return child level list
        """
        
    def AddTree(self, subtree, level):
        """
        add a subtree at parent level
        
        @param subtree: a tree
        @type subtree: L{menu.MenuTree}
        @param level:level where item of the first level of subtree will added
        @type level: number
        """

    def GetTreeList(self):
        return self._treelist
        
    def GetRootLevel(self):
        return self._rootlevel
