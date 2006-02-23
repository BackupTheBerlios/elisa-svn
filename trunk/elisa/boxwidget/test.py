import window, surface, fontsurface

class w (window.Window):
    
    def __init__(self):
        window.Window.__init__(self)
        self.s = surface.Surface('s')
        (self.x,self.y,self.z) =  100,100,0
        self.s.set_location(self.x,self.y,self.z)
        self.s.set_back_color(255,0,0)
        s2 = surface.Surface('s2')
        s2.set_back_color(255,255,0)
        s2.set_location(100,100,0)
        s3 = surface.Surface('s3')
        s3.set_back_color(255,0,255)
        s3.set_location(100,100,0)
        self.s.add_surface(s2)
        s2.add_surface(s3)
        self.add_surface(self.s)
        f = fontsurface.FontSurface()
        #f.set_text("test")
        self.add_surface(f)
  
    def refresh(self):
        window.Window.refresh(self)  
        #self.x += 1    
        #self.s.set_location(self.x,self.y,self.z)
t = w()
t.run()
