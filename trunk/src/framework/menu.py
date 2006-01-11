class MenuItem(object):

    """
    manipulate menu item element
    """
    
    def __init__(self): pass
        
    def Set(self, key, value):
        """
        set value of menuitem
        
        key can be :
            - shortname (string) : name used on menu if picture is not set
            - helpstring (string) : helpstring shown on box when item is selected
            - picture (string) : complete path of picture shown in menu
            - callback (function) : callback called when menu item is selected
        
        @param key: parameter name
        @type key: string
        @param value: value
        @type value: value associated to key
       
        """
        
    def Get(self, key):
        """
        get value of menuitem
        @param key: parameter name, see set function
        @type key: string
        @return: the value of the key
        """
        
        
class MenuLevel(object):

    """
    manipulate menu level element (group of L{menu.MenuItem} element)
    """
    
    def __init__(self): pass
    
    def AddItem(self, item):
        """
        add item to level
        """
    
    def RemoveItem(self, item):
        """
        remove item from level
        """
        
    def GetItemList(self):
        """
        return item list
        """
    
class MenuTree(object):

    """
    manipulate a tree element (hierachical group of L{menu.MenuLevel} element)
    """
    
    def __init__(self): pass
    
    def AddLevel(self, new_level, parent_level):
        """
        add item under a parent level
        """
    
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
