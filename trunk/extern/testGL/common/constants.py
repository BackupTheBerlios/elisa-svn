def GetVideoMode():
    return 'OpenGL'


def GetWindowSize():
    return (800,600)

MainForm = None
def GetForm():
    global MainForm
    return MainForm
 
def _SetForm(f):
    global MainForm
    MainForm = f
