from internal import factory

class Surface(factory._SurfaceFactory()):
    """
    Surface class
    """
    
    def __init__(self):
        super(Surface,self).__init__()  

class SurfaceGroup(Surface):
    """
    SurfaceGroup class
    group all surface, but have not 
    """
    
    def __init__(self):
        Surface.__init__(self)
        #Surface of group element are always hidden
        Surface.Hide(self)
        
        self._ChildVisible = True
        
    def HideGroup(self):
        self._ChildVisible = False
        self.RecursiveHide(self)
    
    def RecursiveHide(self, in_surface):
        for s in in_surface._GetChildSurface():
            s.Hide()
            self.RecursiveHide(s)
            
    def ShowGroup(self):
        self._ChildVisible = True
        self.RecursiveShow(self)
        
    def RecursiveShow(self, in_surface):
        for s in in_surface._GetChildSurface():
            s.Show()
            self.RecursiveShow(s)
            
    def VisibleGroup(self):
        return self._ChildVisible
