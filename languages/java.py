from dragonfly import *

import modules.util.formatter


def define_function(text):
    Text("function ").execute()
    modules.util.formatter.camel_case_text(text)
    Text("() {").execute()
    Key("left:3").execute()


rules = MappingRule(
    mapping={
        # Keywords:
        "abstract": Text("abstract "),
        "and": Text(" && "),
        "assign": Text(" = "),
        "(bool|boolean)": Text("boolean "),
        "break": Text("break"),
        "case": Text("case "),
        "catch": Text("catch () {") + Key("left:3"),
        "class": Text("class "),
        "comment": Text("// "),
        "continue": Text("continue"),
        "close comment": Text(" */"),
        "do": Text("do {"),
        "equals": Text(" == "),
        "else": Text("else"),
        "else if": Text("else if () {") + Key("left:3"),
        "extends ": Text("extends "),
        "final": Text("final "),
        "for": Text("for () {") + Key("left:3"),
        "false": Text("false"),
        "finally": Text("finally {") + Key("enter"),
        "greater than": Text(" > "),
        "greater equals": Text(" >= "),
        "if": Text("if ("),
        "if <text>": Text("if (%(text)s) {") + Key("left:3"),
        "instanceof": Text("instanceof "),
        "(int|I N T)": Text("int "),
        "less than": Text(" < "),
        "less equals": Text(" <= "),
        "(line end|end line)": Key("end") + Text(";") + Key("enter"),
        "(minus|subtract|subtraction)": Text(" - "),
        "(minus|subtract|subtraction) equals": Text(" -= "),
        "modulo": Key("space") + Key("%%") + Key("space"),
        "new": Text("new "),
        "not (equal|equals) [to]": Text(" != "),
        "null": Text("null"),
        "open comment": Text("/* "),
        "or": Text(" || "),
        "(plus|add|addition)": Text(" + "),
        "(plus|add|addition) equals": Text(" += "),
        "private": Text("private "),
        "protected": Text("protected "),
        "public": Text("public "),
        "return": Text("return "),
        "static": Text("static "),
        "string": Text("String"),
        "switch": Text("switch () {") + Key("left:3"),
        "this": Text("this"),
        "throw": Text("throw "),
        "true": Text("true"),
        "try": Text("try {") + Key("enter"),
        "toString": Text("toString()") + Key("left"),
        "while": Text("while () {") + Key("left:3"),
    },
    extras=[
        IntegerRef("n", 1, 100),
        Dictation("text"),
    ],
    defaults={
        "n": 1
    }
)


def create_grammar():
    grammar = Grammar("java")
    grammar.add_rule(rules)
    return grammar, False
