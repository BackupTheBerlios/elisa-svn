from elisa.skins import base_skin_pictures

class MCESkinPictures(base_skin_pictures.BaseSkinPictures):

    def __init__(self):
        base_skin_pictures.BaseSkinPictures.__init__(self)
        self._pictures['BACKGROUND_PICTURE']    = 'elisa/skins/mce_skin/pictures/backgound.png'
