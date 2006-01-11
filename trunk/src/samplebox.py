#sample bnx using framework

from framework import application
from plugins import dvd, radio

if __name__ == '__main__':
    _main = application.BoxApplication()
    _main.AddPlugin(dvd.PluginTreeDvd(),0)
    _main.AddPlugin(radio.PluginTreeRadio())
    _main.Run()

    
