from dragonfly import Key, MappingRule, Function
from dragonfly_loader import Unit

import dictation


class Nesting(Unit):
    def __init__(self):
        Unit.__init__(self, "nesting")
        self.__nesting_levels = []
        self.__floor = 0

    def set_floor(self):
        self.__floor = len(self.__nesting_levels)

    def remove_floor(self):
        self.__floor = 0

    def add_nesting_level(self, level):
        self.__nesting_levels.append(level)
        if not dictation.is_dictating():
            Key("left/3:%s" % level).execute()

    def remove_nesting_level(self):
        if len(self.__nesting_levels) == self.__floor:
            return

        if len(self.__nesting_levels) != 0:
            value = self.__nesting_levels.pop()
            if not dictation.is_dictating():
                Key("right/3:%s" % value).execute()

    def get_complete_nesting_level(self):
        if len(self.__nesting_levels) != 0:
            levels = reduce(lambda x, y: x + y, self.__nesting_levels[self.__floor:])
            return levels
        else:
            return 0

    def clear_nesting_levels(self):
        del self.__nesting_levels[self.__floor:]

    def remove_nesting_levels(self):
        level = self.get_complete_nesting_level()
        self.clear_nesting_levels()
        if level > 0:
            Key("right/3:%s" % level).execute()

    def load_data(self, data):
        self.__nesting_levels = data["nesting_levels"]

    def save_data(self):
        data = {}
        data["nesting_levels"] = self.__nesting_levels
        return data

    def create_grammar(self, g, t):
        g.add_rule(MappingRule(mapping={
            "done|next|exit": Function(self.remove_nesting_level),
            "(done|exit) all": Function(self.remove_nesting_levels),
        }))
        return True


__unit = Nesting()


def instance():
    return __unit


def create_unit():
    return __unit
