from elisa.framework import menu, menu, config,  log

from sets import Set
import inspect

"""
Borrowed some code from this recipe:
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/204349
"""

class InterfaceOmission(Exception):
    """
    Raised when an un-implemented method is found in the plugin
    """
    

class IPlugin(object):
    """
    This is the base interface for our plugin system. Every Plugin
    sub-class has to implement it.

    You can declare the default methods each plugin should implement here.
    """

    
class InterfaceChecker(type):
    """
    Validates the presence of required attributes
    """
    
    def __new__(cls, classname, bases, classdict):
        obj = type.__new__(cls, classname, bases, classdict)
        interface = classdict.get('__implements__')
        if interface:
            defined = Set(dir(obj))
            required = Set(dir(interface))
            if not required.issubset(defined):
                missing = list(required - defined)
                error = "Not implemented methods from %s : %r"
                raise InterfaceOmission, error % (interface.__name__,
                                                  missing)

        # safety check
        if classname not in ('Plugin', 'TreePlugin',
                             'CustomPlugin', 'ScreenLessPlugin'):
            assert obj.implements(IPlugin), \
                   "You need to implement at least IPlugin in %r" % classname
        
        return obj

class Plugin(object):
    
    "Plugin Base Class"

    __metaclass__ = InterfaceChecker


    default_config = {}
    name = "default"
    
    def __init__(self):
        """
        Constructor
        """
        self.logger = log.Logger()
        self.load_config()
        
    def load_config(self):
        self.logger.info('Plugin %s is loading its config' % self.name)
        _config = config.Config()
        section_name = "plugins.%s" % self.name

        section = _config.get_section(section_name)
        if not section:
            section = self.default_config
            _config.add_section(section_name,self.default_config)

        self.config = section

    def get_config(self):
        return self.config

    def implements(cls, interface):
        """
        Check the class implements the given interface which is searched
        "deeply" in the __implements__ list.
        """

        assert hasattr(cls, '__implements__'), "Missing __implements__ in %r" % cls

        def findInterface(interface, iface,doInspect=True):
            if doInspect:
                classTree = inspect.getclasstree([iface,])
            else:
                classTree = iface
            for item in classTree:
                try:
                    (typ, subTree) = item
                except TypeError:
                    return False
                except ValueError:
                    (typ, subTree) = item[0]
                if (interface.__name__ == typ.__name__) \
                       or findInterface(interface, subTree,doInspect=False) :
                    return True
            return False

        return findInterface(interface, cls.__implements__)
    
    implements = classmethod(implements)
    


class TreePlugin(Plugin, menu.MenuTree):
    
    "tree navigation Plugin Class"

    def __init__(self):
        """
        Constructor
        """
        Plugin.__init__(self)
        menu.MenuTree.__init__(self)

class CustomPlugin(Plugin):
    
    "custom interface Plugin Class"

    def __init__(self):
        """
        Constructor
        """


class ScreenLessPlugin(Plugin):
    
    def __init__(self):
        """
        Constructor
        """
        
