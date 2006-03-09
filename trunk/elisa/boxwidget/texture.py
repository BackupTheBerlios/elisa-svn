from elisa.boxwidget.bindings import testgl_impl
from elisa.framework.log import Logger
from Image import *

class Texture(object):
    
    def __init__(self):
        self._texture_impl = None
        self._texture_init = False
        self._texture_impl = testgl_impl._testGL_Texture_Impl()
    
    def init_texture(self,width, height, buffer=None, use_alpha=False):
        if self._texture_init == False:
            self._texture_impl.init_texture(width, height, buffer, use_alpha)
            self._texture_init = True
    
    def init_texture_from_picture(self, path_and_filename):
        if self._texture_init == False and path_and_filename != None: 
            _picture_file = open(path_and_filename)
            _buffer = _picture_file.tostring("raw", _picture_file.mode, 0, -1)
            
            if _picture_file.mode == "RGBA":
                use_alpha = True
            else:
                use_alpha = False

            self.init_texture(_picture_file.size[0], _picture_file.size[1], _buffer, use_alpha)
   
    def _get_surface_impl(self):
        return self._texture_impl
    
    def set_buffer(self, buffer):
        if self._texture_init == True:
            self._texture_impl.set_buffer(buffer)

    def set_flip_buffer(self, flip):
        self._texture_impl.set_flip_buffer(flip)
        
    def is_init(self):
        return self._texture_init
        
    def get_size(self):
        if self._texture_init == True:
            return self._texture_impl.get_size()
        return None
