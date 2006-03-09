from OpenGL.GL import *
from OpenGL.GLU import *

class OpenGLTexture(object):

    def __init__(self):
        self._textureid = glGenTextures(1)
        self._format = None    
        self._width = None
        self._height = None
        self._XTextureRatio = 1
        self._YTextureRatio = 1
        self._texture_init = False
        self._buffer_flip = False
    
    def set_flip_buffer(self, flip):    
        self._buffer_flip = flip
        
    def get_flip_buffer(self):
        return self._buffer_flip
        
    def init_texture(self, width, height, format, buffer=None):
  
        if format not in (GL_RGBA, GL_RGB):
            raise("format invalid")
        self._format = format    
        self._width = width
        self._height = height
        TextureSize = 64
        if self._width > 0 and self._height > 0 : 
            while ((TextureSize) < self._width or (TextureSize) < self._height):
                TextureSize = TextureSize * 2         
         
        self._XTextureRatio = self._width / float(TextureSize)
        self._YTextureRatio = self._height / float(TextureSize)
        glBindTexture(GL_TEXTURE_2D, self._textureid)
        glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D (GL_TEXTURE_2D, 0, format, TextureSize, TextureSize, 0, format, GL_UNSIGNED_BYTE, None)
        
        if buffer != None:
            self.set_buffer(buffer)
        self._texture_init = True
   
    def get_ratio(self):
        return (self._XTextureRatio ,self._YTextureRatio)
        
    def get_size(self):
        return (self._width, self._height)
   
    def get_texture_id(self):        
        return self._textureid
   
    def GetFormat(self):
        return self._format
        
    def set_texture(self):
        if self._texture_init == True:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self._textureid)  
    
    def is_init(self):
        return self._texture_init

    def unset_texture(self):
        if self._texture_init == True:
            glDisable(GL_TEXTURE_2D)      
               
    def set_buffer(self, buffer):
        glBindTexture(GL_TEXTURE_2D, self._textureid)
        glTexSubImage2D (GL_TEXTURE_2D, 0, 0, 0, self._width, self._height, self._format, GL_UNSIGNED_BYTE, buffer) 



                    
        
