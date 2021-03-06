
from elisa.framework.plugin import IPlugin, TreePlugin, ExtensionPoint
from elisa.framework.extension_points import IDataAccess
import elisa.utils.misc

class PicturesTreePlugin(TreePlugin):
    """
    pictures plugin_tree
    """

    __implements__ = IPlugin

    data_access = ExtensionPoint(IDataAccess)
    
    name = "pictures"
    default_config = {'locations':['sample_data/pictures',]}

    def __init__(self, _application):
        TreePlugin.__init__(self, _application)
        self.set_short_name("pictures")
        
        folder_image = 'elisa/skins/default_skin/pictures/folder.png'
        locations = self.get_config().get('locations')
        
        for data_loader in self.data_access:
            for location in locations:
                data_loader.load_location(location,
                                          item_filter=elisa.utils.misc.file_is_picture,
                                          folder_icon_path=folder_image,
                                          item_action=self.show_picture)

    def show_picture(self, menu_item):
        appli = self.get_application()
        surface = appli.get_menu_renderer().get_surface_from_menuitem(menu_item)
        #import pdb; pdb.set_trace()
        appli.set_background_texture(surface.get_texture())
        self.logger.info('Showing picture %s' % surface.get_background_file())
