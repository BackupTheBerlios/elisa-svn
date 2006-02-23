#sample bnx using framework
import os

#os.environ['PYCHECKER_DISABLED'] = '1'
# 
# -F /home/pnormand/Projects/Elisa/trunk/misc/pycheckerrc"
os.environ['PYCHECKER'] = " -q -b ['configobj', 'validate']"

import pychecker.checker




from elisa.framework import application, log
import time

class BoxApplication(application.Application):
    
    def run(self):
        logger = log.Logger()

        while 1:
            try:
                logger.info("i'm running")
                time.sleep(0.5)
            except:
                self.close()
                break

if __name__ == '__main__':
    main = BoxApplication()
    
    main.load_plugins()

    main.run()

    
