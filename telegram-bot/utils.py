import re

def string_has_letter(string):
    return re.search('[a-zA-Z]', string)


def string_has_bar(string):
    return '/' in string