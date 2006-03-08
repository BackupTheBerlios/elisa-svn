from elisa.boxwidget import surface, fontsurface

class MCEButton(surface.Surface):

    def __init__(self, text="label"):
        surface.Surface.__init__(self, text)
        self.set_background_from_file("extern/testGL/themes/mce/COMMON.BUTTON.LEFT.FOCUS.PNG")
        self.set_size(250,36)
        self.set_back_color(255, 255, 255)
        
        self._font = fontsurface.FontSurface('mce button font')
        self._font.set_text(text)
        self.add_surface(self._font)
        self.set_font_size(34)

    def get_font(self):
        return self._font
        
    def set_font_size(self, size):
        self._font.set_font_size(size)
        (_xb,_yb) = self.get_size()
        self._font.set_location(10, (_yb - size) / 2.0 , 0.1)
