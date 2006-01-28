from binding import testgl

_Engine = "testGL"
    
def _SetRenderer(engine):
    """
    set engine used by the class factory
    @param in_WidgetEngine: widget engine used. can be "testGL"
    @type in_WidgetEngine: string
    """
    testgl._Engine = "testGL"
        
def _WindowFactory():
    """
    return window object of select render engine
    """ 
    if _Engine == "testGL":
        return testgl.zWindow

def _SurfaceFactory():
    """
    return surface object of select render engine
    @param in_WidgetEngine: widget engine used. can be "testGL"
    @type in_WidgetEngine: string
    """
    if _Engine == "testGL":
        return testgl.zSurface

def _VideoSurfaceFactory():
    """
    return surface object of select render engine
    @param in_WidgetEngine: widget engine used. can be "testGL"
    @type in_WidgetEngine: string
    """
    if _Engine == "testGL":
        return testgl.zVideoSurface
        
def _EventsManagerFactory():
    """
    return surface object of select render engine
    @param in_WidgetEngine: widget engine used. can be "testGL"
    @type in_WidgetEngine: string
    """
    if _Engine == "testGL":
        return testgl.zEventsManager 
