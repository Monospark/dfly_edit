import string

from dragonfly import *
from dragonfly_loader import Unit

from command_tracker import text, surround_rule, key


def common_symbols(t):
    return {
        t("dash"): "-",
        t("period"): ".",
        t("comma"): ",",
        t("backslash"): "\\",
        t("underscore"): "_",
        t("asterisk"): "*",
        t("colon"): ":",
        t("semicolon"): ";",
        t("slash"): "/",
        t("space"): " ",
        t("double_quote"): '"',
        t("single_quote"): "'",
        t("open_parenthesis"): "(",
        t("close_parenthesis"): ")",
        t("open_bracket"): "[",
        t("close_bracket"): "]",
        t("open_angle_bracket"): "<",
        t("close_angle_bracket"): ">",
        t("open_brace"): "{",
        t("close_brace"): "}",
        t("tab"): "    "
    }


def surroundings(t):
    return {
        t("angle_brackets"): ("<", ">"),
        t("brackets"): ("[", "]"),
        t("braces"): ("{", "}"),
        t("parentheses"): ("(", ")"),
        t("double_quotes"): ("\"", "\""),
        t("single_quotes"): ("'", "'"),
    }


def rare_symbols(t):
    return {
        t("at"): "@",
        t("hash"): "#",
        t("dollar"): "$",
        t("percent"): "%%",
        t("and"): "&",
        t("equal"): "=",
        t("plus"): "+",
        t("pipe"): "|",
        t("caret"): "^"
    }


def letters(t):
    letter_map = {}
    for char in string.lowercase:
        letter_map[char] = (t(char), string.capitalize(char))
    return letter_map


def all_symbols(t):
    all_symbols = {}
    for k, v in letters(t).iteritems():
        all_symbols[k] = v[0]
        all_symbols[t("capital") + " " + k] = v[1]
    for k, v in rare_symbols(t).iteritems():
        all_symbols[k] = v + " " + t("symbol")
    all_symbols.update(common_symbols(t))
    return all_symbols


class Symbols(Unit):

    def __init__(self):
        Unit.__init__(self, "symbols")

    def create_grammar(self, grammar, t):
        class SymbolRule(CompoundRule):
            spec = "<symbols>"
            extras = [Repetition(name="symbols", child=Choice("symbols", all_symbols), max=20)]

            def _process_recognition(self, node, extras):
                text(reduce(lambda x, y: x + y, extras["symbols"])).execute()

        class NumberRule(CompoundRule):
            spec = "number <m> [point <n>]"
            extras = [NumberRef("m", True), NumberRef("n", True)]

            def _process_recognition(self, node, extras):
                integer = extras["m"]
                number = str(integer)
                if "n" in extras:
                    floating_point = extras["n"]
                    number += "." + str(floating_point)

                text(number).execute()

        for key, value in surroundings.iteritems():
            grammar.add_rule(surround_rule(key, value[0], value[1]))
        grammar.add_rule(SymbolRule())
        grammar.add_rule(NumberRule())
        return True


def create_unit():
    return Symbols()
