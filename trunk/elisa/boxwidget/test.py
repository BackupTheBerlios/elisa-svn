import window, surface, fontsurface

class w (window.Window):
    
    def __init__(self):
        window.Window.__init__(self)
        
        f = fontsurface.FontSurface()
        self.add_surface(f)
        
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

        self.t = surface.Surface('s')
        self.add_surface(self.t)
        self.t.set_location(self.x,self.y + 300,self.z)
        
        self.is_d = False
        
    def refresh(self):
        window.Window.refresh(self)  
        #self.x += 1    
        #self.s.set_location(self.x,self.y,self.z)
        if self.is_d==False:
            self.is_d = True
            self.remove_surface(self.s)

if __name__ == '__main__':
    t = w()
    t.run()
