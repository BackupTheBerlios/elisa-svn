#Common file imported on all file
#Used for global variables


def GetApplication():
    return _Application
    
def _SetApplication(in_app):
    global _Application
    _Application = in_app
