#!/usr/bin/env python
#
# TEST APPLICATION FOR zForm API
#

from pygame.locals import *
from pygame.display import *
from pygame.event import *
from pygame.key import *
from pygame.font import *
from pygame.image import *
from pygame.time import *
from pygame import *
from testGL.common import constants
from testGL.zAPI.zForms import zForm
from testGL.zAPI.zForms import zPictureBox
from testGL.zAPI.zForms import zFont
from testGL.zAPI.zForms import zVideo
import time
import profile
import pstats
    
class MyClass(zForm.Form):

    def __init__(self):
        zForm.Form.__init__(self)        

        self.SetBackColor(1.0, 1.0, 1.0)
        self.SetBackgroundImageFromFile("testGL/themes/mce/COMMON.BACKGROUND.PNG")
        
        #FIXME : FONT + VIDEO IS VERY SLOW
        #self._font = zFont.Font("very slow with long text !!! to fix")
        #self._font.SetSize(500, 80)
        #self._font.SetText("ctl") 
        #self._font.SetLocation(120.0, 480.0, 2.0)
        #self.AddControl(self._font)
        
        self._font2 = zFont.Font("text test")
        self._font2.SetSize(200, 80)
        self._font2.SetText("ctl") 
        self._font2.SetLocation(120.0, 280.0, 2.0)  
        self.AddControl(self._font2)

        self._ctl2 = zVideo.Video()
        self._ctl2.SetSize(320, 176)
        self._ctl2.SetText("ctl2")
        self._ctl2.SetLocation(0.0, 0.0, 0.0)
        self._ctl2.SetBackColor(255, 255, 255)
        self._ctl2.SetURI("file:///home/yoyo/temp/nemo-fr.avi")
        self._ctl2.Play()
        self.AddControl(self._ctl2)
        
        self._ctl = zPictureBox.PictureBox()
        self._ctl.SetSize(300, 40)
        self._ctl.SetText("ctl")
        self._ctl.SetLocation(120.0, 80.0, 2.0)
        self._ctl.SetBackgroundImageFromFile("testGL/themes/mce/COMMON.BUTTON.LEFT.FOCUS.PNG", True)
        self.AddControl(self._ctl)

        self._ctl3 = zVideo.Video()
        self._ctl3.SetSize(640, 352)
        self._ctl3.SetText("ctl2")
        self._ctl3.SetLocation(100.0, 100.0, 1.0)
        self._ctl3.SetBackColor(255, 255, 255)
        self._ctl3.SetURI("file:///home/yoyo/temp/Le-roi-lion.avi")
        self._ctl3.SetAlpha(150)
        self._ctl3.Play()
        self.AddControl(self._ctl3)

        
           
if __name__ == '__main__': 
    
    test = MyClass()
    profile.run('test.run()','test.profile')    
    pstats.Stats('test.profile').sort_stats('time').print_stats()

