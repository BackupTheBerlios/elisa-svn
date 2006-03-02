from extern.testGL.common import constants
from OpenGL.GL import *
from OpenGL.GLU import *
from extern.testGL.zAPI.zRenderer import zBaseClass
from extern.testGL.zAPI.zDrawing import zRectangle3D
from extern.testGL.zAPI.zDrawing.zPoint3D import Point3D
from Image import *

class OpenGLSurface(zBaseClass.SurfaceBase):
    
    def __init__(self,ApplyCoordinateTrans=True):
    
        self._GLposX, self._GLposY, self._GLposZ = (0,0,0)
        self._GLwidth, self._GLheight, self._GLdeep = (0,0,0)
        
        zBaseClass.SurfaceBase.__init__(self)
        self._TextureOrder = 0
        self._BackgroundImage = None
        self._RefreshTexture = False
        self._TextureID = None
        self._XTextureRatio = 1.0
        self._YTextureRatio = 1.0
        self._ImageBuffer=True
        self._Format=GL_RGB
        self._BufferWidth=None
        self._BufferHeight=None
        self._screenwidth, self._screenheight = constants.GetWindowSize()
        self._ApplyCoordinateTrans = ApplyCoordinateTrans
        self._renderer = None
        self._same_texture_surface_list = []
    
    def add_surface_with_same_texture(self, surface):
        #print "add_surface_with_same_texture( " + str(surface) + " ) on " + str(self)
        self._same_texture_surface_list.append(surface)
        surface._SetTextureID(self._TextureID)
        surface.SetTextureOrder(self._TextureOrder)
        surface._SetTextureRatio(self._XTextureRatio, self._YTextureRatio)
        
    def remove_surface_with_same_texture(self, surface):
        if surface in self._same_texture_surface_list:
            self._same_texture_surface_list.remove(surface)
    
    def _refresh_surface_with_same_texture(self):
        #print "Start refresh on " + str(self)
        for surface in self._same_texture_surface_list:
            #print "refresh " + str(surface) + " to " + str(self._TextureID)
            surface._SetTextureID(self._TextureID)
            surface.SetTextureOrder(self._TextureOrder)
            surface._SetTextureRatio(self._XTextureRatio, self._YTextureRatio)
        
    def SetTextureOrder(self, order):
        if order == 1 or order == 0:
              self._TextureOrder = order
        
    def _SetTextureID(self, textureid):
        #print "set textureid to " + str(textureid) + " on " + str(self)
        self._TextureID = textureid
     
    def _SetTextureRatio(self, x, y):
       self._XTextureRatio = x
       self._YTextureRatio = y
             
    def SetBackgroundImageFromFile(self, FileName, UseAlpha=False):
        isinstance(UseAlpha, bool)," UseAlpha need Boolean as parameter"
        zBaseClass.SurfaceBase.SetBackgroundImageFromFile(self, FileName, UseAlpha=False)
   
        if FileName == None:
            self._BackgroundImage = None
            self._RefreshTexture = False
        else:    
            self._BackgroundImage = open(FileName)
            #Alpha is allowed only for png images
            s = len(FileName)
            ext = FileName[s-3:s]
            if ext not in ('PNG','png'): UseAlpha=False
            
            if UseAlpha == True:
                self._Format = GL_RGBA
                self._ImageBuffer = self._BackgroundImage.tostring("raw", "RGBA", 0, -1)
            else:
                self._Format = GL_RGB
                self._ImageBuffer = self._BackgroundImage.tostring("raw", "RGB", 0, -1)

            self._BufferWidth = self._BackgroundImage.size[0]
            self._BufferHeight = self._BackgroundImage.size[1]  
            self._RefreshTexture = True

    def SetBackgroundImageFromBuffer2(self, buffer, width, height, UseAlpha=False):
        isinstance(UseAlpha, bool)," UseAlpha need Boolean as parameter"
        self._ImageBuffer = buffer
        self._BufferWidth = width
        self._BufferHeight = height
        if buffer == None:
            self._RefreshTexture = False
        else:    
            if UseAlpha == True:
                self._Format = GL_RGBA
            else:
                self._Format = GL_RGB
                
            self._RefreshTexture = True
    
    def SetBackgroundImageFromBuffer(self, buffer, width, height, UseAlpha=False):
        isinstance(UseAlpha, bool)," UseAlpha need Boolean as parameter"
        self._ImageBuffer = buffer.data
        self._BufferWidth = width
        self._BufferHeight = height
        
        if buffer == None:
            self._RefreshTexture = False
        else:    
            if UseAlpha == True:
                self._Format = GL_RGBA
            else:
                self._Format = GL_RGB
                
            self._RefreshTexture = True

    def RecreateTexture(self): self._TextureID = None
    
    #FIXME : allow different image size. actually, all image must have the same size.
    def LoadTexture(self):
    
        CreateTexture = False
               
        if self._TextureID == None:
            self._TextureID = glGenTextures(1)
            CreateTexture = True
               
        TextureSize = 64
        
        if self._BufferWidth > 0 and self._BufferHeight > 0 : 
            while ((TextureSize) < self._BufferWidth or (TextureSize) < self._BufferHeight):
                TextureSize = TextureSize * 2         
         
        self._XTextureRatio = self._BufferWidth / float(TextureSize);
        self._YTextureRatio = self._BufferHeight / float(TextureSize);      

        glBindTexture(GL_TEXTURE_2D, self._TextureID)
        
        if CreateTexture == True: 
            #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri (GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
            glTexImage2D (GL_TEXTURE_2D, 0, self._Format, TextureSize, TextureSize, 0, self._Format, GL_UNSIGNED_BYTE, None)        glTexSubImage2D (GL_TEXTURE_2D, 0, 0, 0, self._BufferWidth, self._BufferHeight, self._Format, GL_UNSIGNED_BYTE, self._ImageBuffer) 
        
        self._refresh_surface_with_same_texture()
        
    def Render(self):
        glPushMatrix()
      
        glTranslatef(self._GLposX, self._GLposY, self._GLposZ)        glScalef(self._GLwidth, -self._GLheight, self._GLdeep)
        #FIXME cache result.
        r,g,b,a = self.GetBackColorWithAlpha()
        glColorf(r/255.0, g/255.0, b/255.0, a/255.0)
        
        if self._RefreshTexture == True:
            self._RefreshTexture = False
            self.LoadTexture()
            
        if self._TextureID != None:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self._TextureID)
            #print "texture loaded: " + str(self._TextureID)
        #else:
            #print "texture not loaded: " + str(self._TextureID) + " on " + str(self)
        
        XTextureOffsetPercent = 0.0
        YTextureOffsetPercent = 0.0
        XTextureOffset = -XTextureOffsetPercent * self._XTextureRatio / 100.0
        YTextureOffset = -YTextureOffsetPercent * self._YTextureRatio / 100.0      
        
        #FIXME : use lists
        if self._TextureOrder == 1:
            #Texture for normal coordinate system
            glBegin(GL_QUADS)
            glTexCoord2f(self._XTextureRatio+XTextureOffset,YTextureOffset)
            glVertex3f(1.0, 0.0, 0.0)
            glTexCoord2f(XTextureOffset,YTextureOffset)
            glVertex3f(0.0, 0.0, 0.0)
            glTexCoord2f(XTextureOffset,self._YTextureRatio+YTextureOffset)
            glVertex3f(0.0, 1.0, 0.0)
            glTexCoord2f(self._XTextureRatio+XTextureOffset,self._YTextureRatio+YTextureOffset)
            glVertex3f(1.0, 1.0, 0.0)            glEnd()
        else:
            #Texture for Videos    
            glBegin(GL_QUADS)
            glTexCoord2f(self._XTextureRatio+XTextureOffset,YTextureOffset)
            glVertex3f(1.0, 1.0, 0.0)
            glTexCoord2f(XTextureOffset,YTextureOffset)
            glVertex3f(0.0, 1.0, 0.0)
            glTexCoord2f(XTextureOffset,self._YTextureRatio+YTextureOffset)
            glVertex3f(0.0, 0.0, 0.0) 
            glTexCoord2f(self._XTextureRatio+XTextureOffset,self._YTextureRatio+YTextureOffset)
            glVertex3f(1.0, 0.0, 0.0)            glEnd() 
        
        if self._TextureID != None :#and self._BackgroundImage != None :
            glDisable(GL_TEXTURE_2D)
            
        glPopMatrix()
        
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



        

