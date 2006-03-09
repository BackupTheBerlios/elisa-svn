from elisa.skins.mce_skin.mce_button_menu import MCEButtonMenu
from elisa.skins.mce_skin.mce_browser import MCEBrowser
from elisa.boxwidget import surface, events

class MCESkin(surface.Surface):

    def __init__(self, root_menuitem_list, name="mce skin"):
        surface.Surface.__init__(self, name)
        self._root_menuitem_list = root_menuitem_list
        self.set_size(0.0, 0.0)
        self._widget_stack = []
        self._widget_stack.append(MCEButtonMenu(root_menuitem_list))
        self._current_widget_rank = 1
        self.add_surface(self._widget_stack[0])
        
    def on_message(self, receiver, message, sender):
        self._logger.debug('MCESkin.on_message(' + str(message) + ')', self)
        if self.visible(True):
            
            if isinstance(message, events.InputEvent):
                if message.get_simple_event() == events.SE_OK:
                    _current_widget = self._widget_stack[self._current_widget_rank-1]
                    _current_menuitem = _current_widget.get_current_menuitem()
                    if _current_menuitem.has_items():
                        _new_widget = MCEBrowser(_current_menuitem.get_items())
                        self._widget_stack[self._current_widget_rank-1].animate_before_hide()
                        self._widget_stack.append(_new_widget)
                        self._current_widget_rank +=1
                        self._widget_stack[self._current_widget_rank-1].animate_before_show()
                if message.get_simple_event() == events.SE_BACK:
                    if self._current_widget_rank >1:
                        _previous_widget = self._widget_stack[self._current_widget_rank-1]
                        _previous_widget.animate_before_hide()
                        self._widget_stack.remove(_previous_widget)
                        self._current_widget_rank -=1
                        self._widget_stack[self._current_widget_rank-1].animate_before_show()
                        
