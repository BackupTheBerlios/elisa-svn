class InputDevices(object):

    """
    input device abstraction
    for keyboard, mouse and infrared devices
    """
    
    #Main device
    DEVICE_KEYBOARD = 0
    DEVICE_MOUSE = 1
    DEVICE_INFRARED = 2
    
    #Data type returned in event
    DT_ASCII = 0
    
    #SimpleEvent
    SE_OK = 0
    SE_UP = 1
    SE_DOWN = 2
    SE_LEFT = 3
    SE_RIGHT = 4
    
    def __init__(self):
    
        self._KeyValue = ""
        
    def EventQueue(self):
        """
        list of event in queue
        each call empty the queue
        @return: tuple with 4 parameter: (MainDevice, DataType, Value, SimpleEvent)
        
        MainDevice, Datatype and SimpleEvent are constants define in InputDevices class.  
            - DEVICE_* are MainDevice constants
            - DT_* are DataType constants
            - SE_* are SimpleEvent constants
        """
