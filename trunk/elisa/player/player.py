
import pygst
pygst.require('0.10')
import gst
import gobject, sys, time
from mutex import mutex
from elisa.utils import event_dispatcher
from elisa.player import events

_player_manager = None

class _PlayerManager(event_dispatcher.EventDispatcher):

    def __init__(self):
        self.players = []

    def add_player(self, player):
        self.players.append(player)
        self.fire_event(events.NewPlayerEvent(player))
        
    def fullscreen(self, player):
        for p in self.players:
            if p != player and p.get_state() == p.PLAYING:
                p.save()
                p.stop()
        player.fullscreen()

                
def PlayerManager():
    global _player_manager
    if not _player_manager:
        _player_manager = _PlayerManager()
    return _player_manager

VIDEO_CAPS="video/x-raw-rgb,bpp=24,depth=24"

# unused
AUDIO_CAPS="audio/x-raw-int,rate=44100"

class Player(event_dispatcher.EventDispatcher):

    PLAYING = gst.STATE_PLAYING
    PAUSED = gst.STATE_PAUSED
    STOPPED = gst.STATE_READY

    def __init__(self, uri=''):
        self._uri = uri
        self._queue = []
        self._current_item_index = -1
        self._saved_item_index = None
        self._saved_status = None
        self._g_timeout_id = None
        self._playbin = gst.element_factory_make('playbin', 'playbin')

        bus = self._playbin.get_bus()
        bus.add_signal_watch()
        bus.connect('message', self.on_message)

        caps = VIDEO_CAPS
        #caps = AUDIO_CAPS
        
        self._sink = VideoSinkBin(caps)
        #self._playbin.set_property("video-sink", self._sink)
        
        self._videowidth = None
        self._videoheight = None   

        if self._uri:
            self.add_playable(Playable(self._uri))
            self.next()

    def idle(self):
        position, duration = self.get_status()

        current_item = self.get_current_item()
        current_item.set_length(duration)
        current_item.set_status(position)

        ###################################################
        # TODO: disable this when integrated in boxwidget
        current_item.print_status()

        if position == 5:
            self.seek_forward(10)
##         elif position == 20:
##             #self.seek_backward(19)
##             self.save()
##         elif position == 30:
##             self.load()

##         print self.get_video_width()

        if position == 30 and self._current_item_index == 0:
            self.next()
        elif position == 25 and self._current_item_index == 1:
            self.previous()

        ###################################################
            
        time.sleep(0.1)
        sys.stdout.flush()
        return True

    def on_message(self, bus, msg, extra=None):
        #print bus, msg
        return True

    def get_id(self):
        return id(self)

    def get_video_width(self):
        return self._sink.get_width()

    def get_video_height(self):
        return self._sink.get_height()
            
    def play_uri(self, uri):
        self.stop()
        self._playbin.set_property('uri', uri)
        self.play()
        if self._g_timeout_id:
            gobject.source_remove(self._g_timeout_id)
        self._g_timeout_id = gobject.timeout_add(1, self.idle)

    def play(self):
        self._playbin.set_state(gst.STATE_PLAYING)
        self.fire_event(events.PlayingEvent(self.get_current_item()))
        
    def pause(self):
        self._playbin.set_state(gst.STATE_PAUSED)
        self.fire_event(events.PausedEvent())

    def stop(self):
        self._playbin.set_state(gst.STATE_READY)

    def seek_forward(self, seconds):
        playable = self.get_current_item()
        new_location = playable.get_status() + seconds
        if new_location <= playable.get_length():
            self.seek_to_location(new_location)
            
    def seek_backward(self, seconds):
        playable = self.get_current_item()
        new_location = playable.get_status() - seconds
        if new_location > 0:
            self.seek_to_location(new_location)
        
    def seek_to_location(self, location):
        """
        @param location: time to seek to, in nanoseconds
        """
        print "seeking to %s" % location
        location *= gst.SECOND
        event = self._playbin.seek(1.0, gst.FORMAT_TIME,
                                   gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
                                   gst.SEEK_TYPE_SET, location,
                                   gst.SEEK_TYPE_NONE, 0)

    def save(self):
        print 'saving'
        self._saved_item_index = self._current_item_index
        self._saved_status = self.get_status()

    def load(self):
        if self._saved_item_index >= 0 and self._saved_status:
            print 'loading'
            self._current_item_index = self._saved_item_index
            item = self._queue[self._current_item_index]
            self.play_uri(item.get_uri())
            position, duration = self._saved_status
            self.seek_to_location(position)
            self._saved_item_index = None
            self._saved_status = None
            
    def add_playable(self, playable):
        self._queue.append(playable)

    def remove_playable_with_id_from_queue(self, playable_id):
        for playable in self._queue:
            if playable.get_id() == playable_id:
                self._queue.remove(playable)
                break

    def next(self):
        new_index = self._current_item_index + 1
        try:
            new_item = self._queue[new_index]
        except IndexError:
            print self._queue
            raise IndexError, "end of queue reached"
        else:
            print new_item
            self._current_item_index = new_index
            self.play_uri(new_item.get_uri())

    def previous(self):
        new_index = self._current_item_index - 1
        if new_index < 0:
            raise IndexError, "can't go prior to the first queue's item"
        new_item = self._queue[new_index]
        self._current_item_index = new_index
        self.play_uri(new_item.get_uri())

    def get_current_item(self):
        return self._queue[self._current_item_index]

    def get_status(self):
        "Returns a (position, duration) tuple"
        try:
            position, format = self._playbin.query_position(gst.FORMAT_TIME)
            position /= gst.SECOND
        except:
            position = gst.CLOCK_TIME_NONE

        try:
            duration, format = self._playbin.query_duration(gst.FORMAT_TIME)
            duration /= gst.SECOND
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
      
    """

    def __init__(self, uri, name="playable", contains_audio=True,
                 contains_video=True, length=-1):
        self._uri = uri
        self._name = name
        self._contains_audio = contains_audio
        self._contains_video = contains_video
        self.set_status(0)
        self.set_length(length)
        
    def __repr__(self):
        return "%s (%s)" % (self.get_name(), self.get_uri())
        
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
    
    def set_length(self, length):
        self._length = length

    def print_status(self):
        position = self.get_status()
        duration = self.get_length()
        if position != gst.CLOCK_TIME_NONE:
            status = "%02d:%02d / %02d:%02d" % (position / 60, position % 60,
                                                duration / 60, duration % 60)
            print '\r %s (%s)' % (status,self.get_uri()),


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

    def on_play(event):
        print 'start playing : %s' % event

    """
    for uri in sys.argv[1:]:
    
        p = Player(uri)
        p.register('player.playing', on_play)
        manager.add_player(p)
        p.play()
    """

    p = Player()
    p.register('player.playing', on_play)
    manager.add_player(p)
    
    for uri in sys.argv[1:]:
        p.add_playable(Playable(uri))


    p.next()
    
    mainloop.run()
