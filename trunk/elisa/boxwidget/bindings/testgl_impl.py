from elisa.boxwidget.bindings import base_impl
from elisa.boxwidget.bindings import base_impl
from extern.testGL.zAPI.zForms import zForm, zPictureBox
from elisa.framework.log import Logger

import pygame
from pygame.locals import *

class _testGL_Window_Impl(base_impl._Base_Window_Impl):
    """
    windows binding class for testGL renderEngine
    """

    def __init__(self):
        self._logger = Logger()
        self._logger.debug('_testGL_Window_Impl.__init__()', self)
        self._window_native=zForm.Form()
        self._window_native.FpsEnable = False
        
    def refresh(self):
        self._window_native.Refresh()

    def set_back_color(self, red, green, blue):
        self._window_native.SetBackColor(Red, Green, Blue)

    def set_background_from_file(self, path_and_file_name=None):
        self._window_native.SetBackgroundImageFromFile(path_and_file_name)
        
    def close(self):
        self._window_native.DisplayStats()
     
    def add_surface(self, impl_surface):
        self._logger.debug('_testGL_Window_Impl.add_surface()', self)
        self._window_native.AddControl(impl_surface.get_native_surface())
        #(_tx, _ty, _tz) = in_surface.GetAbsoluteLocation()
        #self._surface_native.SetLocation(_tx, _ty, _tz)

    def remove_surface(self, impl_surface):
        self._window_native.RemoveControl(impl_surface.get_native_surface())


class _testGL_Surface_Impl(base_impl._Base_Surface_Impl):

    def __init__(self):
        self._logger = Logger()
        self._logger.debug('_testGL_Surface_Impl.__init__()', self)
        self._surface_native = zPictureBox.PictureBox()
    
    def get_native_surface(self):
        return self._surface_native       
        
    def set_size(self, Width, Height):  
        self._surface_native.SetSize(Width, Height)
        
    def set_location(self, x, y, z):
        self._surface_native.SetLocation( x, y, z)
    
    def set_back_color(self, Red, Green, Blue):
        self._surface_native.SetBackColor(Red, Green, Blue)

    def set_background_from_file(self, path_and_filename=None):
        self._surface_native.SetBackgroundImageFromFile(path_and_filename, True)
        
    def set_alpha_level(self, level):
        self._surface_native.SetAlpha(level*2.55)
        
    def hide(self):
        self._logger.debug('_testGL_Surface_Impl.hide()', self)
        self._surface_native.Hide()

    def show(self):
        self._surface_native.Show()  

class _testGL_EventsManager_Impl(object):

    def __init__(self, push_event_function):
        self._push_event_function = push_event_function
        
    def get_event_queue(self):
        for event in pygame.event.get():
            _boxevent = self.pygame_event_converter(event)
            if _boxevent != None:
                self._push_event_function(_boxevent)
        
        return eventsmanagerbase._EventsManagerBase.GetEventQueue(self)
            
    def pygame_event_converter(self, pyevent):
    
        if pyevent.type == pygame.QUIT:   
            return event.Event(event.DEV_SYSTEM, event.EVENT_QUIT, event.SE_QUIT)
        if pyevent.type == pygame.KEYDOWN:
            if pyevent.key == pygame.K_LEFT:
                return event.Event(event.DEV_KEYBOARD, event.KEY_LEFT, event.SE_LEFT)
            if pyevent.key == pygame.K_RIGHT:
                return event.Event(event.DEV_KEYBOARD, event.KEY_RIGHT, event.SE_RIGHT)
            if pyevent.key == pygame.K_UP:
                return event.Event(event.DEV_KEYBOARD, event.KEY_UP, event.SE_UP)
            if pyevent.key == pygame.K_DOWN:
                return event.Event(event.DEV_KEYBOARD, event.KEY_DOWN, event.SE_DOWN)
            if pyevent.key == pygame.K_RETURN:
                return event.Event(event.DEV_KEYBOARD, event.KEY_RETURN, event.SE_OK)
            if pyevent.key == pygame.K_SPACE:
                return event.Event(event.DEV_KEYBOARD, event.KEY_SPACE, event.SE_MENU)
            if pyevent.key == pygame.K_ESCAPE:
                return event.Event(event.DEV_KEYBOARD, event.KEY_ESCAPE, event.SE_QUIT)
                
        return None
