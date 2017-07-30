from dragonfly import Grammar, Function, MappingRule, Key, Mouse
import win32api, win32con


is_dictating = False
dictation = None
__dictation_incompatible_grammars = []
__disabled_dictation_grammars = []
is_marking = False
is_cursor_following_mouse = False
nesting_levels = []


def add_dictation_incompatible_grammar(grammar):
    __dictation_incompatible_grammars.append(grammar)


def stop_marking_or_update_cursor():
    if is_marking:
        stop_marking()
    else:
        update_cursor()


def update_cursor():
    if is_cursor_following_mouse:
        Mouse("left/3").execute()

def stop_marking():
    global is_marking
    if is_marking:
        is_marking = False
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def add_nesting_level(level):
    nesting_levels.append(level)
    if not is_dictating:
        Key("left/3:%s" % level).execute()


def remove_nesting_level():
    if len(nesting_levels) != 0:
        value = nesting_levels.pop()
        if not is_dictating:
            Key("right/3:%s" % value).execute()


def get_complete_nesting_level():
    if len(nesting_levels) != 0:
        levels = reduce(lambda x, y: x + y, nesting_levels)
        return levels
    else:
        return 0


def clear_nesting_levels():
    global nesting_levels
    nesting_levels = []


def remove_nesting_levels():
    level = get_complete_nesting_level()
    clear_nesting_levels()
    if level > 0:
        Key("right/3:%s" % level).execute()


def __start_dictating():
    global is_dictating
    is_dictating = True
    clear_nesting_levels()

    for grammar in __dictation_incompatible_grammars:
        if grammar.enabled:
            grammar.disable()
            __disabled_dictation_grammars.append(grammar)


def append_dictation(text):
    global dictation
    if dictation is None:
        dictation = text
    else:
        split_position = len(dictation) - get_complete_nesting_level()
        prefix = dictation[:split_position]
        suffix = dictation[split_position:]
        dictation = prefix + text + suffix


def __stop_dictating():
    global dictation
    global is_dictating
    is_dictating = False
    clear_nesting_levels()
    print(dictation)
    dictation = None

    for grammar in __disabled_dictation_grammars:
        grammar.enable()

    __disabled_dictation_grammars[:] = []


def __toggle_marking():
    global is_marking
    if is_marking:
        stop_marking()
    else:
        is_marking = True
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)


def __toggle_cursor():
    global is_cursor_following_mouse
    is_cursor_following_mouse = not is_cursor_following_mouse


def load_data(data):
    global is_cursor_following_mouse
    is_cursor_following_mouse = data["is_cursor_following_mouse"]
    global is_marking
    is_marking = data["is_marking"]
    global nesting_levels
    nesting_levels = data["nesting_levels"]


def save_data():
    data = {}
    data["is_cursor_following_mouse"] = is_cursor_following_mouse
    data["is_marking"] = is_marking
    data["nesting_levels"] = nesting_levels
    return data


def create_grammar():
    grammar = Grammar("global state")
    grammar.add_rule(MappingRule(mapping={
        "mark": Function(__toggle_marking),
        "cursor": Function(__toggle_cursor),
        "done": Function(remove_nesting_level),
        "done all": Function(remove_nesting_levels),
        "dictate": Function(__start_dictating),
        "finish": Function(__stop_dictating)
    }))
    return grammar, True
