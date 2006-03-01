
from elisa.boxwidget.surface import Surface
from elisa.player.player import Player

class SurfacePlayer(Surface, Player):

    def __init__(self, uri):
        Surface.__init__(self)
        Player.__init__(self, uri)

    def get_size(self):
        width = Player.get_width(self)
        height = Player.get_height(self)
        if None in (width, height):
            width, height = Surface.get_size(self)
        return (width, height)
    
    def fullscreen(self):
        pass

class MiniSurfacePlayer(SurfacePlayer):

    """
    TODO:

    - on gstreamer side : scale the video sink ?
    """

    def get_size(self):
        " return fixed width/height "
        return (128, 128)
    
    def fullscreen(self):
        " do nothing to switch to fullscreen "
        pass
    
