class _Base_Window_Impl(object):
    """
    windows binding base class 
    """

    def refresh(self): pass

    def set_back_color(self, red, green, blue): pass

    def set_background_from_file(self, path_and_filename=None): pass
        
    def close(self): pass
     
    def add_surface(self, impl_surface): pass

    def remove_surface(self, impl_surface): pass
    
    
class _Base_Surface_Impl(object):
    
    def get_native_surface(self): pass      
        
    def set_size(self, Width, Height): pass
        
    def set_location(self, x, y, z): pass
    
    def set_back_color(self, Red, Green, Blue): pass

    def set_background_from_file(self, path_and_filename=None): pass
    
    def set_alpha_level(self, level): pass
    
    def hide(self): pass

    def show(self): pass
    
    def set_texture(self, impl_texture): pass
    
    def set_background_from_buffer(self, buffer, width, height, flip = False): pass
    
    def set_texture(self, texture): pass
    
  
class _Base_EventsManager_Impl(object):
        
    def get_event_queue(self): pass
         

class _Base_Font_Impl(object):

    def get_native_surface(self): pass      
        
    def set_size(self, Width, Height): pass
    
    def get_size(self): pass
        
    def set_location(self, x, y, z): pass
    
    def set_back_color(self, Red, Green, Blue): pass
    
    def set_alpha_level(self, level): pass
    
    def hide(self): pass

    def show(self): pass

class _Base_Texture_Impl(object):

    def __init__(self): pass
    
    def init_texture(self, width, height, buffer=None, use_alpha=False): pass
                   
    def set_buffer(self, buffer): pass
    
    def set_flip_buffer(self, flip): pass
    
    def get_size(self): pass
