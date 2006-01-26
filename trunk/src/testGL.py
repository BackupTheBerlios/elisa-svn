#!/usr/bin/env python

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
        self.SetBackgroundImage("testGL/themes/mce/COMMON.BACKGROUND.PNG")
        
        self._font = zFont.Font("Super MediaBox : test de police !!!! longue ligne")
        self._font.SetSize(500, 80)
        self._font.SetText("ctl") 
        self._font.SetLocation(120.0, 480.0, 2.0)
        
        self._font2 = zFont.Font("12345TGFDS234TYHKUJYTHRGFDVT5RG")
        self._font2.SetSize(500, 80)
        self._font2.SetText("ctl") 
        self._font2.SetLocation(120.0, 280.0, 2.0)
        
      
        self.AddControl(self._font)
        self.AddControl(self._font2)
    
        Video = False    
        if Video == True:
            self._ctl2 = zVideo.Video()
            self._ctl2.SetSize(320, 176)
            self._ctl2.SetText("ctl2")
            self._ctl2.SetLocation(0.0, 0.0, 0.0)
            self._ctl2.SetBackColor(255, 255, 255)
            self._ctl2.SetURI("file:///home/yoyo/temp/nemo-fr.avi")
            self._ctl2.Play()
            self.AddControl(self._ctl2)
           
if __name__ == '__main__': 
    
    test = MyClass()
    profile.run('test.run()','test.profile')    
    pstats.Stats('test.profile').sort_stats('time').print_stats()

