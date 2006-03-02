from elisa.framework.message import Message
import os, sys

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
        assert isinstance(message, Message)
        frame = calling_frame()
        sender = frame.f_locals['self']
        self.queue.insert(0, (message, sender, receiver))

    def register(self, instance, callback):
        #
        klass = callback.im_class
        self.callbacks[klass] = (callback, instance)

    def dispatch_messages(self):
        while self.queue:
            message, sender, receiver = self.queue.pop()
            if receiver:
                # dispatch to receiver
                callback, instance = self.callbacks.get(receiver.__class__,
                                                        lambda x,y: None)
                result = callback(receiver, message, sender)
                # flush the queue and exit if callback returned False
                if result == False:
                    self.queue = []
                    break
            else:
                # broadcast to all registered entities
                for receiver, callback in self.callbacks.iteritems():
                    callback, instance = self.callbacks.get(receiver, lambda x,y: None)
                    #import pdb; pdb.set_trace()
                    #print callback
                    result = callback(instance, message, sender)
                    # flush the queue and exit if callback returned False
                    if result == False:
                        self.queue = []
                        break
                    
def MessageBus():
    global _bus
    if not _bus:
        _bus = _MessageBus()
    return _bus

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
