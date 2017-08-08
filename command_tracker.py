from dragonfly import Function, ActionBase, ActionError, Rule, Compound, Key, Text, Mouse, MappingRule, IntegerRef, \
    Grammar

import mouse_state
import nesting

previous_commands = []
undoed_commands = []

current_command = None


def add_nesting_level(level):
    return reversible(func(mouse_state.instance().add_nesting_level, level=level), func(mouse_state.instance().remove_nesting_level))


def __on_mouse_input():
    mouse_state.instance().stop_marking()
    nesting.instance().clear_nesting_levels()


def key(action):
    return IrreversibleAction(Key(action))


def func(f, **kwargs):
    return IrreversibleAction(Function(f, **kwargs))


def mouse(action):
    return irreversible(Function(__on_mouse_input) + Mouse(action))


def text(text):
    text_command = _PositionalText(text)
    reverse_command = Function(lambda: text_command.reverse())
    return _ReversibleAction(text_command, reverse_command)


def __add_actions(a1, a2):
    if isinstance(a1, _ReversibleAction) and isinstance(a2, _ReversibleAction):
        return _ReversibleAction(a1.action + a2.action, a2.reverse_action + a1.reverse_action)
    else:
        return IrreversibleAction(a1.action + a2.action)


def sequence(*actions):
    action = reduce(__add_actions, actions)
    reverse_action = reduce(__add_actions, reversed(actions))
    return _ReversibleAction(action, reverse_action)


def reversible(action, reverse_action):
    return _ReversibleAction(action, reverse_action)


class _TrackedAction(ActionBase):
    def __init__(self, action):
        self.action = action
        ActionBase.__init__(self)

    def execute(self, data=None):
        try:
            global current_command
            is_top_level_command = current_command is None
            if is_top_level_command:
                current_command = self

            self.action.execute(data)

            if is_top_level_command:
                current_command = None
                global previous_commands
                self.on_execute()
        except ActionError, e:
            self._log_exec.error("Execution failed: %s" % e)
            return False

    def on_execute(self):
        raise NotImplementedError()


class _ReversibleAction(_TrackedAction):

    def __init__(self, action, reverse_action):
        self.reverse_action = reverse_action
        _TrackedAction.__init__(self, action)

    def on_execute(self):
        previous_commands.append((self, data))


def irreversible(action):
    return IrreversibleAction(action)


class IrreversibleAction(_TrackedAction):

    def __init__(self, action):
        _TrackedAction.__init__(self, action)

    def on_execute(self):
        global previous_commands
        previous_commands = []
        global undoed_commands
        undoed_commands = []


class _PositionalText(Text):

    def __init__(self, spec=None, static=False, pause=Text._pause_default, autofmt=False):
        Text.__init__(self, spec=spec, static=static, pause=pause, autofmt=autofmt)

    def _execute_events(self, events):
        if nesting.instance().get_complete_nesting_level() == 0:
            mouse_state.instance().update_cursor()
        return Text._execute_events(self, events)

    def reverse(self):
        lines = self._spec.split("\n")
        if len(lines) == 1:
            Key("backspace/1:%d" % len(self._spec)).execute()
        else:
            for i in range(1, len(lines)):
                Key("s-home/1:2").execute()
                Key("s-left/1").execute()
                Key("delete/1").execute()

            Key("backspace/1:%d" % len(lines[0])).execute()


def undo_command():
    if len(previous_commands) != 0:
        last_command, data = previous_commands.pop()
        last_command.reverse_action.execute(data)


data = {
    "undo [last] command": Function(undo_command)
}


class CommandRule(MappingRule):
    mapping = data
    extras = [
        IntegerRef("n", 1, 100)
    ]
    defaults = {
        "n": 1,
    }


def create_grammar():
    grammar = Grammar("commands")
    grammar.add_rule(CommandRule())
    return grammar, True
