class InputDevices(object):

    """
    input device abstraction
    for keyboard, mouse and infrared devices
    """
    
    KEY = 0
    KEY_RIGHT_ARROW = 1
    KEY_UP_ARROW = 2
    KEY_DOWN_ARROW = 4
    KEY_ENTER = 5
    
    def __init__(self):
    
        self._KeyValue = ""
        
    def EventQueue(self):
        """
        list of event in queue
        each call empty the queue
        """
