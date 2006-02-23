
import logging

logger = None

class _Logger:
    """
    The Elisa logger, which basically log messages to a file named
    elisa.log. Use it like this:
    
      from framework.log import Logger

      logger.debug("hey this is a log message")
      logger.info("need some info ?")
      
    Logging levels:

    - INFO            : 20
    - DEBUG           : 10
    - DEBUG_DETAILLED : 5
    - DEBUG_VERBOSE   : 1

    """

    levels = {'DEBUG_DETAILLED': 5,
              'DEBUG_VERBOSE': 1
              }

    def __init__(self):
        
	format = '%(asctime)s %(levelname)-8s %(message)s'
	datefmt = '%a, %d %b %Y %H:%M:%S'
	fname = 'elisa.log'
	
	formatter = logging.Formatter(format, datefmt)
	handler = logging.FileHandler(fname)
	handler.setFormatter(formatter)

        for name, lvl in self.levels.iteritems():
            logging.addLevelName(lvl, name)

	Logger._log = logging.getLogger('Elisa')
	Logger._log.addHandler(handler)

        #self.set_level('STATUS')
        self.set_level('DEBUG_DETAILLED')
        
	logging.basicConfig()
	root = logging.getLogger()
	handler = root.handlers[0]
	handler.setFormatter(formatter)

    def set_level(self, name):
        """ Set the log level. name can be one of:

        - 'INFO'
        - 'DEBUG'
        - 'DEBUg_DETAILLED'
        - 'DEBUG_VERBOSE'

        """
        level = logging.getLevelName(name)
	Logger._log.setLevel(level)
        self._level_name = name

    def get_level(self):
        return self._level_name

    
    def info(self, info):
        """ Log some basic info (in >= INFO log level)
        """
        Logger._log.log(logging.INFO, info)

    def debug(self, msg):
        """ Log functional data (in >= DEBUG log level)
        """
        Logger._log.log(logging.DEBUG, msg)

    def debug_detailled(self, msg):
        """ Log verbose functional data (in >= DEBUG_DETAILLED log level)
        """
        Logger._log.log(self.levels['DEBUG_DETAILLED'], msg)

    def debug_verbose(self, msg, obj=None, level=None):
        """ Detailled logging (in >= DEBUG_VERBOSE log level)
        """
        if obj:
            msg = '%s on %s' % (msg, str(obj))
        Logger._log.log(self.levels['DEBUG_VERBOSE'], msg)
        
def Logger():
    global logger
    if logger is None:
        logger = _Logger()
    return logger

if __name__ == '__main__':
    l = Logger()

    l.info("Hello World")
    l.debug("Argh")
