from dragonfly import Clipboard
from dragonfly import Key


__rule_counter = 0


def get_unique_rule_name():
    global __rule_counter
    __rule_counter += 1
    return str(__rule_counter)


def get_selected_text():
    clipboard = Clipboard()
    previous = clipboard.get_system_text()
    clipboard.set_system_text("")
    Key("c-c/3").execute()
    selected = clipboard.get_system_text()
    clipboard.set_text(previous)
    clipboard.copy_to_system()
    return selected


def set_clipboard(text):
    clipboard = Clipboard()
    clipboard.set_text(text)
    clipboard.copy_to_system()
