
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

    def __init__(self):
        
	format = '%(asctime)s %(levelname)-8s %(message)s'
	datefmt = '%a, %d %b %Y %H:%M:%S'
	fname = 'elisa.log'
	
	formatter = logging.Formatter(format, datefmt)
	handler = logging.FileHandler(fname)
	handler.setFormatter(formatter)
	
        logging.addLevelName(25, 'STATUS')
        logging.addLevelName(15, 'DETAILLED')

	Logger._log = logging.getLogger('Elisa')
	Logger._log.addHandler(handler)

        self.set_level('STATUS')
        #self.set_level('DETAILLED')
        	
	logging.basicConfig()
	root = logging.getLogger()
	handler = root.handlers[0]
	handler.setFormatter(formatter)

    def set_level(self, name):
        level = logging.getLevelName(name)
	Logger._log.setLevel(level)
        self._level_name = name

    def get_level(self):
        return self._level_name

    def ponctual(self, msg):
        Logger._log.log('NORMAL',msg)

    def loop(self, msg):
        Logger._log.log('DETAILLED', msg)
    
    def info(self, info):
        Logger._log.log('STATUS', info)

    def debug(self, msg, obj=None, level=None):
        if not obj:
            Logger._log.log('DEBUG', msg)
        else:
            Logger._log.log('DEBUG', msg + ' on ' + str(obj) )

        
def Logger():
    global logger
    if logger is None:
        logger = _Logger()
    return logger

if __name__ == '__main__':
    l = Logger()

    l.info("Hello World")
    l.error("Argh")
