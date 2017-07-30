from dragonfly import MappingRule
from dragonfly_loader import Unit

from command_tracker import func


class Dictation(Unit):

    def __init__(self):
        Unit.__init__(self, "dictation")
        self.__is_dictating = False
        self.__dictation = None
        self.__dictation_incompatible_grammars = []
        self.__disabled_dictation_grammars = []

    @property
    def is_dictating(self):
        return self.__is_dictating

    def __start_dictating(self):
        self.__is_dictating = True
        for grammar in self.__dictation_incompatible_grammars:
            if grammar.enabled:
                grammar.disable()
                self.__disabled_dictation_grammars.append(grammar)

    def append_dictation(self, text):
        if self.__dictation is None:
            self.__dictation = text
        else:
            split_position = len(self.__dictation) - get_complete_nesting_level()
            prefix = self.__dictation[:split_position]
            suffix = self.__dictation[split_position:]
            self.__dictation = prefix + text + suffix

    def __stop_dictating(self):
        self.__is_dictating = False
        clear_nesting_levels()
        print(self.__dictation)
        self.__dictation = None

        for grammar in self.__disabled_dictation_grammars:
            grammar.enable()

            self.__disabled_dictation_grammars[:] = []

    def create_grammar(self, g, t):
        g.add_rule(MappingRule(mapping={
            "dictate": func(lambda: self.__start_dictating),
            "finish": func(lambda: self.__stop_dictating)
        }))
        return True


__unit = Dictation()


def is_dictating():
    return __unit.is_dictating


def append_dictation(dictation):
    __unit.append_dictation(dictation)


def create_unit():
    return __unit


