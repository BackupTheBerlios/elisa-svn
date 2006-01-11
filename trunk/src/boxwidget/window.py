import widget

class _WindowBase(widget._WidgetBase):
    """
    Main window boxwidget base class
    do not use directly
    """
    
    def __init__(self):
        widget._WidgetBase.__init__(self)

    
    def Refresh(self):
        """
        refresh complete window (draw current frame)
        @return: False if loop stop required, True if noting.
        """
        return True
          
def WindowFactory( in_WidgetEngine="testGL" ):
    """
    return window object of select render engine
    @param in_WidgetEngine: widget engine used. can be "testGL"
    @type in_WidgetEngine: string
    """
    
    return zWindow()
    
class zWindow(_WindowBase):
    """
    Binding class for testGL renderEngine
    """

    def __init__(self):
        _WindowBase.__init__(self)
    
    def Refresh(self):
        _WindowBase.Refresh(self)
            
        return True
        
    def SetBackColor(self, Red, Green, Blue): pass
