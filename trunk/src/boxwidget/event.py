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
SE_UP = "SE_UP"
SE_DOWN = "SE_DOWN"
SE_LEFT = "SE_LEFT"
SE_RIGHT = "SE_RIGHT"
SE_QUIT = "SE_QUIT"

class Event(object):
    """
    single event class handler
    """
    def __init__(self, in_device, in_value, in_simpleevent):
    
        self._device = in_device
        self._value = in_value
        self._simpleevent = in_simpleevent
        
    def GetDevice(self):
        return self._device
        
    def GetValue(self):
        return self._datatype
        
    def GetSimpleEvent(self):
        return self._simpleevent
        
    def __repr__(self):
        return "Event("+str(self._device)+","+str(self._value)+","+str(self._simpleevent)+")"
