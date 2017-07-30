from dragonfly import Choice, Compound, MappingRule, CompoundRule, RuleRef
from dragonfly_loader import Unit, json_parser, loader

from command_tracker import text


class Abbreviations(Unit):

    def __init__(self, grammar_name="abbreviations"):
        Unit.__init__(self, grammar_name)

    def create_grammar(self, g, t):
        class AbbreviationRule(CompoundRule):
            spec = "[cap|capitalize] abbreviate <abbreviation>"

            def __init__(self, exported):
                extras = [Choice("abbreviation", self.__abbreviation_map)]
                CompoundRule.__init__(self, extras=extras, exported=exported)

            def value(self, node):
                return node.get_child_by_name("abbreviation").value()

            def _process_recognition(self, node, extras):
                text(self.value(node)).execute()

        g.add_rule(AbbreviationRule())
        return True

    def load_config(self, config_path):
        file = "data/abbreviations." + loader.get_locale() + ".json"
        self.__abbreviation_map = json_parser.parse_json(file)["abbreviations"]


def create_unit():
    return Abbreviations()
