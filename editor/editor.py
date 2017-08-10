from dragonfly import Clipboard, Key
from dfly_edit.command_tracker import key


class Editor:
    def mark_surrounded_text(self, start, end, include_delimiters=False):
        pass


class UnsupportedEditor(Editor):
    def mark_surrounded_text(self, start, end, include_delimiters=False):
        clipboard = Clipboard()
        saved_text = clipboard.get_system_text()
        clipboard.set_system_text('')
        left_counter = 0
        while left_counter < 50:
            key("s-left, c-c/3").execute()
            left_counter += 1
            if clipboard.get_system_text().startswith(start):
                break

        key("left").execute()
        move_right = left_counter
        if not include_delimiters:
            move_right -= 1
            key("right").execute()
        key("s-right:%s" % move_right).execute()

        right_counter = 0
        while right_counter < 50:
            key("s-right, c-c/3").execute()
            right_counter += 1
            if clipboard.get_system_text().endswith(end):
                break

        if not include_delimiters:
            key("s-left").execute()

        clipboard.set_text(saved_text)
        clipboard.copy_to_system()

    def indent(self, n):
        key("home/3, tab:%s" % n).execute()

    def unindent(self, n):
        key("s-tab:%s" % n).execute()

    def get_marked_text(self):
        clipboard = Clipboard()
        previous = clipboard.get_system_text()
        clipboard.set_system_text("")
        Key("c-c/3").execute()
        selected = clipboard.get_system_text()
        clipboard.set_text(previous)
        clipboard.copy_to_system()
        return selected or None


__editor = UnsupportedEditor()


def instance():
    return __editor
