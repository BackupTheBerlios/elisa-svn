class _Base_Window_Impl(object):
    """
    windows binding base class 
    """

    def __init__(self): pass
    
    def refresh(self): pass

    def set_back_color(self, red, green, blue): pass

    def set_background_from_file(self, path_and_filename=None): pass
        
    def close(self): pass
     
    def add_surface(self, impl_surface): pass

    def remove_surface(self, impl_surface): pass
