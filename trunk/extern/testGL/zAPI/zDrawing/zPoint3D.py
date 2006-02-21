class Point3D(object):

    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y 
        self.z = z

    def __str__(self):
        return 'Point3D(' + str(self.x) + ', ' + str(self.y) + ', ' + str(self.z) + ')'
         
