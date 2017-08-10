
from dragonfly import *

from dfly_edit.command_tracker import add_nesting_level, text, sequence
from dfly_edit.dictation import dictation
from dfly_edit.dragonfly_utils import create_surround_rule
from dfly_edit.formatter import FormatType, format_text, format_snake_case
from dfly_edit.nesting import nesting


class LambdaRule(CompoundRule):
    spec = "[no-param] lambda"

    def _process_recognition(self, node, extras):
        has_parameters = node.words()[0] != "no-param"
        string = "lambda"
        if not has_parameters:
            string += ":"
        else:
            string += " :"
        text(string).execute()
        if has_parameters:
            nesting.add_nesting_level(1)


class DefineClassRule(CompoundRule):
    spec = "(def|define) [child] class [<text>]"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        is_child = node.words()[1] == "child"
        string = "class "
        if "text" in extras:
            string += format_text(extras["text"], FormatType.pascalCase)

        if is_child:
            string += "()"
        text(string).execute()
        if is_child:
            nesting.add_nesting_level(1)
            if "text" not in extras:
                nesting.add_nesting_level(1)


class DefineVariableRule(CompoundRule):
    spec = "(def|define) (variable|constant) [<text>] [equals]"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        type = node.words()[1]
        string = ""
        if "text" in extras:
            if type == "variable":
                name = format_snake_case(extras["text"])
            else:
                name = format_text(extras["text"],
                                             [FormatType.snakeCase, FormatType.upperCase])

            string = name

        string += " = "
        text(string).execute()
        if "text" not in extras:
            nesting.add_nesting_level(3)


class DefineFunctionRule(CompoundRule):
    spec = "(def|define) [no-param] (constructor | ((function | method) [<text>]))"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        has_parameters = node.words()[1] != "no-param"
        type = node.words()[1 if has_parameters else 2]
        string = "def "

        name = None
        if type == "constructor":
            name = "__init__"
        elif "text" in extras:
            name = format_snake_case(extras["text"])

        if name is not None:
            string += name

        parameters_start = "("
        if type in ("method", "constructor"):
            parameters_start += "self, " if has_parameters else "self"

        string += parameters_start + ")"
        text(string).execute()
        if has_parameters:
            nesting.add_nesting_level(1)
        if name is None:
            name_offset = len(parameters_start)
            if not has_parameters:
                name_offset += 1
            nesting.add_nesting_level(name_offset)


class CallFunctionRule(CompoundRule):
    spec = "call [empty] (constructor | function <text>) [on]"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        is_constructor = "text" not in extras
        name = "__init__" if is_constructor else format_text(extras["text"], FormatType.snakeCase)
        has_arguments = node.words()[1] != "empty"
        has_period = node.words()[len(node.words()) - 1] == "on"
        string = "." if has_period else ""
        string += name
        string += "()"
        text(string).execute()

        if has_arguments:
            nesting.add_nesting_level(1)


class CreateObjectRule(CompoundRule):
    spec = "create [empty] <text>"
    extras = [Dictation("text")]

    def _process_recognition(self, node, extras):
        has_arguments = node.words()[1] != "empty"
        string = format_text(extras["text"], FormatType.pascalCase)
        string += "()"
        text(string).execute()

        if has_arguments:
            nesting.add_nesting_level(1)


def ternary():
    text(" if  else ").execute()
    nesting.add_nesting_level(6)
    nesting.add_nesting_level(4)


def list_comprehension():
    text("[ for  in ]").execute()
    nesting.add_nesting_level(1)
    nesting.add_nesting_level(4)
    nesting.add_nesting_level(5)


def format_variable(name, prefix="", suffix=""):
    full_name = format_text(name, FormatType.snakeCase)
    text(prefix + full_name + suffix).execute()


def class_name(name):
    full_name = format_text(name, FormatType.pascalCase)
    text(full_name).execute()


