from elisa.utils.event_dispatcher import Event

"""
TODO:

- more Events!
- current events are really minimal, they could hold more data for instance


"""

class PlayingEvent(Event):
    name = "player.playing"

    def __init__(self, playable):
        self.playable = playable

    def __str__(self):
        return 'Playing : %r' % repr(self.playable)

class PausedEvent(Event):
    name = "player.paused"

    def __init__(self, playable):
        self.playable = playable
    
class StoppedEvent(Event):
    name = "player.stopped"

class NewPlayerEvent(Event):
    name = "player_manager.new_player"

    def __init__(self, player):
        self.player = player
