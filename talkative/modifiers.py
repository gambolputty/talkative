# Some modifiers by Allison Parrish: https://github.com/aparrish/pytracery/blob/master/tracery/modifiers.py

def capitalize(text, *params):
    return text[0].upper() + text[1:]


def replace(text, *params):
    return text.replace(params[0], params[1])


def choice(text, *params):
    choices = [x for x in text.split('|')]
    index = int(params[0]) - 1
    try:
        return choices[index]
    except KeyError:
        return choices[0]

base = {
    'capitalize': capitalize,
    'replace': replace
    'choice': choice
}
