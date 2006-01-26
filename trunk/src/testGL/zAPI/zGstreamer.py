#export GST_DEBUG=pygst:5
#ulimit -c unlimited
import sys
import pygst
pygst.require('0.10')
import gst, gobject, time
from mutex import mutex

class GstPlayer(object):

    def __init__(self,caps):

        self._MySink = SinkBin(caps)
        self._playbin = gst.element_factory_make('playbin', 'playbin')
        self._playbin.set_property("video-sink", self._MySink)
        self._videowidth = None
        self._videoheight = None   
         
    def SetURI(self, location):
        self._playbin.set_property('uri', location)
        
    def Pause(self):
        gst.info("pausing player")
        self._playbin.set_state(gst.STATE_PAUSED)

    def Play(self):
        gst.info("playing player")
        self._playbin.set_state(gst.STATE_PLAYING)
        
    def Stop(self):
        gst.info("stopping player")
        self._playbin.set_state(gst.STATE_READY)
        gst.info("stopped player")

    def GetState(self, timeout=1):
        return self._playbin.get_state(timeout=timeout)
        
    def GetVideoHeight(self):
        return self._MySink.GetHeight()
        
    def GetVideoWidth(self):
        return self._MySink.GetWidth()
    
    def GetVideoSize(self):
        return self._MySink.GetWidth(), self._MySink.GetHeight()
    
    def GetCurrentFrame(self):
        return self._MySink.GetCurrentFrame()

    def SetCaps(self, caps):
        self._MySink.SetCaps(caps)
        
        
################################################################################

class SinkBin(gst.Bin):

    def __init__(self, needed_caps):
        self._width = None
        self._height = None
        self._CurrentFrame = None
        gobject.threads_init()
        self._mutex = mutex()
        gst.Bin.__init__(self)
        self._capsfilter = gst.element_factory_make ("capsfilter", "capsfilter")
        caps = gst.caps_from_string(needed_caps)                                     
        self._capsfilter.set_property("caps",caps)
        self.add(self._capsfilter)
        
        fakesink = gst.element_factory_make('fakesink','fakesink')
        fakesink.set_property("sync",True)
        self.add(fakesink)
        self._capsfilter.link(fakesink)
        
        pad = self._capsfilter.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        
        pad2probe = fakesink.get_pad("sink")
        pad2probe.add_buffer_probe(self.buffer_probe)

        self.add_pad(ghostpad)
        self.sink = self._capsfilter

    def _SetCurrentFrame(self, value):
        self._mutex.testandset()
        self._CurrentFrame = value
        self._mutex.unlock()
    
    def SetCaps(self, caps):
        GstCaps = gst.caps_from_string(caps) 
        self._capsfilter.set_property("caps",GstCaps)
        
    def GetCurrentFrame(self):
        self._mutex.testandset()
        frame = self._CurrentFrame
        self._CurrentFrame = None
        self._mutex.unlock()
        return frame
        
    def buffer_probe(self, pad, buffer):
        if self._width == None or self._height == None:
            caps = pad.get_negotiated_caps()
            if caps != None:
                s = caps[0]
                self._width = s['width']
                self._height = s['height']
        if self._width != None and self._height != None:
            self._SetCurrentFrame(buffer)
        return True
        
    def GetHeight(self):
        return self._height
        
    def GetWidth(self):
        return self._width
            
gobject.type_register(SinkBin)    
