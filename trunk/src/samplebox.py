#sample bnx using framework

from framework import application
from boxwidget import surface, treelevel, tree
from plugins import dvd, radio, movies, pictures

if __name__ == '__main__':
    _main = application.BoxApplication()
    #_main.MainWindow().SetBackgroundImage("testGL/themes/mce/COMMON.BACKGROUND.PNG")
    _main.SetBackColor(0,0,0)
    
    #_test = surface.Surface()
    #_test.SetSize(300, 40)
    #_test.SetLocation(120.0, 80.0, 1.0)
    #_test.SetBackgroundImage("testGL/themes/mce/COMMON.BUTTON.LEFT.FOCUS.PNG")
    #_main.MainWindow().AddSurface(_test)
    
    _main.AddPlugin(pictures.PluginTreePictures())
    _main.AddPlugin(movies.PluginTreeMovies())
    _main.AddPlugin(radio.PluginTreeRadio())
    _main.AddPlugin(dvd.PluginTreeDvd())
        
    _main.Run()

    
