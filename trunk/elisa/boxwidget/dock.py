
from elisa.boxwidget import surface
from elisa.skins.default_skin import treeitem

"""
This should probably go to skin package ...

"""

class Dock(surface.Surface):

    def __init__(self, name="Dock"):
        surface.Surface.__init__(self, name)

        self._back_image = surface.Surface('backimage')
        self._back_image.set_background_from_file("extern/testGL/themes/mce/COMMON.BACKGROUND.PNG")
        self._back_image.set_size(250,340)
        self._back_image.set_location(10,10,2.1)
        self.add_surface(self._back_image)


        self._surface_items = []
        self.set_alpha_level(0)
        self._items_surface = surface.Surface('group items surface')
        self._items_surface.set_alpha_level(0)
        self._items_surface.set_location(0,0,0.01)
        self.add_surface(self._items_surface)

        
        #self.add_surface()
    
    def add_item(self, item):
        self._items_surface.add_surface(treeitem.TreeItem(item))
