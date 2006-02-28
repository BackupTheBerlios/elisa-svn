
from elisa.boxwidget.surface import Surface
from elisa.player.player import Player

class SurfacePlayer(Surface, Player):

    def get_width(self):
        pass

    def get_height(self):
        pass

    def fullscreen(self):
        pass

class MiniSurfacePlayer(SurfacePlayer):

    def get_width(self):
        " return fixed width "

    def get_height(self):
        " return fixed height "

    def fullscreen(self):
        " do nothing to switch to fullscreen "
        pass
    
