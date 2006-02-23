import pygst
pygst.require('0.10')
import gst
import gobject, sys

def message_cb(bin, message):
    print message


def playfile(filename):
    player = gst.element_factory_make("playbin", "player")
    bin = player.get_bus()
    bin.connect('message', message_cb)
    

    player.set_property('uri', filename)

    print 'Playing:', filename
    player.set_state(gst.STATE_PLAYING)

playfile(sys.argv[1])
