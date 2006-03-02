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
    
    
class _Base_Surface_Impl(object):

    def __init__(self): pass
    
    def get_native_surface(self): pass      
        
    def set_size(self, Width, Height): pass
        
    def set_location(self, x, y, z): pass
    
    def set_back_color(self, Red, Green, Blue): pass

    def set_background_from_file(self, path_and_filename=None): pass
    
    def set_alpha_level(self, level): pass
    
    def hide(self): pass

    def show(self): pass
    
    def set_background_from_surface(self, impl_surface): pass
    
    def set_background_from_buffer(self, buffer, width, height): pass
  
  
class _Base_EventsManager_Impl(object):
        
    def get_event_queue(self): pass
            
    def pygame_event_converter(self, pyevent): pass

class _Base_Font_Impl(object):

    def __init__(self): pass
    
    def get_native_surface(self): pass      
        
    def set_size(self, Width, Height): pass
    
    def get_size(self): pass
        
    def set_location(self, x, y, z): pass
    
    def set_back_color(self, Red, Green, Blue): pass
    
    def set_alpha_level(self, level): pass
    
    def hide(self): pass

    def show(self): pass
