from testGL.zAPI.zForms import zPictureBox
from pygame.locals import *
from pygame.display import *
from pygame.event import *
from pygame.key import *
from pygame.font import *
from pygame.image import *
from pygame.time import *
from pygame import *

class Font(zPictureBox.PictureBox):

    def __init__(self, text = ""):
        zPictureBox.PictureBox.__init__(self)
        
        font.init()
        if not font.get_init():
            print 'Could not render font.'
            sys.exit(0)
        self._font = font.Font('testGL/common/font.ttf',72)
        self._texture = None
        if text != "": self.SetFontText(text)
    
    def TextureFromString(self, s):        
        try:
            letter_render = self._font.render(s, 1, (255,255,255))
            letter = image.tostring(letter_render, 'RGBA', 1)
            letter_w, letter_h = letter_render.get_size()
        except:
            print "marche po"
            letter = None
            letter_w = 0
            letter_h = 0
        return (letter, letter_w, letter_h)
        
    def SetFontText(self, s):
        if s != "":
            self._texture = self.TextureFromString(s)
            print len(self._texture[0])
            (_buffer, _width, _height) = self._texture
            self.SetBackgroundImageFromBuffer(_buffer, _width, _height, True)
