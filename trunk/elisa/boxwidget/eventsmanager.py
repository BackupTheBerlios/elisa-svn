from elisa.boxwidget import events
from elisa.boxwidget.bindings import testgl_impl
from elisa.framework.log import Logger

class EventsManager(object):
    """
    events class
    """
    
    def __init__(self):
        self._logger = Logger()
        self._logger.debug('EventsManager.__init__()', self)
        
        self._eventsmanager_impl = testgl_impl._testGL_EventsManager_Impl()
    
    def get_event_queue(self):
        """
        @return: a list of event is queue and empty the queue
        """
        #self._logger.debug('EventsManager.get_event_queue()', self)
        return self._eventsmanager_impl.get_event_queue()

        
