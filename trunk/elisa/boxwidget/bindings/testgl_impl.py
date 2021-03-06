from elisa.boxwidget import events
from elisa.boxwidget.bindings import base_impl
from extern.testGL.zAPI.zForms import zForm, zPictureBox, zFont
from extern.testGL.zAPI.zRenderer import zOpenGLTexture
from elisa.framework.log import Logger
from OpenGL.GL import *
from OpenGL.GLU import *

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

    def set_back_color(self, Red, Green, Blue):
        self._window_native.SetBackColor(Red, Green, Blue)

    def set_texture(self, impl_texture):
        self._window_native.SetTexture(impl_texture.get_native_surface()) 
        
    def set_background_from_buffer(self, buffer, width, height, flip = False):
        self._window_native.SetBackgroundImageFromBuffer(buffer, width, height, Flip=flip)
        
    def close(self):
        self._window_native.DisplayStats()
     
    def add_surface(self, impl_surface):
        self._logger.debug('_testGL_Window_Impl.add_surface()', self)
        self._window_native.AddControl(impl_surface.get_native_surface())
        
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
        
    def set_alpha_level(self, level):
        self._surface_native.SetAlpha(level*2.55)
        
    def hide(self):
        self._logger.debug('_testGL_Surface_Impl.hide()', self)
        self._surface_native.Hide()

    def show(self):
        self._surface_native.Show()
        
    def set_background_from_buffer(self, buffer, width, height, flip = False):
        self._surface_native.SetBackgroundImageFromBuffer(buffer, width, height, Flip=flip)

    def set_texture(self, impl_texture):
        self._surface_native.SetTexture(impl_texture.get_native_surface())
    
class _testGL_EventsManager_Impl(base_impl._Base_EventsManager_Impl):

    def __init__(self):
        self._logger = Logger()
        self._logger.debug('_testGL_EventsManager_Impl.__init__()', self)

    def process_input_events(self):
        events = []
        for pyevent in pygame.event.get():
            _boxevent = self.pygame_event_converter(pyevent)
            if _boxevent != None:
                events.append(_boxevent)
        return events
            
    def pygame_event_converter(self, pyevent):
    
        self._logger.debug_verbose  ('_testGL_EventsManager_Impl.pygame_event_converter()', self)
        if pyevent.type == pygame.QUIT:   
            return events.InputEvent(events.DEV_SYSTEM, events.EVENT_QUIT, events.SE_QUIT)
        if pyevent.type == pygame.KEYDOWN:
            if pyevent.key == pygame.K_LEFT:
                return events.InputEvent(events.DEV_KEYBOARD, events.KEY_LEFT, events.SE_LEFT)
            if pyevent.key == pygame.K_RIGHT:
                return events.InputEvent(events.DEV_KEYBOARD, events.KEY_RIGHT, events.SE_RIGHT)
            if pyevent.key == pygame.K_UP:
                return events.InputEvent(events.DEV_KEYBOARD, events.KEY_UP, events.SE_UP)
            if pyevent.key == pygame.K_DOWN:
                return events.InputEvent(events.DEV_KEYBOARD, events.KEY_DOWN, events.SE_DOWN)
            if pyevent.key == pygame.K_RETURN:
                return events.InputEvent(events.DEV_KEYBOARD, events.KEY_RETURN, events.SE_OK)
            if pyevent.key == pygame.K_SPACE:
                return events.InputEvent(events.DEV_KEYBOARD, events.KEY_SPACE, events.SE_MENU)
            if pyevent.key == pygame.K_ESCAPE:
                return events.InputEvent(events.DEV_KEYBOARD, events.KEY_ESCAPE, events.SE_QUIT)
            if pyevent.key == pygame.K_BACKSPACE:
                return events.InputEvent(events.DEV_KEYBOARD, events.KEY_BACKSPACE, events.SE_BACK)
                
        return None

class _testGL_Font_Impl(base_impl._Base_Font_Impl):

    def __init__(self, text='text'):
        self._logger = Logger()
        self._logger.debug('_testGL_Surface_Impl.__init__(' + str(text) + ')', self)
        self._surface_native = zFont.Font(text)
    
    def get_native_surface(self):
        return self._surface_native       
        
    def set_size(self, Width, Height):  
        self._surface_native.SetSize(Width, Height)
        
    def get_size(self):
        return self._surface_native.GetSize()
        
    def set_location(self, x, y, z):
        self._surface_native.SetLocation( x, y, z)
        
    def set_back_color(self, Red, Green, Blue):
        self._surface_native.SetBackColor(Red, Green, Blue)
        
    def set_alpha_level(self, level):
        self._surface_native.SetAlpha(level*2.55)
        
    def hide(self):
        self._logger.debug('_testGL_Surface_Impl.hide()', self)
        self._surface_native.Hide()

    def show(self):
        self._surface_native.Show()   
        
    def set_font_size(self, size):
        self._surface_native.SetFontSize(size)
        
    def set_text(self, text):
        self._surface_native.SetText(text)
        
class _testGL_Texture_Impl(object):

    def __init__(self):
        self._logger = Logger()
        self._logger.debug('_testGL_Texture_Impl.__init__()', self)
        
        self._surface_native = zOpenGLTexture.OpenGLTexture()
    
    def init_texture(self, width, height, buffer=None, use_alpha=False):
        if use_alpha == True:
            _format = GL_RGBA
        else:
            _format = GL_RGB
        self._surface_native.init_texture(width, height, _format, buffer)
        
    def get_native_surface(self):
        return self._surface_native       
                       
    def set_buffer(self, buffer):
        self._surface_native.set_buffer(buffer)
        
    def set_flip_buffer(self, flip):
        self._surface_native.set_flip_buffer(flip)
        
    def get_size(self):
        return self._surface_native.get_size()
        
    def set_aspect_ratio(self, respect_aspect_ratio):
        self._surface_native.apply_aspect_ratio(respect_aspect_ratio)