rules = MappingRule(
    mapping={
        # Commands and keywords:
        "and": text(" and "),
        "as": text("as "),
        "assign": text(" = "),
        "assert": text("assert "),
        "break": text("break"),
        "comment": text("# "),
        "class": text("class "),
        "continue": text("continue"),
        "del": text("del "),
        "divided by": text(" / "),
        "string <text>": text("\"%(text)s\""),
        "(var|variable) <text>": Function(format_variable),
        "(arg|argument) <text>": Function(format_variable, suffix="="),
        "private": text("__"),
        "private <text>": Function(format_variable, prefix="__"),
        "protected": text("_"),
        "protected <text>": Function(format_variable, prefix="_"),
        "class <text>": Function(class_name),
        "else": text("else:\n"),
        "except": text("except "),
        "exec": text("exec "),
        "(el if|else if)": text("elif "),
        "equals": text(" == "),
        "false": text("False"),
        "finally": text("finally:\n"),
        "for": text("for "),
        "from": text("from "),
        "global ": text("global "),
        "global <text>": Function(format_variable, prefix="global "),
        "greater than": text(" > "),
        "greater [than] equals": text(" >= "),
        "if": text("if "),
        "if not": text("if not "),
        "in": text(" in "),
        "is": text(" is "),
        "is not": text(" is not "),
        "is instance": sequence(text("isinstance(, )"), add_nesting_level(1), add_nesting_level(2)),
        "import": text("import "),
        "lambda": text("lambda "),
        "less than": text(" < "),
        "less [than] equals": text(" <= "),
        "list comprehension": Function(list_comprehension),
        "(minus|subtract|subtraction)": text(" - "),
        "(minus|subtract|subtraction) equals": text(" -= "),
        "modulo": text(" %% "),
        "not": text(" not "),
        "not equals": text(" != "),
        "none": text("None"),
        "or": text(" or "),
        "pass": text("pass"),
        "(plus|add|addition)": text(" + "),
        "(plus|add|addition) equals": text(" += "),
        "raise": text("raise "),
        "return": text("return "),
        "return nothing": text("return"),
        "self": text("self"),
        "ternary": Function(ternary),
        "true": text("True"),
        "try": text("try:\n"),
        "times": text(" * "),
        "with": text("with "),
        "while": text("while "),
        "yield": text("yield "),

        "start block": Function(nesting.clear_nesting_levels) + Key("end") + text(":\n"),
        "new entry": Function(nesting.clear_nesting_levels) + Key("end") + text(",\n"),
        "next [(arg|argument)]": Function(nesting.remove_nesting_levels) + text(", "),
        "value": Function(nesting.remove_nesting_levels) + text(": "),

        # Some common modules.
        "datetime": text("datetime"),
        "(io|I O)": text("io"),
        "logging": text("logging"),
        "(os|O S)": text("os"),
        "(pdb|P D B)": text("pdb"),
        "(re|R E)": text("re"),
        "(sys|S Y S)": text("sys"),
        "S Q lite 3": text("sqlite3"),
        "subprocess": text("subprocess"),
    },
    extras=[
        Dictation("text"),
    ]
)

surroundings = {
    "string": ("\"", "\"")
}


def create_grammar():
    grammar = Grammar("python")
    grammar.add_rule(rules)
    grammar.add_rule(LambdaRule())
    grammar.add_rule(DefineClassRule())
    grammar.add_rule(DefineFunctionRule())
    grammar.add_rule(DefineVariableRule())
    grammar.add_rule(CallFunctionRule())
    grammar.add_rule(CreateObjectRule())
    grammar.add_rule(create_surround_rule("string", "\"", "\""))
    grammar.add_rule(create_surround_rule("to string", "str(", ")"))
    grammar.add_rule(create_surround_rule("list", "list(", ")"))
    grammar.add_rule(create_surround_rule("dictionary", "dict(", ")"))
    grammar.add_rule(create_surround_rule("int", "int(", ")"))
    grammar.add_rule(create_surround_rule("length", "len(", ")"))
    grammar.add_rule(create_surround_rule("print", "print(", ")"))
    grammar.add_rule(create_surround_rule("reversed", "reversed(", ")"))
    grammar.add_rule(create_surround_rule("range", "range(", ")"))
    grammar.add_rule(create_surround_rule("doc string", '"""', '"""'))
    dictation.add_dictation_incompatible_grammar(grammar)
    return grammar, False
