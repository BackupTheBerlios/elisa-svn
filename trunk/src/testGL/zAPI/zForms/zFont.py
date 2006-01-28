from testGL.zAPI.zForms import zPictureBox
from pygame.font import *
from pygame import *

class Font(zPictureBox.PictureBox):

    def __init__(self, in_text = "font"):
        zPictureBox.PictureBox.__init__(self)
        font.init()
        if not font.get_init():
            print 'Could not render font.'
            sys.exit(0)
        self._font = font.Font('testGL/common/font.ttf',72)
        self._texture = None
        self._fontsize = 32
        self.SetText(in_text)
    
    def TextureFromString(self, s):        
        try:
            letter_render = self._font.render(s, 1, (255,255,255))
            letter = image.tostring(letter_render, 'RGBA', 1)
            letter_w, letter_h = letter_render.get_size()
        except:
            print 'Could not render font.(2)'
            letter = None
            letter_w = 0
            letter_h = 0
        return (letter, letter_w, letter_h)
   
    def SetFontSize(self, in_size):
        self._fontsize = in_size
        self._SetFontText(self.GetText())

    def GetFontSize(self):
        return self._fontsize
                        
    def _SetFontText(self, s):
        if s != "":
            self._texture = self.TextureFromString(s)
            (_buffer, _width, _height) = self._texture
            self.SetBackgroundImageFromBuffer(_buffer, _width, _height, True, False)
            self.SetSize(self._fontsize * _width/float(_height),self._fontsize)

    def SetText(self, in_text):
        zPictureBox.PictureBox.SetText(self, in_text)
        self._SetFontText(in_text)
