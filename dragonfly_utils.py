from dragonfly import MappingRule, Function

from command_tracker import text, sequence, func, add_nesting_level
from editor import editor


def create_surround_rule(name, start, end):
    def surround():
        selected_text = editor.instance().get_marked_text()
        to_write = start + selected_text + end
        text(to_write).execute()

    return MappingRule(mapping={
        "empty " + name: text(start + end),
        name: sequence(
            text(start + end),
            add_nesting_level(len(end))
        ),
        "surround " + name: Function(surround)
    })
