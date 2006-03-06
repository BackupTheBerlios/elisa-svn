from elisa.framework.message_bus import Message

"""
TODO:

- more Events!
- current events are really minimal, they could hold more data for instance


"""

class PlayingEvent(Message):
    name = "player.playing"

    def __init__(self, playable):
        self.playable = playable

class PausedEvent(Message):
    name = "player.paused"

    def __init__(self, playable):
        self.playable = playable
    
class StoppedEvent(Message):
    name = "player.stopped"

class NewPlayerEvent(Message):
    name = "player_manager.new_player"

    def __init__(self, player):
        self.player = player
