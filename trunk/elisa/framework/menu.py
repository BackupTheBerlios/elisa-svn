import copy
from elisa.framework import message_bus

class Mixin:
    def set_short_name(self, name):
        "name used on menu if picture is not set"
        self._short_name = name

    def get_short_name(self):
        "name used on menu if picture is not set"
        if not hasattr(self, '_short_name'):
            self.set_short_name('')
        return self._short_name
    
    def get_items(self):
        """fetch the list of sub MenuTree/MenuItem instances """
        if not hasattr(self, '_items'):
            self._items = []
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

##     def __repr__(self):
##         items = self.get_items()
##         name = self.get_short_name()
##         return "%s (%s items)" % (name, len(items))

    def get_tree_from_item(self, parent_item=None, root_level=False):
        """ Create a new MenuTree starting at parent and including all
        the items stored by this item.
        """
        if not parent_item:
            parent_item = self.get_root()

        menu = MenuTree(parent_item.get_short_name())

        def build_sub_tree(items, parent):
            for item in items:
                new_item = item.copy()
                menu.add_item(new_item, parent=parent)
                if not root_level:
                    build_sub_tree(item.get_items(),new_item)

        build_sub_tree(parent_item.get_items(), parent_item.copy())
        return menu


class MenuTree(Mixin):
    """
    manipulate a tree 
    """
    
    def __init__(self, short_name="MenuTree"):
        self._items = []
        self.set_short_name(short_name)
        
    def get_parent(self):
        return None

    def get_root(self):
        return self

    def copy(self):
        """ Create a copy of the MenuItem
            TODO: copy the items too ?
        """
        dup = copy.deepcopy(self)
        dup._items = []
        return dup

    def as_menu_item(self):
        new_item = MenuItem(short_name=self.get_short_name())
        new_item._items = self._items
        return new_item
        
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
        self._bus = message_bus.MessageBus()
        self._bus.register(self, self.on_message)
        self._items = []
        self.set_parent(parent)
        self.set_short_name(short_name)
        self.set_help_string("")
        self.set_icon_path(None)
        self.set_target_path(None)
        #self.set_picture_path(None)
        self.set_selected_callback(None)
        self.set_unselected_callback(None)
        self.set_action_callback(None)

    def on_message(self, receiver, message, sender):
        return True
        
    def pretty_print(self):
        """ Textual representation of the item """
        level = self.get_level() 
        representation = "%s - %s" % ("  " * level,
                                      self.get_short_name())
        for item in self.get_items():
            representation += "\n" + item.pretty_print()
        return representation

    def copy(self):
        dup = copy.deepcopy(self)
        dup.set_parent(None)
        dup._items = []
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

    def get_root(self):
        parent = self.get_parent()
        while parent:
            if not parent.get_parent():
                return parent
            parent = parent.get_parent()
        return None

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

    def set_help_string(self, help_string):
        """helpstring shown on box when item is selected"""        
        self._help_string = help_string

    def get_help_string(self):
        """helpstring shown on box when item is selected"""        
        return self._help_string

##     def set_picture_path(self, path):
##         """complete path of picture shown in menu"""        
##         self._picture_path = path

##     def get_picture_path(self):
##         """complete path of picture shown in menu"""
##         return self._picture_path

    def set_icon_path(self, path):
        """ """
        self._icon_path = path

    def get_icon_path(self):
        """ """
        return self._icon_path

    def set_target_path(self, path):
        """ """
        self._target_path = path

    def get_target_path(self):
        """ """
        return self._target_path

    def set_selected_callback(self, callback):
        """message called when menu item is selected"""
        self.selected_callback = callback
        
    def fire_selected(self, *args):
        """message called when menu item is selected"""
        if callable(self.selected_callback):
            self.selected_callback(*args)

    def set_action_callback(self, callback):
        """callback called when menu item is activated"""
        self.action_callback = callback
        
    def fire_action(self, *args):
        """message called when menu item is activated"""
        if callable(self.action_callback):
            self.action_callback(*args)
        
    def set_unselected_callback(self, callback):
        """message called when menu item is unselected"""
        self.unselected_callback = callback
        
    def fire_unselected(self, *args):
        """message called when menu item is unselected"""
        if callable(self.unselected_callback):
            self.unselected_callback(*args)

if __name__ == '__main__':
    root = MenuTree()
    
    root.add_item(MenuItem(short_name="level 1"))

    sub = MenuItem(short_name="level 1 bis")
    sub.add_item(MenuItem(short_name="level 2"))
    root.add_item(sub)

    print root.pretty_print()
    print "-" * 80
    lvl1b = root.get_item_with_name("level 1 bis")
    print lvl1b
    
    print root.get_items()

    print sub.get_root()

    new_sub_tree = root.get_tree_from_item()#lvl1b)
    print new_sub_tree
    print new_sub_tree.get_items()[0].get_level()
    print new_sub_tree.pretty_print()

    print root.get_tree_from_item(lvl1b).pretty_print()

    print "-" * 80
    
    print root.get_tree_from_item(root_level=True).pretty_print()
