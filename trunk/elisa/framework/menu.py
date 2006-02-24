
class Mixin:
    def set_short_name(self, name):
        "name used on menu if picture is not set"
        self._short_name = name

    def get_short_name(self):
        "name used on menu if picture is not set"
        return self._short_name
    
    def get_items(self):
        """fetch the list of sub MenuTree/MenuItem instances """
        return self._items
    
    def add_item(self, item, parent=None):
        """ Add a new MenuTree/MenuItem in our children list and link
        the item with self
        """
        if not parent:
            parent = self
            
        item.set_parent(parent)
        self._items.append(item)

    def del_item(self, item):
        """ Remove the item instance from our children list
        """
        index = self._items.index(item)
        del self._items[index]

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

    def __repr__(self):
        items = self.get_items()
        name = self.get_short_name()
        return "%s (%s items)" % (name, len(items))

class MenuTree(Mixin):
    """
    manipulate a tree 
    """
    
    def __init__(self, short_name="MenuTree"):
        self._items = []
        self.set_short_name(short_name)

    def get_parent(self):
        return None
        
    def pretty_print(self):
        """ Textual representation of the tree. This method is recursive
        """
        items = self.get_items()
        representation = "- %s (%s items)" % (self.get_short_name(),
                                              len(items))
        for item in items:
            representation += "\n" + item.pretty_print()
        return representation

class MenuItem(Mixin):
    """
    Manipulate menu item element
    """
    
    def __init__(self, parent=None, short_name="None"):
        self.set_parent(parent)
        self.set_short_name(short_name)
        self.set_help_string("")
        self.set_picture_path(None)
        self.set_selected_callback(None, ())
        self.set_unselected_callback(None, ())
        self.set_action_callback(None, ())
        self._items = []
        
    def pretty_print(self):
        """ Textual representation of the item """
        level = self.get_level() 
        representation = "%s - %s" % ("  " * level,
                                      self.get_short_name())
        for item in self.get_items():
            representation += "\n" + item.pretty_print()
        return representation

    def copy(self):
        """ Create a copy of the MenuItem
            TODO: copy all the MenuItem attributes (callbacks, help, picture_path)
        """
        dup = MenuItem(parent=self.get_parent(),
                       short_name=self.get_short_name())
        return dup
    
    def set_parent(self, parent):
        """ Link the current instance with another MenuTree, which
        becomes our parent node
        """
        self._parent = parent

    def get_parent(self):
        """ MenuTree parent accessor
        """
        return self._parent

    def get_items_from_parent(self, parent=None):
        """ Create a new MenuTree starting at parent and including all
        the items stored by this item.
        """
        if not parent:
            parent = self.get_root()

        menu = MenuTree(parent.get_short_name())

        def build_sub_menu(items):
            for item in items:
                new_item = item.copy()
                menu.add_item(new_item, parent=item.get_parent())
                build_sub_menu(item.get_items())

        build_sub_menu(parent.get_items())
        return menu


    def get_root(self):
        parent = self.get_parent()
        while parent:
            if not parent.get_parent():
                return parent
            parent = parent.get_parent()
        return None

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

    sub = MenuItem(short_name="level 2")
    sub.add_item(MenuItem(short_name="level 3"))
    root.add_item(sub)

    print root.pretty_print()
    print "-" * 80
    print root.get_item_with_name("level 2")

    print root.get_items()

    print sub.get_root()
    
    print sub.get_items_from_parent(sub).pretty_print()
