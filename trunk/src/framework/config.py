class Config(object):
    
    def __init__(self):
        self._config = {}
        self.SetDefaultConfig()
        
    def Get(self, key):
        return self._config[key]
        
    def SetDefaultConfig(self):
        self._config["RenderEngine"] = "testGL"
