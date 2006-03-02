from elisa.framework.message import Message

class MessageBus:

    # list of (message, sender, receiver) tuples
    queue = []

    # mapping of class -> callback
    callbacks = {}
    
    def send_message(self, message, sender, receiver):
        assert isinstance(message, Message)
        self.queue.insert(0, (message, sender, receiver))

    def register(self, obj, callback):
        self.callbacks[obj] = callback

    def dispatch_messages(self):
        while self.queue:
            message, sender, receiver = self.queue.pop()
            callback = self.callbacks.get(receiver.__class__, lambda x,y: None)
            callback(receiver, message, sender)

if __name__ == '__main__':
    
    bus = MessageBus()

    class Foo: pass
    class Bar:

        def on_message(self, message, sender):
            print 'Got message %r from %r' % (message, sender)
            print message.data

    f = Foo()
    b = Bar()
    bus.register(Bar, Bar.on_message)

    for i in range(5):
        data = '%s. Hello you' % i
        bus.send_message(Message('sentence', data), f, b)

    bus.dispatch_messages()
