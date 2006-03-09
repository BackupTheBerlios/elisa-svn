from elisa.skins.mce_skin.mce_button_menu import MCEButtonMenu
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
                    if self._current_widget_rank < len(self._widget_stack):
                        self._widget_stack[self._current_widget_rank-1].animate_hide()
                        self._current_widget_rank += 1
                        self._widget_stack[self._current_widget_rank-1].animate_show()
                if message.get_simple_event() == events.SE_BACK:
                    if self._current_widget_rank > 1:
                        self._widget_stack[self._current_widget_rank-1].animate_hide()
                        self._current_widget_rank -= 1
                        self._widget_stack[self._current_widget_rank-1].animate_show()
                    
