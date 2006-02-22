#sample bnx using framework

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

    
