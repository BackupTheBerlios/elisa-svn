#sample bnx using framework

from elisa.framework import application

class BoxApplication(application.Application):
    pass

if __name__ == '__main__':
    main = BoxApplication()
    
    main.load_plugins()

    main.run()

    
