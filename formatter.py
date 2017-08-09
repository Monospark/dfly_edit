class FormatType:
    camelCase = 1
    pascalCase = 2
    snakeCase = 3
    squash = 4
    upperCase = 5
    lowerCase = 6
    dashify = 7
    dotify = 8
    spokenForm = 9


format_map = {
    "camel case": FormatType.camelCase,
    "pascal case": FormatType.pascalCase,
    "snake case": FormatType.snakeCase,
    "uppercase": FormatType.upperCase,
    "lowercase": FormatType.lowerCase,
    "squash": FormatType.squash,
    "lowercase squash": [FormatType.squash, FormatType.lowerCase],
    "uppercase squash": [FormatType.squash, FormatType.upperCase],
    "squash lowercase": [FormatType.squash, FormatType.lowerCase],
    "squash uppercase": [FormatType.squash, FormatType.upperCase],
    "dashify": FormatType.dashify,
    "lowercase dashify": [FormatType.dashify, FormatType.lowerCase],
    "uppercase dashify": [FormatType.dashify, FormatType.upperCase],
    "dashify lowercase": [FormatType.dashify, FormatType.lowerCase],
    "dashify uppercase": [FormatType.dashify, FormatType.upperCase],
    "dotify": FormatType.dotify,
    "lowercase dotify": [FormatType.dotify, FormatType.lowerCase],
    "uppercase dotify": [FormatType.dotify, FormatType.upperCase],
    "dotify lowercase": [FormatType.dotify, FormatType.lowerCase],
    "dotify uppercase": [FormatType.dotify, FormatType.upperCase],
    "say": FormatType.spokenForm,
    "environment variable": [FormatType.snakeCase, FormatType.upperCase],
}


def format_camel_case(input_text):
    new_text = ""
    words = input_text.split(" ")
    for word in words:
        if new_text == '':
            new_text = word[:1].lower() + word[1:]
        else:
            new_text = '%s%s' % (new_text, word.capitalize())
    return new_text


def format_pascal_case(input_text):
    new_text = ""
    words = input_text.split(" ")
    for word in words:
        new_text = '%s%s' % (new_text, word.capitalize())
    return new_text


def format_snake_case(input_text):
    new_text = ""
    words = input_text.split(" ")
    for word in words:
        if new_text != "" and new_text[-1:].isalnum() and word[-1:].isalnum():
            word = "_" + word  # Adds underscores between normal words.
        new_text += word.lower()
    return new_text


def format_dashify(input_text):
    new_text = ""
    words = input_text.split(" ")
    for word in words:
        if new_text != "" and new_text[-1:].isalnum() and word[-1:].isalnum():
            word = "-" + word  # Adds dashes between normal words.
        new_text += word
    return new_text


def format_dotify(input_text):
    new_text = ""
    words = input_text.split(" ")
    for word in words:
        if new_text != "" and new_text[-1:].isalnum() and word[-1:].isalnum():
            word = "." + word  # Adds dashes between normal words.
        new_text += word
    return new_text


def format_squash(input_text):
    new_text = ""
    words = input_text.split(" ")
    for word in words:
        new_text = '%s%s' % (new_text, word)
    return new_text


def format_upper_case(input_text):
    new_text = ""
    words = input_text.split(" ")
    for word in words:
        if new_text != "" and new_text[-1:].isalnum() and word[-1:].isalnum():
            word = " " + word  # Adds spacing between normal words.
        new_text += word.upper()
    return new_text


def format_lower_case(input_text):
    new_text = ""
    words = input_text.split(" ")
    for word in words:
        if new_text != "" and new_text[-1:].isalnum() and word[-1:].isalnum():
            if new_text[-1:] != "." and word[0:1] != ".":
                word = " " + word  # Adds spacing between normal words.
        new_text += word.lower()
    return new_text


def format_spoken_form(input_text):
    new_text = ""
    words = input_text.split(" ")
    for word in words:
        if new_text != "":
            word = " " + word
        new_text += word
    return new_text


FORMAT_TYPES_MAP = {
    FormatType.camelCase: format_camel_case,
    FormatType.pascalCase: format_pascal_case,
    FormatType.snakeCase: format_snake_case,
    FormatType.squash: format_squash,
    FormatType.upperCase: format_upper_case,
    FormatType.lowerCase: format_lower_case,
    FormatType.dashify: format_dashify,
    FormatType.dotify: format_dotify,
    FormatType.spokenForm: format_spoken_form,
}


def format_text(text, format_type):
    if type(format_type) != type([]):
        format_type = [format_type]
    result = ""
    for value in format_type:
        if not result:
            if format_type == FormatType.spokenForm:
                result = text
            else:
                result = str(text)
        method = FORMAT_TYPES_MAP[value]
        result = method(result)
    return result


def format_and_write_text(text, format_type):
    import command_tracker

    formatted = format_text(text, format_type)
    command_tracker.text(formatted).execute()
