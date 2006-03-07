from elisa.boxwidget.bindings import testgl_impl
from elisa.framework.log import Logger

class Texture(object):
    
    def __init__(self):
        self._texture_impl = None
        self._texture_init = False
        self._texture_impl = testgl_impl._testGL_Texture_Impl()
    
    def init_texture(self,width, height, buffer=None, use_alpha=False):
        self._texture_impl.init_texture(width, height, buffer, use_alpha)
        self._texture_init = True
        
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
