class _EventsManagerBase(object):
    """
    Base class for input event management
    do not use directly
    """

    def __init__(self):
        self._eventqueue = []
    
    def GetEventQueue(self):
        """
        @return: a list L{eventsmanager.Event} and empty the queue
        """
        return_value = self._eventqueue
        self._eventqueue = []
        return return_value
        
    def PushEvent(self, in_event):
        self._eventqueue.append(in_event)
