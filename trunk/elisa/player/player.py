
import pygst
pygst.require('0.10')
import gst
import gobject, sys, os
from mutex import mutex
from elisa.boxwidget import texture

# XXX: this is crap
try:
    from elisa.framework.message_bus import MessageBus
except ImportError:
    sys.path.append(os.path.abspath("%s/../../.." % __file__))
    from elisa.framework.message_bus import MessageBus

from elisa.player import events
from elisa.framework import log

_player_manager = None

class _PlayerManager:

    """
    TODO:

    - more player management methods
      * resume(player)
      * ...
    - more events!
      
    """

    def __init__(self):
        self.players = []
        self.get_bus().register(self, self.on_message)

    def get_bus(self):
        return MessageBus()

    def on_message(self, receiver, message, sender):
        return True
        
    def add_player(self, player):
        self.players.append(player)
        self.get_bus().send_message(events.NewPlayerEvent(player))
        
    def fullscreen(self, player):
        """ Switch the player to fullscreen mode and suspend all other players.
        """
        for p in self.players:
            if p != player and p.get_state() == p.PLAYING:
                p.save()
                p.stop()
        player.fullscreen()

    def refresh(self):
        for p in self.players:
            p.refresh()
            
    def get_player(self, uri):
        for p in self.players:
            if p.get_uri() == uri:
                return p
        new_p = Player(uri)
        self.add_player(new_p)
        return new_p

    def uri_is_attached(self, uri):
        for p in self.players:
            if p.get_uri() == uri:
                return True
        return False
                               
def PlayerManager():
    global _player_manager
    if not _player_manager:
        _player_manager = _PlayerManager()
    return _player_manager

VIDEO_CAPS="video/x-raw-rgb,bpp=24,depth=24"

class Player:

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
        self._texture = texture.Texture()
        self._texture.set_flip_buffer(True)

        gst_bus = self._playbin.get_bus()
        gst_bus.add_signal_watch()
        gst_bus.connect('message', self.on_message)

        self.get_bus().register(self, self.on_elisa_message)

        caps = VIDEO_CAPS
        
        self._sink = VideoSinkBin(caps)
        self._playbin.set_property("video-sink", self._sink)

        if self._uri:
            self.set_uri(self._uri)

    def get_texture(self):
        return self._texture
        
    def get_bus(self):
        return MessageBus()

    def refresh(self):
        """ Used to update the current playing item status, lenght and
        capabilities.
        """
        position, duration = self.get_status()

        current_item = self.get_current_item()
        current_item.set_length(duration)
        current_item.set_status(position)

        #current_item.print_status()

        if self._texture.is_init()==False:
             (width, height) = (self.get_video_width(), self.get_video_height() )
             if width != None and height != None:
                self._texture.init_texture(width, height)
                
        if self._texture.is_init()==True:
            frame = self.get_current_frame()
            if frame != None:
                self._texture.set_buffer(frame)
        return True

    def on_message(self, bus, message, extra=None):
        """ Callback used by Gstreamer messaging system
        """
        t = message.type
        if t == gst.MESSAGE_ERROR:
            err, debug = message.parse_error()
            print "Error: %s" % err, debug
            if self.on_eos:
                self.on_eos()
        elif t == gst.MESSAGE_EOS:
            if self.on_eos:
                self.on_eos()

    def on_elisa_message(self, receiver, message, sender):
        if isinstance(message, events.PlayerEvent):
            logger = log.Logger()
            logger.debug("Got message from player")
            #print message
        return True

    def on_eos(self):
        try:
            self.next()
        except IndexError:
            self.stop()

    def close(self):
        self._playbin.set_state(gst.STATE_NULL)

    def get_current_frame(self):
        return self._sink.get_current_frame()
            
    def get_id(self):
        """ Return the player id as an integer
        """
        return id(self)

    def get_video_width(self):
        """ Return the width of the playing video. If we're playing
        non-video data, return None.
        """
        return self._sink.get_width()

    def get_video_height(self):
        """ Return the width of the playing video. If we're playing
        non-video data, return None.
        """
        return self._sink.get_height()

    def get_uri(self):
        return self._uri
                    
    def set_uri(self, uri):
        """ Play the media identified by its uri string
        """
        self._uri = uri
        # stop the player
        self.stop()

        # reset the sink
        self._sink.set_width(None)
        self._sink.set_height(None)

        # TODO: detect whether file is local or remote
        if not uri.startswith('file://'):
            uri = "file://%s" % uri

        # play the new uri
        self._playbin.set_property('uri', uri)
        print uri

        self.add_playable(Playable(uri))

    def play_uri(self, uri):
        self.set_uri(uri)
        self.play()
        
    def play(self):
        """ Set the player state to playing mode and fire a Playing
        event holding the current playing item of the queue.
        """
        self._playbin.set_state(gst.STATE_PLAYING)
        self.get_bus().send_message(events.PlayingEvent(self.get_current_item()))
        
    def pause(self):
        """ Set the player state to paused mode and fire a Paused
        event holding the current playing item of the queue.
        """
        self._playbin.set_state(gst.STATE_PAUSED)
        self.get_bus().send_message(events.PausedEvent(self.get_current_item()))

    def stop(self):
        """ Set the player state to stopped mode and fire a Stopped
        event.
        """
        if self._g_timeout_id:
            gobject.source_remove(self._g_timeout_id)
        self._playbin.set_state(gst.STATE_READY)
        self.get_bus().send_message(events.StoppedEvent())

    def seek_forward(self, seconds):
        """ Seek the current playing item some seconds
        forward. Seconds are supplied as integers. If the resulting
        location is valid within the playing item's length, the seek is
        performed. Otherwise, nothing happens.
        """
        playable = self.get_current_item()
        new_location = playable.get_status() + seconds
        if new_location <= playable.get_length():
            self.seek_to_location(new_location)
            
    def seek_backward(self, seconds):
        """ Seek the current playing item some seconds
        backward. Seconds are supplied as integers. If the resulting
        location is valid, the seek is performed. Otherwise, nothing
        happens.
        """
        playable = self.get_current_item()
        new_location = playable.get_status() - seconds
        if new_location > 0:
            self.seek_to_location(new_location)
        
    def seek_to_location(self, location):
        """ Seek to an absolute location in the current playing item.
        @param location: time to seek to, in seconds
        """
        location *= gst.SECOND
        event = self._playbin.seek(1.0, gst.FORMAT_TIME,
                                   gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
                                   gst.SEEK_TYPE_SET, location,
                                   gst.SEEK_TYPE_NONE, 0)

    def save(self):
        """ Store informations about the current playing item in some
        instance variables:

        - _saved_item_index : current position of the playing queue
        - _saved_status : playing position of the current playing item
        """
        self._saved_item_index = self._current_item_index
        self._saved_status = self.get_status()

    def load(self):
        """ Fetch saved states of the player and restore them. See
        save() method to know about saved/restored informations.
        """
        if self._saved_item_index >= 0 and self._saved_status:
            self._current_item_index = self._saved_item_index
            item = self._queue[self._current_item_index]
            self.play_uri(item.get_uri())
            position, duration = self._saved_status
            self.seek_to_location(position)
            self._saved_item_index = None
            self._saved_status = None
            
    def add_playable(self, playable):
        """ Add a new item in the end of the playing queue. 
        """
        self._queue.append(playable)

    def remove_playable_with_id_from_queue(self, playable_id):
        """ Remove a playable from the queue, given its id (see
        Playable.get_id()).
        """
        for playable in self._queue:
            if playable.get_id() == playable_id:
                self._queue.remove(playable)
                break

    def next(self):
        """ Move forward to the next item in the playing queue. If the
        end of queue is reached, an IndexError is raised.
        """
        new_index = self._current_item_index + 1
        try:
            new_item = self._queue[new_index]
        except IndexError:
            raise IndexError, "end of queue reached"
        else:
            self._current_item_index = new_index
            self.play_uri(new_item.get_uri())

    def previous(self):
        """ Move backward to the previous item in the playing
        queue. If the beginning of the queue is reached an IndexError
        is raised.
        """
        new_index = self._current_item_index - 1
        if new_index < 0:
            raise IndexError, "can't go prior to the first queue's item"
        new_item = self._queue[new_index]
        self._current_item_index = new_index
        self.play_uri(new_item.get_uri())

    def get_current_item(self):
        """ Return the item of the playing queue which is currently selected
        """
        try:
            return self._queue[self._current_item_index]
        except IndexError:
            import pdb; pdb.set_trace()

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
        """ Fetch the current state of the player, can be one of:

        - Player.PLAYING
        - Player.PAUSED
        - Player.STOPPED
        """
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
            status = "%02d:%02d:%02d / %02d:%02d:%02d" % (position / 360, position / 60,
                                                          position % 60,
                                                          duration / 360, duration / 60,
                                                          duration % 60)
            print '\r %s (%s)' % (status,self.get_uri()),
        sys.stdout.flush()

