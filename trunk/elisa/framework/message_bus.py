import os, sys
import copy

def calling_frame():
    """ Calling sys frame """
    f = sys._getframe()

    while True:
        if is_user_source_file(f.f_code.co_filename):
            return f
        f = f.f_back

def is_user_source_file(filename):
    return os.path.normcase(filename) != _srcfile

def _current_source_file():
    base, ext = os.path.splitext(__file__)
    if ext in ('.pyc', '.pyo'):
        return '%s.py' % base
    else:
        return __file__

_srcfile = os.path.normcase(_current_source_file())


_bus = None

class _MessageBus:

    # list of (message, sender, receiver) tuples
    queue = []

    # mapping of class -> callback
    callbacks = {}

    def send_message(self, message, receiver=None):
        assert isinstance(message, Message), message
        frame = calling_frame()
        sender = frame.f_locals['self']
        self.queue.insert(0, (message, sender, receiver))

    def register(self, instance, callback):
        self.callbacks[instance] = callback
        
    def dispatch_messages(self):

        while self.queue:
            message, sender, receiver = self.queue.pop()
            if receiver:
                # dispatch to receiver
                callback = self.callbacks.get(receiver,
                                              lambda x,y: None)
                result = callback(receiver, message, sender)
                # flush the queue and exit if callback returned False
                if result == False:
                    self.queue = []
                    break
            else:
                # broadcast to all registered entities
                callbacks = copy.copy(self.callbacks)
                for receiver, callback in callbacks.iteritems():
                    result = callback(receiver, message, sender)
                    
                    # flush the queue and exit if callback returned False
                    if result == False:
                        self.queue = []
                        break
                    
def MessageBus():
    global _bus
    if not _bus:
        _bus = _MessageBus()
    return _bus

class Message(object): pass


if __name__ == '__main__':
    
    bus = MessageBus()

    class Foo: pass
    class Bar:

        def on_message(self, message, sender):
            print 'Got message %r from %r' % (message, sender)
            print message.data

    f = Foo()
    b = Bar()
    bus.register(Bar.on_message)

    for i in range(5):
        data = '%s. Hello you' % i
        bus.send_message(Message('sentence', data), f, b)

    bus.dispatch_messages()
