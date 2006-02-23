
import logging

logger = None

class _Logger:
    """
    The Elisa logger, which basically log messages to a file named
    elisa.log. Use it like this:
    
      from framework.log import Logger

      logger.debug("hey this is a log message")
      logger.info("need some info ?")
      
    Other operations available:

    - error(msg)
    - warning(msg)
    - critical(msg)

    """

    def __init__(self):
        
	format = '%(asctime)s %(levelname)-8s %(message)s'
	datefmt = '%a, %d %b %Y %H:%M:%S'
	fname = 'elisa.log'
	
	formatter = logging.Formatter(format, datefmt)
	handler = logging.FileHandler(fname)
	handler.setFormatter(formatter)

        logging.addLevelName(15, 'DETAILLED')
	
	Logger._log = logging.getLogger('Elisa')
	Logger._log.addHandler(handler)

        self.set_level('DEBUG')
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

    def disable(self):
        for level_name in ('CRITICAL', 'DEBUG', 'INFO',
                           'ERROR', 'FATAL'):
            level = getattr(logging, level_name)
            logging.disable(level)

    def enable(self):
        pass

    def debug(self, msg, obj=None, level=None):

        if not level:
            level = self.get_level()
        elif level == 'NORMAL':
            level = 'INFO'
        elif level == 'VERBOSE':
            level = 'DEBUG'

        self.set_level(level)

        if not obj:
            Logger._log.debug(msg)
        else:
            Logger._log.debug(msg + ' on ' + str(obj) )
    
    def info(self, info):
        Logger._log.info(info)

    """
    def error(self, error):
        Logger._log.error(error)

    def warning(self, warning):
        Logger._log.warning(warning)

    def critical(self, msg):
        Logger._log.critical(msg)
    """
        
def Logger():
    global logger
    if logger is None:
        logger = _Logger()
    return logger

if __name__ == '__main__':
    l = Logger()

    l.info("Hello World")
    l.error("Argh")
