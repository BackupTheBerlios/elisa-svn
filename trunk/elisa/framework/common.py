_application = None

def _set_application(app):
    global _application
    _application = app
    
def get_application():
    global _application
    return _application
    
