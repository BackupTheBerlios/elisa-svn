#sample bnx using framework
import os

# set this to 0 to enable PyChecker (time-consuming!)
os.environ['PYCHECKER_DISABLED'] = '1'
os.environ['PYCHECKER'] = " -q -b ['configobj', 'validate']"

try:
    import pychecker.checker
except ImportError:
    pass


from elisa.framework import application, log
import time

class BoxApplication(application.Application): pass

if __name__ == '__main__':
    main = BoxApplication()

    main.run()

    
