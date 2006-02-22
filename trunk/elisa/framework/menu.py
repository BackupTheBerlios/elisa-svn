class MenuTree:

    """
    manipulate a tree 
    """
    
    def __init__(self, parent=None, short_name="MenuTree"):
        self._items = []
        self.set_parent(parent)
        self.set_short_name(short_name)
        self.set_help_string("")
        self.set_picture_path(None)

    def set_short_name(self, name):
        "name used on menu if picture is not set"
        self._short_name = name

    def get_short_name(self):
        "name used on menu if picture is not set"
        return self._short_name

    def set_help_string(self, help):
        """helpstring shown on box when item is selected"""        
        self._help_string = help

    def get_help_string(self):
        """helpstring shown on box when item is selected"""        
        return self._help_string

    def set_picture_path(self, path):
        """complete path of picture shown in menu"""        
        self._picture_path = path

    def get_picture_path(self):
        """complete path of picture shown in menu"""
        return self._picture_path

    def get_items(self):
        return self._items

    def get_item_with_name(self, name):
        for item in self.get_items():
            found = item.get_item_with_name(name)
            if not found:
                if item.get_short_name() == name:
                    found = item
            if found:
                return found

        return None
        
    def add_item(self, item):
        item.set_parent(self)
        self._items.append(item)

    def del_item(self, item):
        index = self._items.index(item)
        del self._items[index]

    def is_root(self):
        return self.get_parent() is None

    def set_parent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    def __repr__(self):
        level = self.get_level() 
        items = self.get_items()
        representation = "%s - %s (%s items)" % ("  " * level,
                                                 self.get_short_name(),
                                                 len(items))
        for item in items:
            representation += "\n" + repr(item)
        return representation

    def get_level(self):
        parent = self.get_parent()
        level = 0
        while parent:
            parent = parent.get_parent()
            level += 1
        return level


class MenuItem(MenuTree):

    """
    manipulate menu item element
    """
    
    def __init__(self, short_name="None"):
        MenuTree.__init__(self, short_name=short_name)
        self.set_selected_callback(None,())
        self.set_unselected_callback(None, ())
        self.set_action_callback(None, ())

    def __repr__(self):
        level = self.get_level() 
        representation = "%s - %s" % ("  " * level,
                                      self.get_short_name())
        return representation

    def set_selected_callback(self, cb, args):
        """callback called when menu item is selected"""
        self._selected_callback = cb
        self._selected_cb_args = args
        
    def get_selected_callback(self):
        """callback called when menu item is selected"""
        return (self._selected_callback, self._selected_cb_args)

    def set_action_callback(self, cb, args):
        self._action_callback = cb
        self._action_cb_args = args
        
    def get_action_callback(self):
        return (self._action_callback, self._action_cb_args)

    def set_unselected_callback(self, cb, args):
        self._unselected_callback = cb
        self._unselected_cb_args = args
        
    def get_unselected_callback(self):
        return (self._unselected_callback, self._unselected_cb_args)

    def call_selected_callback(self):
        """callback called when menu item is selected"""
        cb, args = self.get_selected_callback()
        cb(*args)

    def call_unselected_callback(self):
        """callback called when menu item is selected"""
        cb, args = self.get_unselected_callback()
        cb(*args)

    def call_action_callback(self):
        """callback called when menu item is selected"""
        cb, args = self.get_action_callback()
        cb(*args)

    # deprecated

    def SetShortname(self, in_shortname):
        """name used on menu if picture is not set"""
        raise DeprecationWarning, 'use set_short_name() instead'
    
    def GetShortname(self):
        raise DeprecationWarning, 'use get_short_name() instead'
        
    def GetLevel(self):
        "name used on menu if picture is not set"
        raise DeprecationWarning, 'use get_level() instead'
        
    def SetHelpstring(self, in_helpstring):
        raise DeprecationWarning, 'use set_help_string() instead'
        
    def GetHelpstring(self):
        raise DeprecationWarning, 'use get_help_string() instead'
     
    def SetPicturePathAndFilename(self, in_picturepath):
        raise DeprecationWarning, 'use set_picture_path() instead'
    
    def GetPicturePathAndFilename(self):
        """complete path of picture shown in menu"""
        raise DeprecationWarning, 'use get_picture_path() instead'
    
    def SetSelectedCallback(self, in_callback, in_args = None):
        raise DeprecationWarning, 'use set_selected_callback() instead'
        
    def SetUnselectedCallback(self, in_callback, in_args = None):
        """callback called when menu item is selected"""
        raise DeprecationWarning, 'use set_unselected_callback() instead'

    def SetActionCallback(self, in_callback, in_args = None):
        """callback called when menu item is selected"""
        raise DeprecationWarning, 'use set_action_callback() instead'

    def CallSelectedCallback(self):
        raise DeprecationWarning, 'use call_selected_callback() instead'
        
    def CallUnselectedCallback(self):
        raise DeprecationWarning, 'use call_unselected_callback() instead'
        
    def CallActionCallback(self):
        raise DeprecationWarning, 'use call_action_callback() instead'
    


if __name__ == '__main__':
    root = MenuTree()
    
    root.add_item(MenuItem(short_name="level 1"))

    sub = MenuTree()
    sub.add_item(MenuItem(short_name="level 2"))
    root.add_item(sub)

    print root
