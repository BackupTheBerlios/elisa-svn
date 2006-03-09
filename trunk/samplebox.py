#sample bnx using framework
import os
import sys

# set this to 0 to enable PyChecker (time-consuming!)
os.environ['PYCHECKER_DISABLED'] = '1'
os.environ['PYCHECKER'] = " -q -b ['configobj', 'validate']"

try:
    import pychecker.checker
except ImportError:
    pass


from elisa.framework import application

class BoxApplication(application.Application): pass

if __name__ == '__main__':

    args = sys.argv[1:]

    if len(args):
        config_file = args[0]
        main = BoxApplication(config_file)
    else:
        main = BoxApplication()
        
    main.run()

    
