class BaseSkinPictures(object):

    def __init__(self):
        self._pictures = {}
        self._pictures['BACKGROUND_PICTURE']    = None
        
    def get_picture(self, name):
        return self._pictures[name]
        
