
from elisa.framework.plugin import IPlugin

class IDataAccess(IPlugin):

    def load_directory(name, item_filter=None, folder_icon_path=None,
                       item_action=None, item_icon_path=None):
        pass
    
    
