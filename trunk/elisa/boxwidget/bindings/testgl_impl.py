import base_impl
from extern.testGL.zAPI.zForms import zForm, zPictureBox

class _testGL_Window_Impl(base_impl._Base_Window_Impl):
    """
    windows binding class for testGL renderEngine
    """

    def __init__(self):
        self._window_native=zForm.Form()
        self._window_native.FpsEnable = False
        
    def refresh(self):
        self._window_native.Refresh()

    def set_back_color(self, red, green, blue):
        self._window_native.SetBackColor(Red, Green, Blue)

    def set_background_from_file(self, path_and_file_name=None):
        self._window_native.SetBackgroundImageFromFile(PathAndFileName)
        
    def close(self):
        self._window_native.DisplayStats()
     
    def add_surface(self, impl_surface):
        self._window_native.AddControl(impl_surface.get_native_surface())
        #(_tx, _ty, _tz) = in_surface.GetAbsoluteLocation()
        #self._surface_native.SetLocation(_tx, _ty, _tz)

    def remove_surface(self, impl_surface):
        self._window_native.RemoveControl(impl_surface.get_native_surface())


class _testGL_Surface_Impl(object):

    def __init__(self):
        self._surface_native = zPictureBox.PictureBox()
    
    def get_native_surface(self):
        return self._surface_native       
        
    def set_size(self, Width, Height):  
        self._surface_native.SetSize(Width, Height)
        
    def set_location(self, x, y, z):
        self._surface_native.SetLocation( x, y, z)
    
    def set_back_color(self, Red, Green, Blue):
        self._surface_native.SetBackColor(Red, Green, Blue)

    def set_background_from_file(self, path_and_filename=None):
        self._surface_native.SetBackgroundImageFromFile(path_and_filename, True)
        
    def set_alpha_level(self, level):
        self._surface_native.SetAlpha(level*2.55)
        
    def hide(self):
        self._surface_native.Hide()

    def show(self):
        self._surface_native.Show()  
