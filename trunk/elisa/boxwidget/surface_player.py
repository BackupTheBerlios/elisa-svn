
from elisa.boxwidget.surface import Surface
from elisa.player.player import Player

class SurfacePlayer(Surface, Player):

    def get_size(self):
        pass
    
    def fullscreen(self):
        pass

class MiniSurfacePlayer(SurfacePlayer):

    def get_size(self):
        " return fixed width/height "

    def fullscreen(self):
        " do nothing to switch to fullscreen "
        pass
    
