#Main device
DEV_KEYBOARD = "DEV_KEYBOARD"
DEV_SYSTEM = "DEV_SYSTEM"

#Predefined value for data for system event
EVENT_QUIT = "EVENT_QUIT"
KEY_LEFT = "KEY_LEFT"   
KEY_RIGHT = "KEY_RIGHT"
KEY_UP = "KEY_UP"   
KEY_DOWN = "KEY_DOWN"
KEY_RETURN = "KEY_RETURN"
KEY_SPACE = "KEY_SPACE"
KEY_ESCAPE = "KEY_ESCAPE"

#SimpleEvent
SE_OK = "SE_OK"
SE_MENU = "SE_MENU"
SE_UP = "SE_UP"
SE_DOWN = "SE_DOWN"
SE_LEFT = "SE_LEFT"
SE_RIGHT = "SE_RIGHT"
SE_QUIT = "SE_QUIT"

class Events(object):
    """
    single event class handler
    """
    def __init__(self, device, value, simple_event):
    
        self._device = device
        self._value = value
        self._simple_event = simple_event
        
    def get_device(self):
        return self._device
        
    def get_value(self):
        return self._datatype
        
    def get_simple_event(self):
        return self._simple_event
        
    def __repr__(self):
        return "Event("+str(self._device)+","+str(self._value)+","+str(self._simple_event)+")"
