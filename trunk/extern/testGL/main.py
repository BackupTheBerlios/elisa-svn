#!/usr/bin/env python


from extern.testGL.common import constants
from extern.testGL.zAPI.zForms import zForm
from extern.testGL.zAPI.zForms import zPictureBox
from extern.testGL.zAPI.zForms import zVideo
import time

class MyClass(zForm.Form):

    def __init__(self):
        zForm.Form.__init__(self)        

        self.SetBackColor(1.0, 1.0, 1.0)
        self.SetBackgroundImage("themes/mce/COMMON.BACKGROUND.PNG")
        
        self._ctl = zPictureBox.PictureBox()
        self._ctl.SetSize(300, 40)
        self._ctl.SetText("ctl") 
        self._ctl.SetLocation(120.0, 80.0, 2.0)
        self._ctl.SetBackgroundImage("themes/mce/COMMON.BUTTON.LEFT.FOCUS.PNG", True)
        
        self._ctl2 = zVideo.Video()
        self._ctl2.SetSize(320, 176)
        self._ctl2.SetText("ctl2")
        self._ctl2.SetLocation(0.0, 0.0, 0.0)
        self._ctl2.SetBackColor(255, 255, 255)
        self._ctl2.SetURI("file:///home/yoyo/temp/nemo-fr.avi")
        self._ctl2.Play()
        
        self._ctl3 = zVideo.Video()
        self._ctl3.SetSize(640, 352)
        self._ctl3.SetText("ctl2")
        self._ctl3.SetLocation(100.0, 100.0, 1.0)
        self._ctl3.SetBackColor(255, 255, 255)
        self._ctl3.SetURI("file:///home/yoyo/temp/Le-roi-lion.avi")
        self._ctl3.SetAlpha(150)
        self._ctl3.Play()
        
        self.AddControl(self._ctl)
        self.AddControl(self._ctl2)
        self.AddControl(self._ctl3)
        
    def quit(self):
        self._ctl2.Stop()
        self._ctl3.Stop()
           
if __name__ == '__main__': 

    test = MyClass()
    test.run()
    test.quit()
