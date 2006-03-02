
class Message:

    def __init__(self, typ, data):
        self.typ = typ
        self.data = data

    def get_type(self):
        return self.typ

    def get_data(self):
        return self.data
    
