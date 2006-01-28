from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import time
from pygame.locals import *
from testGL.zAPI.zForms import zControl
from testGL.zAPI.zForms import zPictureBox
from testGL.zAPI.zRenderer import zRendererFactory
from testGL.common import constants


class Form(zControl.Control):

    
    def __init__(self, VideoMode='OpenGL'):
        self._ControlCollection = []
        self._SortedControlCollection = []
        self._SortzOderDrawingBool = True
        self.FpsEnable = True
        self._wait = 0
        
        constants._SetForm(self)
        zControl.Control.__init__(self)
        self.SetMaxFps(80)
        self._clock = pygame.time.Clock()
        if constants.GetVideoMode() == 'OpenGL':
            video_flags = OPENGL|DOUBLEBUF
        else:
            video_flags = DOUBLEBUF|HWSURFACE
        pygame.init()
        pygame.display.set_mode(constants.GetWindowSize(), video_flags)
        self._Renderer = zRendererFactory.RendererFactory()
        self._Renderer.init()
        self.SetText("Form")
        
        self._frame = 0
        self._TickStart = pygame.time.get_ticks()
    
    def _GetRenderer(self):
        return self._Renderer
        
    def _SortzOderDrawing(self):
        self._SortzOderDrawingBool = True
                
    def SetBackColor(self, Red, Green, Blue):
        zControl.Control.SetBackColor(self, Red, Green, Blue)
        self._Renderer.SetBackColor(Red, Green, Blue)
    
    def SetBackgroundImageFromFile(self, PathAndFileName, UseAlpha=False):
        self._Renderer.SetBackgroundImageFromFile(PathAndFileName)
        
    #FIXME : not implemented
    def SetLocation(self, x, y): pass
    #FIXME : not implemented
    def GetLocation(self): pass
    #FIXME : not implemented
    def SetSize(self, Width, Height): pass
    #FIXME : not implemented   
    def GetSize(self): pass
       
    def run(self):
            
        self._TickStart = pygame.time.get_ticks()
       
        while 1 :
            if self.Refresh() == False:
                break

        for c in self._ControlCollection:
            c.OnUnload()
            
        self.DisplayStats()    
    
    def Refresh(self):
        StartAt = pygame.time.get_ticks()
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
           return False
        
        if constants.GetVideoMode() == 'OpenGL':
            self._Renderer.ClearScreen()
        
        self.Render()
        
        if constants.GetVideoMode() == 'OpenGL':
            pygame.display.flip()
       
        self._frame = self._frame + 1 
        
        if self.FpsEnable == True:
            self._wait=( (self._MinMsBetweenFrame - (pygame.time.get_ticks() - StartAt))/1000.0 )
            if self._wait >0:
                time.sleep(self._wait)
            else:
                time.sleep(0.001)
            
        return True
    
    def DisplayStats(self):
        es_time = ( (pygame.time.get_ticks() - self._TickStart) / 1000.0 )
        print "fps = ", self._frame / es_time
        print self._frame, " frames in ", es_time, "s, wait=",self._wait
        
    def AddControl(self, ctrl):
        self._ControlCollection.append(ctrl)
        self._SortzOderDrawingBool = True
        ctrl._SetForm(self)
    
    def ReorderControls(self):
        self._SortzOderDrawingBool = True
        
    def RemoveControl(self, ctrl):
        ctrl.OnUnload()
        self._ControlCollection.remove(ctrl)
        self._SortzOderDrawingBool = True
        ctrl._SetForm(None)
        
    def Render(self):
        self.Draw()
        
        if self._SortzOderDrawingBool == True:
            self._SortzOderDrawingBool = False
            self._SortedControlCollection = []
            self._TempDict = {}
            for ctrl in self._ControlCollection:
                z = ctrl.GetLocation()[2]
                if self._TempDict.has_key(z) == True:
                    self._TempDict[z].append(ctrl)
                else:
                    self._TempDict[z] = [ ctrl ]
            
            Zordered = self._TempDict.keys()
            Zordered.sort()
            for z in Zordered:
                self._SortedControlCollection.append(self._TempDict[z])
                
        #print str(len(self._ControlCollection)) + " / sorted : " + str(len(self._SortedControlCollection))
        for control in self._SortedControlCollection:
            if isinstance(control,list) == True:
                for control2 in control:
                    if control2.Visible(): control2.Draw()
            else:
                if control2.Visible(): control.Draw()
            
    def Draw(self):
        self._Renderer.DrawBackground();
        
    def SetMaxFps(self, fps):
        self._MaxFps = fps
        self._MinMsBetweenFrame = 1000/float(fps)
