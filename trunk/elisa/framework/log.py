
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

    - STATUS    : 25
    - INFO      : 20
    - DETAILLED : 15
    - DEBUG     : 10

    """

    levels = {'STATUS': 25,
              'DETAILLED': 15
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
        self.set_level('DETAILLED')
        	
	logging.basicConfig()
	root = logging.getLogger()
	handler = root.handlers[0]
	handler.setFormatter(formatter)

    def set_level(self, name):
        """ Set the log level. name can be one of:

        - 'STATUS'
        - 'INFO'
        - 'DETAILLED'
        - 'DEBUG'

        if the level is set to 'DETAILLED' then 'STATUS' and 'INFOS'
        also become active. Another example: if level set to 'DEBUG',
        all others levels become active too.

        """
        level = logging.getLevelName(name)
	Logger._log.setLevel(level)
        self._level_name = name

    def get_level(self):
        return self._level_name

    def debug_fct(self, msg):
        Logger._log.log(logging.INFO,msg)

    def debug_fct_v(self, msg):
        Logger._log.log(self.levels['DETAILLED'], msg)
    
    def info(self, info):
        Logger._log.log(self.levels['STATUS'], info)

    def debug_details(self, msg, obj=None, level=None):
        if not obj:
            Logger._log.log(logging.DEBUG, msg)
        else:
            Logger._log.log(logging.DEBUG, msg + ' on ' + str(obj) )

    # backward compat

    debug = debug_details

        
def Logger():
    global logger
    if logger is None:
        logger = _Logger()
    return logger

if __name__ == '__main__':
    l = Logger()

    l.info("Hello World")
    l.debug("Argh")
