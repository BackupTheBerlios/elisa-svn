
import pygst
pygst.require('0.10')
import gst
import gobject, sys
from mutex import mutex

_player_manager = None

class _PlayerManager:

    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def fullscreen(self, player):
        for p in self.players:
            if p != player and p.get_state() == gst.STATE_PLAYING:
                p.save()
                p.stop()
        player.fullscreen()
                

    def play(self, player_id=None):
        if not player_id:
            

def PlayerManager():
    global _player_manager
    if not _player_manager:
        _player_manager = _PlayerManager()
    return _player_manager

VIDEO_CAPS="video/x-raw-rgb,bpp=24,depth=24"

# unused
AUDIO_CAPS="audio/x-raw-int,rate=44100"

class Player:

    def __init__(self, uri=''):
        self._uri = uri
        self._queue = []
        self._current_item_index = -1
        self._saved_item_index = None
        self._saved_status = None


        self._playbin = gst.element_factory_make('playbin', 'playbin')

        caps = VIDEO_CAPS
        #caps = AUDIO_CAPS
        
        self._sink = VideoSinkBin(caps)
        self._playbin.set_property("video-sink", self._sink)
        
        self._videowidth = None
        self._videoheight = None   

        if self._uri:
            self.add_to_queue(Playable(self._uri))
            self.next()

    def get_id(self):
        return id(self)
            
    def play_uri(self, uri):
        self._playbin.set_property('uri', uri)
        self.play()

    def play(self):
        self._playbin.set_state(gst.STATE_PLAYING)

    def pause(self):
        self._playbin.set_state(gst.STATE_PAUSED)

    def stop(self):
        self._playbin.set_state(gst.STATE_READY)

    def seek(self, location):
        """
        @param location: time to seek to, in nanoseconds
        """
        gst.debug("seeking to %r" % location)
        event = gst.event_new_seek(1.0, gst.FORMAT_TIME,
                                   gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
                                   gst.SEEK_TYPE_SET, location,
                                   gst.SEEK_TYPE_NONE, 0)

        res = self._playbin.send_event(event)
        if res:
            gst.info("setting new stream time to 0")
            self._playbin.set_new_stream_time(0L)
        else:
            gst.error("seek to %r failed" % location)

    def save(self):
        self._saved_item_index = self._current_item_index
        self._saved_status = self.get_status()

    def load(self):
        if self._saved_item_index and self._saved_status:
            item = self._queue[self._saved_item_index]
            self.play_uri(item.get_uri())
            # TODO: set_status() on the item
            
    def add_to_queue(self, playable):
        self._queue.append(playable)

    def remove_playable_with_id_from_queue(self, playable_id):
        pass

    def next(self):
        new_index = self._current_item_index + 1
        try:
            new_item = self._queue[new_index]
        except IndexError:
            print self._queue
            raise IndexError, "end of queue reached"
        else:
            self.play_uri(new_item.get_uri())
            self._current_item_index = new_index

    def previous(self):
        new_index = self._current_item_index - 1
        if new_index < 0:
            raise IndexError, "can't go prior to the first queue's item"
        new_item = self._queue[new_index]
        self.play_uri(new_item.get_uri())
        self._current_item_index = new_index

    def get_current_item(self):
        return self._queue[self._current_item_index]

    def get_status(self):
        "Returns a (position, duration) tuple"
        try:
            position, format = self._playbin.query_position(gst.FORMAT_TIME)
        except:
            position = gst.CLOCK_TIME_NONE

        try:
            duration, format = self._playbin.query_duration(gst.FORMAT_TIME)
        except:
            duration = gst.CLOCK_TIME_NONE

        return (position, duration)

    def get_state(self):
        return self._playbin.get_state()

    def fullscreen(self):
        " should be implemented by SurfacePlayer "

class Playable:

    """
    TODO:

    - fill infos in:
      * audio capabilities
      * video capabilities
      * length
    - somehow setup a callback system to call:
      * set_status()
      during playback via the player
      
    """

    def __init__(self, uri, name="playable", contains_audio=True,
                 contains_video=True, length=-1):
        self._uri = uri
        self._name = name
        self._contains_audio = contains_audio
        self._contains_video = contains_video
        self._length = length
        self.set_status(0)
        
    def get_id(self):
        return id(self)

    def get_name(self):
        return self._name

    def get_uri(self):
        return self._uri

    def contains_audio(self):
        return self._contains_audio

    def contains_video(self):
        return self._contains_video

    def set_status(self, status):
        self._status = status

    def get_status(self):
        return self._status

    def get_length(self):
        return self._length
    

class VideoSinkBin(gst.Bin):

    def __init__(self, needed_caps):
        self._width = None
        self._height = None
        self._current_frame = None
        gobject.threads_init()
        self._mutex = mutex()
        gst.Bin.__init__(self)
        self._capsfilter = gst.element_factory_make("capsfilter", "capsfilter")

        self.set_caps(needed_caps)
        self.add(self._capsfilter)
        
        fakesink = gst.element_factory_make('fakesink','fakesink')
        fakesink.set_property("sync", True)
        self.add(fakesink)
        self._capsfilter.link(fakesink)
        
        pad = self._capsfilter.get_pad("sink")
        ghostpad = gst.GhostPad("sink", pad)
        
        pad2probe = fakesink.get_pad("sink")
        pad2probe.add_buffer_probe(self.buffer_probe)

        self.add_pad(ghostpad)
        self.sink = self._capsfilter

    def set_current_frame(self, value):
        self._mutex.testandset()
        self._current_frame = value
        self._mutex.unlock()
    
    def set_caps(self, caps):
        gst_caps = gst.caps_from_string(caps) 
        self._capsfilter.set_property("caps", gst_caps)
        
    def get_current_frame(self):
        self._mutex.testandset()
        frame = self._current_frame
        self._current_frame = None
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
            self.set_current_frame(buffer)
        return True
        
    def get_height(self):
        return self._height
        
    def get_width(self):
        return self._width
            
gobject.type_register(VideoSinkBin)    


if __name__ == '__main__':
    manager = PlayerManager()
    mainloop = gobject.MainLoop()

    uri = sys.argv[-1]
    
    p = Player(uri)
    manager.add_player(p)
    p.play()

    mainloop.run()
