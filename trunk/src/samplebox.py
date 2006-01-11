from framework import render, application
from plugins import dvd, radio

if __name__ == '__main__':
    _main = application.MainWindow()
    _main.AddPlugin(dvd.PluginTreeDvd(),0)
    _main.AddPlugin(radio.PluginTreeRadio())
    _main.Run()

    
