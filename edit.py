from dragonfly import CompoundRule, Choice, MappingRule, IntegerRef
from dragonfly_loader import Unit

from command_tracker import mouse, sequence, key, func, reversible
from editor import editor
from mouse_state import mouse_state


def _actions(t):
    return {
        t("cut"): Action.cut,
        t("copy"): Action.copy,
        t("replace"): Action.replace,
        t("delete"): Action.delete,
        t("select"): Action.select,
    }


def _scopes(t):
    return {
        t("all"): Scope.all,
        t("line"): Scope.line,
        t("line content"): Scope.line_content,
        t("this"): Scope.this,
        t("string"): Scope.string,
        t("string content"): Scope.string_content,
        t("letter"): Scope.letter,
        t("left"): Scope.left,
        t("right"): Scope.right
    }


def _edit_rule(t):
    class NormalActionRule(CompoundRule):
        spec = "<action> [<scope>]"
        extras = [
            Choice("action", _actions(t)),
            Choice("scope", _scopes(t))
        ]

        def _process_recognition(self, node, extras):
            action = extras["action"]
            scope = None
            if "scope" in extras:
                scope = extras["scope"]
            edit(action, scope)

    return NormalActionRule()


def _miscellaneous_rule(t):
    def pre_action():
        if not mouse_state.stop_marking():
            mouse_state.update_cursor()

    return MappingRule(
        mapping={
            t("select"): func(edit, action=Action.select, scope=Scope.this),
            t("delete"): sequence(func(pre_action), key("del/3:%(n)d")),
            t("backspace"): sequence(func(pre_action), key("backspace/1:%(n)d")),
            t("paste"): sequence(func(pre_action), key("c-v/3")),
            t("new_line"): sequence(func(pre_action), key("end/3, enter/3:%(n)d")),
            t("new_line_here"): sequence(func(pre_action), key("enter/3:%(n)d")),
            t("indent"): reversible(func(lambda: editor.instance().indent()),
                                    func(lambda: editor.instance().unindent())),
            t("unindent"): reversible(func(lambda: editor.instance().unindent()),
                                      func(lambda: editor.instance().indent())),
            t("undo"): key("c-z/3"),
            t("redo"): key("c-y/3")
        },
        extras=[
            IntegerRef("n", 1, 100)
        ],
        defaults={
            "n": 1,
        }
    )


class Action:
    cut = key("c-x/3")
    copy = key("c-c/3, left/3")
    replace = key("c-v/3")
    delete = key("del/3")
    select = None


class Scope:
    all = key("c-a/3")
    line = mouse("left/3, left/3, left/3")
    line_content = sequence(mouse("left/3"), key("home/3, s-end/3"))
    this = mouse("left/3, left/3")
    string = func(lambda: editor.instance().mark_surrounded_text("\"", "\"", True))
    string_content = func(lambda: editor.instance().mark_surrounded_text("\"", "\"", False))
    letter = sequence(mouse("left/3"), key("s-right/3"))
    left = sequence(mouse("left/3"), key("s-home/3"))
    right = sequence(mouse("left/3"), key("s-end/3"))


def edit(action, scope):
    mouse_state.stop_marking()

    if scope is not None:
        scope.execute()

    if action is not None:
        action.execute()


class Edit(Unit):
    def __init__(self, grammar_name="edit"):
        Unit.__init__(self, grammar_name)

    def create_grammar(self, g, t):
        g.add_rule(_miscellaneous_rule(t))
        g.add_rule(_edit_rule(t))
        return True


def create_unit():
    return Edit()
