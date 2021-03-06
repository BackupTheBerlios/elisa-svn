
class Event:
    name = "override_me"

    def get_name(self):
        return self.name
    

class EventDispatcher:

    callbacks = {}

    def register(self, event_name, callback):
        try:
            self.callbacks[event_name].append(callback)
        except KeyError:
            self.callbacks[event_name] = [callback,]

    def unregister(self, event_name, callback):
        self.callbacks[event_name].remove(callback)

    def fire_event(self, event):
        try:
            callbacks = self.callbacks[event.get_name()]
        except KeyError:
            callbacks = []
        for callback in callbacks:
            callback(event)
        
################################################################################


if __name__ == '__main__':

    class MyEvent(Event):
        name = "foo_bar"

    def my_callback(event):
        print 'event catched: %r' % event

    def other_callback(event):
        print 'catched again: %r' % event

    dispatcher = EventDispatcher()
    dispatcher.register('foo_bar', my_callback)
    dispatcher.register('foo_bar', other_callback)

    dispatcher.fire_event(MyEvent())