class VideoSinkBin(gst.Bin):

    def __init__(self, needed_caps):
        self._width = None
        self._height = None
        self._current_frame = None
        gobject.threads_init()
        self._mutex = mutex()
        gst.Bin.__init__(self)
        self._capsfilter = gst.element_factory_make('capsfilter', 'capsfilter')

        self.set_caps(needed_caps)
        self.add(self._capsfilter)
        
        fakesink = gst.element_factory_make('fakesink', 'fakesink')
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
        if self.get_width() == None or self.get_height() == None:
            caps = pad.get_negotiated_caps()
            if caps != None:
                s = caps[0]
                self.set_width(s['width'])
                self.set_height(s['height'])
        if self.get_width() != None and self.get_height() != None and buffer != None:
            self.set_current_frame(buffer.data)
        return True

    def set_width(self, width):
        self._width = width

    def set_height(self, height):
        self._height = height
        
    def get_height(self):
        return self._height
        
    def get_width(self):
        return self._width
            
gobject.type_register(VideoSinkBin)    


if __name__ == '__main__':
    
    # usage:
    # player.py uri1 uri2
    
    manager = PlayerManager()
    mainloop = gobject.MainLoop()

    bus = MessageBus()

    def on_message(receiver, message, sender):
        print 'got message : %s' % message

    bus.register(lambda x: None, on_message)


    """
    # one player per uri
    for uri in sys.argv[1:]:
    
        p = Player(uri)
        p.register('player.playing', on_play)
        manager.add_player(p)
        p.play()
    """

    #"""
    # one player for all uris => use the queue
    p = Player()
    manager.add_player(p)
    
    for uri in sys.argv[1:]:
        p.add_playable(Playable(uri))

    p.next()
    #"""
    
    mainloop.run()
