from dragonfly import Clipboard, MappingRule, Function
from dragonfly import Key

import nesting
from command_tracker import text, sequence, func
from edit import edit, Action

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


def create_surround_rule(name, start, end):
    def surround():
        selected_text = get_selected_text()
        to_write = start + selected_text + end
        text(to_write).execute()

    return MappingRule(mapping={
        "empty " + name: text(),
        name: sequence(
                text(start + end),
                func(nesting.instance().add_nesting_level(len(end)))
            ),
        "surround " + name: Function(surround)
    })
