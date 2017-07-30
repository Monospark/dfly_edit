import formatter

from dragonfly import *
from dragonfly_loader import Unit
from formatter import format_map, FormatType


class Format(Unit):

    def __init__(self):
        Unit.__init__(self, "format")
        self.__fallback_format = FormatType.spokenForm

    def change_fallback_format(self, format_type):
        self.__fallback_format = format_type

    def create_grammar(self, g, t):
        rule = MappingRule(
            mapping={
                "set default format <format_type>": Function(lambda format_type: self.change_fallback_format(format_type)),
                "<format_type> <text>": Function(formatter.format_and_write_text),
                # "<text>": Function(format_input, format_type=fallback_format)
            },
            extras=[
                Dictation("text"),
                Choice("format_type", format_map),
            ]
        )
        g.add_rule(rule)
        return True


def create_unit():
    return Format()
