from dragonfly import Grammar, Function, MappingRule, Key, Mouse
import win32api, win32con

from dragonfly_loader import Unit


class MouseState(Unit):

    def __init__(self):
        Unit.__init__(self, "mouse_state")
        self.__is_cursor_following_mouse = False
        self.__is_marking = False

    def update_cursor(self):
        if self.__is_cursor_following_mouse:
            MouseState("left/3").execute()

    def stop_marking(self):
        if self.__is_marking:
            self.__is_marking = False
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def __toggle_marking(self):
        if self.__is_marking:
            self.stop_marking()
        else:
            self.__is_marking = True
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)

    def __toggle_cursor(self):
        self.__is_cursor_following_mouse = not self.__is_cursor_following_mouse

    def load_data(self, data):
        self.__is_cursor_following_mouse = data["is_cursor_following_mouse"]
        self.__is_marking = data["is_marking"]

    def save_data(self):
        data = {}
        data["is_cursor_following_mouse"] = self.__is_cursor_following_mouse
        data["is_marking"] = self.__is_marking
        return data

    def create_grammar(self, g, t):
        g.add_rule(MappingRule(mapping={
            "mark": Function(self.__toggle_marking),
            "cursor": Function(self.__toggle_cursor)
        }))
        return True

__unit = MouseState()


def instance():
    return __unit


def create_unit():
    return __unit
