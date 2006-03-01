from elisa.utils import event_dispatcher

"""
TODO:

- more Events!
- current events are really minimal, they could hold more data for instance


"""

class PlayingEvent(event_dispatcher.Event):
    name = "player.playing"

    def __init__(self, playable):
        self.playable = playable

    def __str__(self):
        return 'Playing : %r' % repr(self.playable)

class PausedEvent(event_dispatcher.Event):
    name = "player.paused"
    

class NewPlayerEvent(event_dispatcher.Event):
    name = "player_manager.new_player"

    def __init__(self, player):
        self.player = player
