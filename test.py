from pdb import set_trace as bp
from pprint import pprint
from Grammar import Grammar

grammar = {
    'origin': {
        'rules': [
            'Es #es-ist# #viel# zu #zu-adjektiv.Upper# und #zudem# #viel# zu #zu-adjektiv#',
            'Es #es-ist# zu #zu-adjektiv#, zu #zu-adjektiv# und #zudem# zu #zu-adjektiv#',
            'Es #es-ist# #zudem# #viel# zu #zu-adjektiv#',
            'Zu #zu-adjektiv#, zu #zu-adjektiv#, zu #zu-adjektiv#',
        ]
    },
    'es-ist': {
        'method': 'freq',
        'rules': [
            ['es ist', 1],
            ['es erscheint mir', 7],
            ['ich finde es', 5]
        ]
    },
    'zudem': [
        'im Allgemeinen',
        'weitgehend',
        'im Großen und Ganzen',
        'darüber hinaus',
        'des Wei­te­ren',
        'ganz sicher',
        'jedenfalls',
        'zudem'
    ],
    'viel': {
        'rules': [
            ['viel'],
            'häufig',
            'weitaus',
            'wiederholt',
            'generell',
            'oft',
            'sehr oft',
            'manchmal',
            ['x-fach'],
            ['immer wieder'],
            ['etliche mal'],
            ['enorm']
        ]
    },
    'zu-adjektiv': {
        'method': 'uniq',
        'rules': [
            'zu abartig',
            'zu abenteuerlich',
            'zu abergläubisch',
            'zu abfällig',
            'zu abhängig',
            'zu abrupt',
            'zu abscheulich',
            'zu abseitig',
            'zu abstoßend'
        ]
    }
}

new_story = Grammar(grammar)
for step in range(1, 50):
    # print(f'Step {step}')
    new_story.flatten()
