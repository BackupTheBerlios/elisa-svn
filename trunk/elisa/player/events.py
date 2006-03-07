from elisa.framework.message_bus import Message

"""
TODO:

- more Events!
- current events are really minimal, they could hold more data for instance


"""

class PlayerEvent(Message):
    pass

class PlayingEvent(PlayerEvent):
    name = "player.playing"

    def __init__(self, playable):
        self.playable = playable

class PausedEvent(PlayerEvent):
    name = "player.paused"

    def __init__(self, playable):
        self.playable = playable
    
class StoppedEvent(PlayerEvent):
    name = "player.stopped"

class NewPlayerEvent(PlayerEvent):
    name = "player_manager.new_player"

    def __init__(self, player):
        self.player = player
