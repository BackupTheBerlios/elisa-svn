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

    def set_help_string(self, help_string):
        """helpstring shown on box when item is selected"""        
        self._help_string = help_string

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
        """fetch the list of sub MenuTree/MenuItem instances """
        return self._items

    def get_item_with_name(self, name):
        """look for a MenuTree/MenuItem with given name in the
        children list. This method is recursive
        """
        for item in self.get_items():
            found = item.get_item_with_name(name)
            if not found:
                if item.get_short_name() == name:
                    found = item
            if found:
                return found

        return None
        
    def add_item(self, item):
        """ Add a new MenuTree/MenuItem in our children list and link
        the item with self
        """
        item.set_parent(self)
        self._items.append(item)

    def del_item(self, item):
        """ Remove the item instance from our children list
        """
        index = self._items.index(item)
        del self._items[index]

    def is_root(self):
        """ Boolean util method to check wether we are the root node
        of the tree
        """
        return self.get_parent() is None

    def set_parent(self, parent):
        """ Link the current instance with another MenuTree, which
        becomes our parent node
        """
        self._parent = parent

    def get_parent(self):
        """ MenuTree parent accessor
        """
        return self._parent

    def __repr__(self):
        """ Textual representation of the tree. This method is recursive
        """
        level = self.get_level() 
        items = self.get_items()
        representation = "%s - %s (%s items)" % ("  " * level,
                                                 self.get_short_name(),
                                                 len(items))
        for item in items:
            representation += "\n" + repr(item)
        return representation

    def get_level(self):
        """ Fetch the depth at which the instance is located in the
        tree. Return 0 if we are root.
        """
        parent = self.get_parent()
        level = 0
        while parent:
            parent = parent.get_parent()
            level += 1
        return level


class MenuItem(MenuTree):
    """
    Manipulate menu item element
    """
    
    def __init__(self, short_name="None"):
        MenuTree.__init__(self, short_name=short_name)
        self.set_selected_callback(None, ())
        self.set_unselected_callback(None, ())
        self.set_action_callback(None, ())

    def __repr__(self):
        """ Textual representation of the item """
        level = self.get_level() 
        representation = "%s - %s" % ("  " * level,
                                      self.get_short_name())
        return representation

    def set_selected_callback(self, callback, args):
        """callback called when menu item is selected"""
        self._selected_callback = callback
        self._selected_callback_args = args
        
    def get_selected_callback(self):
        """callback called when menu item is selected"""
        return (self._selected_callback, self._selected_callback_args)

    def set_action_callback(self, callback, args):
        """callback called when menu item is activated"""
        self._action_callback = callback
        self._action_callback_args = args
        
    def get_action_callback(self):
        """callback called when menu item is activated"""
        return (self._action_callback, self._action_callback_args)

    def set_unselected_callback(self, callback, args):
        """callback called when menu item is unselected"""
        self._unselected_callback = callback
        self._unselected_callback_args = args
        
    def get_unselected_callback(self):
        """callback called when menu item is unselected"""
        return (self._unselected_callback, self._unselected_callback_args)

    def call_selected_callback(self):
        """callback called when menu item is selected"""
        callback, args = self.get_selected_callback()
        callback(*args)

    def call_unselected_callback(self):
        """callback called when menu item is selected"""
        callback, args = self.get_unselected_callback()
        callback(*args)

    def call_action_callback(self):
        """callback called when menu item is selected"""
        callback, args = self.get_action_callback()
        callback(*args)

if __name__ == '__main__':
    root = MenuTree()
    
    root.add_item(MenuItem(short_name="level 1"))

    sub = MenuTree()
    sub.add_item(MenuItem(short_name="level 2"))
    root.add_item(sub)

    print root
