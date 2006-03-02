from elisa.framework.message import Message

class MessageBus:

    def send_message(self, message, sender, receiver):
        assert isinstance(message, Message)
        
        if hasattr(receiver, 'on_message'):
            receiver.on_message(message, sender)

if __name__ == '__main__':
    
    bus = MessageBus()

    class Foo: pass
    class Bar:

        def on_message(self, message, sender):
            print 'Got message %r from %r' % (message, sender)
            print message.data
            
    bus.send_message(Message('sentence','Hello you'), Foo(), Bar())
