class _WidgetBase(object):
   
    """
    Base class of widget
    """
    
    def __init__(self): pass

    def GetRect(self):
        """
        return surface rectangle
        """
        
    def SetAlphaLevel(self, level):
        """
        set the alpha level in percent of the widget
        """

    def SetBackgroundImage(self, PathAndFileName):
        """
        set widget background image
        """
        
    def GetBackgroundImage(self):
        """
        return path and filename of background image
        """
        
    def SetSize(self, Width, Height):
        """
        define the size in 2D plan
        """
    
    def GetSize(self):
        """
        return current size
        """

    def SetLocation(self, x, y, z):
        """
        set location of widget
        """
    
    def GetLocation(self):
        """
        get 3D location
        """ 
    
    def Draw(self):
        """
        draw widget
        """
    
    def SetBackColor(self, Red, Green, Blue):
        """
        set widget backcolor
        """
