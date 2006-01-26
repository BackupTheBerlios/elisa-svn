from internal import factory
import event

class EventsManager(factory._EventsManagerFactory()):
    """
    Surface class
    """
    
    def __init__(self):
        super(EventsManager,self).__init__()
