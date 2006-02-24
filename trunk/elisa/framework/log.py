
import logging
from elisa.utils import singleton
import sys

logger = None

class CustomFile:

    def __init__(self, f):
        self.do_write = True
        self.f = f
        

    def write(self, data):
        if self.do_write:
            self.f.write(data)

    def __getattr__(self, attr):
        return getattr(self.f, attr)

err = CustomFile(sys.stderr)

class Logger(singleton.Singleton):
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

    FIXME : Line insered in double in logfile
    FIXME : put miliseconds on logs
    """

    levels = {'DEBUG_DETAILLED': 5,
              'DEBUG_VERBOSE': 1
              }

    def __init__(self):
        singleton.Singleton.__init__(self)
        
        format = '%(asctime)s %(levelname)-8s %(message)s'
        datefmt = '%a, %d %b %Y %H:%M:%S'
        fname = 'elisa.log'

        formatter = logging.Formatter(format, datefmt)
        handler = logging.FileHandler(fname)
        handler.setFormatter(formatter)

        for name, lvl in self.levels.iteritems():
            logging.addLevelName(lvl, name)

        self._log = logging.getLogger('Elisa')
        self._log.addHandler(handler)

        #self.set_level('STATUS')
        self.set_level('DEBUG_DETAILLED')

        try:
            logging.basicConfig(stream=err)
        except TypeError:
            # happens when using python 2.3
            logging.basicConfig()
        
        root = logging.getLogger()
        handler = root.handlers[0]
        handler.setFormatter(formatter)

        self.disable_console_output()

    def enable_console_output(self):
        err.do_write = True

    def disable_console_output(self):
        err.do_write = False

        
    def set_level(self, name):
        """ Set the log level. name can be one of:

        - 'INFO'
        - 'DEBUG'
        - 'DEBUg_DETAILLED'
        - 'DEBUG_VERBOSE'

        """
        level = logging.getLevelName(name)
        self._log.setLevel(level)
        self._level_name = name

    def get_level(self):
        """ Fetch current log level string identifier
        """
        return self._level_name

    def info(self, info):
        """ Log some basic info (in >= INFO log level)
        """
        self._log.log(logging.INFO, info)

    def debug(self, msg, obj=None):
        """ Log functional data (in >= DEBUG log level)
        """
        if obj:
            msg = '%s on %s' % (msg, str(obj))
        self._log.log(logging.DEBUG, msg)

    def debug_detailled(self, msg, obj=None):
        """ Log verbose functional data (in >= DEBUG_DETAILLED log level)
        """
        if obj:
            msg = '%s on %s' % (msg, str(obj))
        self._log.log(self.levels['DEBUG_DETAILLED'], msg)

    def debug_verbose(self, msg, obj=None):
        """ Detailled logging (in >= DEBUG_VERBOSE log level)
        """
        if obj:
            msg = '%s on %s' % (msg, str(obj))
        self._log.log(self.levels['DEBUG_VERBOSE'], msg)

if __name__ == '__main__':
    l = Logger()

    l.info("Hello World")
    l.debug("Argh")
