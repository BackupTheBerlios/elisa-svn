#sample bnx using framework

from framework import application
from boxwidget import surface, treelevel, tree
from plugins import dvd, radio

if __name__ == '__main__':
    _main = application.BoxApplication()
    _main.MainWindow().SetBackgroundImage("testGL/themes/mce/COMMON.BACKGROUND.PNG")
    _main.MainWindow().SetBackColor(0,0,0)
    
    #_test = surface.Surface()
    #_test.SetSize(300, 40)
    #_test.SetLocation(120.0, 80.0, 1.0)
    #_test.SetBackgroundImage("testGL/themes/mce/COMMON.BUTTON.LEFT.FOCUS.PNG")
    #_main.MainWindow().AddSurface(_test)
    
    _main.AddPlugin(dvd.PluginTreeDvd())
    _main.AddPlugin(radio.PluginTreeRadio())
    _main.AddPlugin(dvd.PluginTreeDvd())
    _main.AddPlugin(radio.PluginTreeRadio())
    
    _maintree = tree.Tree(_main._rootlevel)
    #_maintree = treelevel.TreeLevel(_main._rootlevel)
    _maintree.SetSize(300, 40)
    _maintree.SetLocation(120.0, 150.0, 2.0)
    _main.MainWindow().AddSurface(_maintree)
    
    _main.Run()

    
