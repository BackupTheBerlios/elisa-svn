from extern.testGL.common import constants
from OpenGL.GL import *
from OpenGL.GLU import *
from extern.testGL.zAPI.zRenderer import zBaseClass, zOpenGLTexture
from extern.testGL.zAPI.zDrawing import zRectangle3D
from extern.testGL.zAPI.zDrawing.zPoint3D import Point3D
from Image import *

class OpenGLSurface(zBaseClass.SurfaceBase):
    
    def __init__(self,ApplyCoordinateTrans=True):
    
        self._GLposX, self._GLposY, self._GLposZ = (0,0,0)
        self._GLwidth, self._GLheight, self._GLdeep = (0,0,0)
        
        zBaseClass.SurfaceBase.__init__(self)
        self._TextureOrder = 0
        self._screenwidth, self._screenheight = constants.GetWindowSize()
        self._ApplyCoordinateTrans = ApplyCoordinateTrans
        self._renderer = None
        self._texture = zOpenGLTexture.OpenGLTexture()
        
    def SetBackgroundImageFromFile(self, FileName, UseAlpha=False):
        zBaseClass.SurfaceBase.SetBackgroundImageFromFile(self, FileName, UseAlpha=False)
   
        if FileName != None: 
            _BackgroundImage = open(FileName)
            #Alpha is allowed only for png images
            s = len(FileName)
            ext = FileName[s-3:s]
            if ext not in ('PNG','png'): UseAlpha=False
            
            if UseAlpha == True:
                _format = GL_RGBA
                _ImageBuffer = _BackgroundImage.tostring("raw", "RGBA", 0, -1)
            else:
                _format = GL_RGB
                _ImageBuffer = _BackgroundImage.tostring("raw", "RGB", 0, -1)

        self.set_texture_buffer(_BackgroundImage.size[0], _BackgroundImage.size[1], _format, _ImageBuffer)


    def set_texture_buffer(self,width, height, _format, _buffer):
        if self._texture.is_init() == True and \
		( self._texture.get_size() != (width, height) or self._texture.GetFormat() != _format):
            self._texture = zOpenGLTexture.OpenGLTexture()  
            
        if self._texture.is_init() == False:

            self._texture.init_texture(width, height, _format, None)

        self._texture.set_buffer(_buffer)
        
    def SetBackgroundImageFromBuffer(self, _buffer, width, height, UseAlpha=False):

        if UseAlpha == True:
            _format = GL_RGBA
        else:
            _format = GL_RGB
        self.set_texture_buffer(width, height, _format, _buffer)
    
    def SetTextureOrder(self, order):
        if order == 1 or order == 0:
              self._TextureOrder = order
        
    def _SetTextureID(self, textureid):
        #print "set textureid to " + str(textureid) + " on " + str(self)
        self._TextureID = textureid
              
    def Render(self):
        glPushMatrix()
      
        glTranslatef(self._GLposX, self._GLposY, self._GLposZ)        glScalef(self._GLwidth, -self._GLheight, self._GLdeep)
        #FIXME cache result.
        r,g,b,a = self.GetBackColorWithAlpha()
        glColorf(r/255.0, g/255.0, b/255.0, a/255.0)
          
        self.draw_quad()
        
        glPopMatrix()
    
    def draw_quad(self):

	(_XTextureRatio, _YTextureRatio) = (1.0, 1.0)    
        if self._texture != None:
            self._texture.set_texture()
            (_XTextureRatio, _YTextureRatio) = self._texture.get_ratio()
            if self._texture.get_flip_buffer() == False:
                self._TextureOrder = 0
            else:
                self._TextureOrder = 1

        XTextureOffsetPercent = 0.0
        YTextureOffsetPercent = 0.0
        
        XTextureOffset = -XTextureOffsetPercent * _XTextureRatio / 100.0
        YTextureOffset = -YTextureOffsetPercent * _YTextureRatio / 100.0    

	#FIXME : use lists
        if self._TextureOrder == 1:
            #Texture for normal coordinate system
            glBegin(GL_QUADS)
            glTexCoord2f(_XTextureRatio+XTextureOffset,YTextureOffset)
            glVertex3f(1.0, 0.0, 0.0)
            glTexCoord2f(XTextureOffset,YTextureOffset)
            glVertex3f(0.0, 0.0, 0.0)
            glTexCoord2f(XTextureOffset,_YTextureRatio+YTextureOffset)
            glVertex3f(0.0, 1.0, 0.0)
            glTexCoord2f(_XTextureRatio+XTextureOffset,_YTextureRatio+YTextureOffset)
            glVertex3f(1.0, 1.0, 0.0)            glEnd()
        else:
            #Texture for Videos    
            glBegin(GL_QUADS)
            glTexCoord2f(_XTextureRatio+XTextureOffset,YTextureOffset)
            glVertex3f(1.0, 1.0, 0.0)
            glTexCoord2f(XTextureOffset,YTextureOffset)
            glVertex3f(0.0, 1.0, 0.0)
            glTexCoord2f(XTextureOffset,_YTextureRatio+YTextureOffset)
            glVertex3f(0.0, 0.0, 0.0) 
            glTexCoord2f(_XTextureRatio+XTextureOffset,_YTextureRatio+YTextureOffset)
            glVertex3f(1.0, 0.0, 0.0)            glEnd() 
	
	if self._texture != None :
            self._texture.unset_texture()


    def SetSize(self, Width, Height):
        zBaseClass.SurfaceBase.SetSize(self, Width, Height)
        if self._ApplyCoordinateTrans == True:
            if self._renderer==None:
                self._renderer = constants.GetForm()._GetRenderer()
                self._worldwidth, self._worldheight = self._renderer.GetWorldSize()
            self._GLwidth = Width * self._worldwidth / float(self._screenwidth)
            self._GLheight = Height * self._worldheight / float(self._screenheight)
        else:
            self._GLwidth = Width
            self._GLheight = Height
        
    def SetLocation(self, x, y, z):
        zBaseClass.SurfaceBase.SetLocation(self, x, y, z)
        self._GLposZ = z
        if self._ApplyCoordinateTrans == True:
            if self._renderer==None:
                self._renderer = constants.GetForm()._GetRenderer()
                self._worldwidth, self._worldheight = self._renderer.GetWorldSize()
            self._GLposX = (x*self._worldwidth / float(self._screenwidth)) - float(self._worldwidth/2)
            self._GLposY = float(self._worldheight/2) - (y*self._worldheight / float(self._screenheight)) 
        else:
            self._GLposX = x
            self._GLposY = y
        
    def ApplyRotation(self, Rotate):
        assert isinstance(Rotate, Point3D) , "Rotate has wrong type"
        glRotatef(Rotate.x, 1.0, 0.0, 0.0)
        glRotatef(Rotate.y, 0.0, 1.0, 0.0)
        glRotatef(Rotate.z, 0.0, 0.0, 1.0)

    def GetTexture(self):
        return self._texture
        
    def SetTexture(self, texture):
        self._texture = texture
