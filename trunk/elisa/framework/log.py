
import logging
import sys, os
import copy

# Python 2.3 compat
if sys.version_info[:2] == (2,3):
    logging.getLoggerClass = lambda : logging._loggerClass
    
    def basicConfig(stream=None):
        """
        Ripped from logging.__init__ and adapted to support stream
        keyword argument.
        """
        root = logging.getLogger()
        if len(root.handlers) == 0:
            hdlr = logging.StreamHandler(strm=stream)
            fmt = logging.Formatter(logging.BASIC_FORMAT)
            hdlr.setFormatter(fmt)
            root.addHandler(hdlr)
           
    logging.basicConfig = basicConfig
    
logger = None

class CustomFile:

    def __init__(self, f):
        self.f = f
        self.enable()
        
    def enable(self):
        self.do_write = True

    def disable(self):
        self.do_write = False
        
    def write(self, data):
        if self.do_write:
            self.f.write(data)

    def __getattr__(self, attr):
        return getattr(self.f, attr)
 
class ElisaLogRecord(logging.LogRecord):
    """ Custom log record """
    
    def __init__(self, *args, **kwargs):
        logging.LogRecord.__init__(self, *args, **kwargs)
        self.classname = calling_class_name()
        self.funcname = calling_func_name()
        self.argnames = calling_args()
        
class ElisaLogger(logging.getLoggerClass()):
    """ Custom logger that uses our log record """
    
    def makeRecord(self, name, lvl, fn, lno, msg, args, exc_info):
        if lvl != logging.INFO:
            record_class = ElisaLogRecord
        else:
            record_class = logging.LogRecord
        return record_class(name, lvl, fn, lno, msg, args, exc_info)
                            
# Register our logger
logging.setLoggerClass(ElisaLogger)

class ElisaFormatter(logging.Formatter):

    def set_alternate_formatter(self, fmter):
        self._alt_format = fmter

    def get_alternate_formatter(self):
        return self._alt_format

    def format(self, record):
        if isinstance(record,ElisaLogRecord):
            formatted = logging.Formatter.format(self, record)
        else:
            formatted = self.get_alternate_formatter().format(record)
        return formatted

def calling_class_name():
    """ Calling class name """
    f = calling_frame()
    args = copy.copy(f.f_locals)
    #import pdb; pdb.set_trace()
    instance = args.get('self','')
    name = ''
    if instance:
        name = '%s.' % instance.__class__.__name__
    return name

def calling_func_name():
    """ Calling function name """
    f = calling_frame()
    return f.f_code.co_name

def calling_args():
    """ Calling function arguments as dictionnary """
    f = calling_frame()
    args = copy.copy(f.f_locals)
    if 'self' in args.keys():
        del args['self']
    if args:
        args_values = 'args: '
        args_values += ', '.join([ '%s=%s' % (a,v) for (a,v) in args.iteritems() ])
    else:
        args_values = ''
    return args_values

def calling_frame():
    """ Calling sys frame """
    f = sys._getframe()

    while True:
        if is_user_source_file(f.f_code.co_filename):
            return f
        f = f.f_back

def is_user_source_file(filename):
    return os.path.normcase(filename) not in (_srcfile, logging._srcfile)

def _current_source_file():
    base, ext = os.path.splitext(__file__)
    if ext in ('.pyc', '.pyo'):
        return '%s.py' % base
    else:
        return __file__

_srcfile = os.path.normcase(_current_source_file())

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

    FIXME : Line insered in double in logfile
    """

    levels = {'DEBUG_DETAILLED': 5,
              'DEBUG_VERBOSE': 1
              }

    stderr = CustomFile(sys.stderr)


    def __init__(self):
        common = '%(asctime)s.%(msecs)-4d %(levelname)-8s '
        default_format = common + '%(message)s'
        format = common + '[%(classname)s%(funcname)s] %(message)s %(argnames)s'
        datefmt = '%d/%m/%Y %H:%M:%S'
        fname = 'elisa.log'

        formatter = ElisaFormatter(format, datefmt)
        formatter.set_alternate_formatter(logging.Formatter(default_format, datefmt))
        handler = logging.FileHandler(fname)
        handler.setFormatter(formatter)

        for name, lvl in self.levels.iteritems():
            logging.addLevelName(lvl, name)

        self._log = logging.getLogger('Elisa')
        self._log.addHandler(handler)

        self.set_level('DEBUG_DETAILLED')

        logging.basicConfig(stream=self.stderr)
        
        root = logging.getLogger()
        handler = root.handlers[0]
        handler.setFormatter(formatter)

        self.enable_console_output()
        
    def enable_console_output(self):
        """ enable log output to stderr """
        self.stderr.enable()
        self.stderr.flush()
        
    def disable_console_output(self):
        """ disable log output to stderr """
        self.stderr.disable()
        self.stderr.flush()
        
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
        self._log.log(logging.DEBUG, msg)

    def debug_detailled(self, msg, obj=None):
        """ Log verbose functional data (in >= DEBUG_DETAILLED log level)
        """
        self._log.log(self.levels['DEBUG_DETAILLED'], msg)

    def debug_verbose(self, msg, obj=None):
        """ Detailled logging (in >= DEBUG_VERBOSE log level)
        """
        self._log.log(self.levels['DEBUG_VERBOSE'], msg)

def Logger():
    global logger
    if not logger:
        logger = _Logger()
    return logger

if __name__ == '__main__':
    l = Logger()

    l.info("Hello World")
    l.debug("Argh")
