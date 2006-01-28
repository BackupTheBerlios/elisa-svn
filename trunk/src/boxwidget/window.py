from internal import factory
from boxwidget import eventsmanager, event

class Window(factory._WindowFactory()):
    """
    Main Window Class
    #TODO see if Refresh code can be put in base class
    """
    
    def __init__(self):
        super(Window,self).__init__() 
        self._EventsHandler = eventsmanager.EventsManager()
    
    def Refresh(self):
    
        for currentevent in self._EventsHandler.GetEventQueue():
            e = currentevent.GetSimpleEvent()
            self._FireEventToAllWidget(currentevent)
            if e == event.SE_QUIT:
                self.Close()
                
        return super(Window,self).Refresh()
