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
        self._gst_player.set_state(gst.STATE_PLAYING)


def launch():
    mainloop = gobject.MainLoop()

    p = Player()
    p.play_uri(sys.argv[1])

    mainloop.run()


if __name__ == '__main__':
    launch()
