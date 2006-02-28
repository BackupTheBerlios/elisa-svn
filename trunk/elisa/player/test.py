import pygst
pygst.require('0.10')
import gst
import gobject, sys

## def on_eos():
##     pass

## def message_cb(bus, message):
##     print message
##     t = message.type
##     if t == gst.MESSAGE_EOS:
##         on_eos()


## def play_uri(uri):
##     #bin = player.get_bus()
##     #bin.connect('message', message_cb)


class Player:

    def __init__(self):

        self._gst_player = gst.element_factory_make("playbin", "player")

    def play_uri(self, uri):
        print 'Playing:', uri
        self._gst_player.set_property('uri', uri)
        self.play()
        
    def play(self):
        self._gst_player.set_state(gst.STATE_PLAYING)

    def pause(self):
        self._gst_player.set_state(gst.STATE_PAUSED)
        
    def stop(self):
        self._gst_player.set_state(gst.STATE_READY)

    def get_state(self, timeout=1):
        return self._gst_player.get_state(timeout=timeout)

    def query_position(self):
        "Returns a (position, duration) tuple"
        try:
            position, format = self._gst_player.query_position(gst.FORMAT_TIME)
        except:
            position = gst.CLOCK_TIME_NONE

        try:
            duration, format = self._gst_player.query_duration(gst.FORMAT_TIME)
        except:
            duration = gst.CLOCK_TIME_NONE

        return (position, duration)

    def seek(self, location):
        """
        @param location: time to seek to, in nanoseconds
        """
        gst.debug("seeking to %r" % location)
        event = gst.event_new_seek(1.0, gst.FORMAT_TIME,
                                   gst.SEEK_FLAG_FLUSH | gst.SEEK_FLAG_ACCURATE,
                                   gst.SEEK_TYPE_SET, location,
                                   gst.SEEK_TYPE_NONE, 0)

        res = self._gst_player.send_event(event)
        if res:
            gst.info("setting new stream time to 0")
            self._gst_player.set_new_stream_time(0L)
        else:
            gst.error("seek to %r failed" % location)


def launch():
    mainloop = gobject.MainLoop()

    p = Player()
    p.play_uri(sys.argv[1])

    mainloop.run()


if __name__ == '__main__':
    launch()
