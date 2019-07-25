from pdb import set_trace as bp
from pprint import pprint
from random import shuffle
from Story import Story


with open('material/zu.txt', 'r', encoding='utf-8') as f:
    adjectives = f.read().split('\n')
shuffle(adjectives)

grammar = {
    'origin': [
        '#es-ist# #viel# zu #adjektiv.Upper# und #zudem# #viel# zu #adjektiv#',
        '#es-ist# zu #adjektiv#, zu #adjektiv# und #zudem# zu #adjektiv#',
        '#es-ist# #zudem# #viel# zu #adjektiv#',
        'Zu #adjektiv#, zu #adjektiv#, zu #adjektiv#',
    ],
    'es-ist': {
        'method': 'freq',
        'rules': [
            ['es ist', 1],
            ['es erscheint mir', 7],
            ['ich finde es', 5]
        ]
    },
    'viel': {
        'method': 'freq',
        'rules': [
            ['viel', 2],
            ['häufig', 2],
            ['weitaus', 2],
            ['wiederholt', 2],
            ['generell', 2],
            ['oft', 2],
            ['sehr oft', 2],
            ['manchmal', 2],
            ['x-fach', 2],
            ['immer wieder', 2],
            ['etliche mal', 2],
            ['enorm', 2],
            ['', 1],
        ]
    },
    'zudem': [
        'im Allgemeinen',
        'weitgehend',
        'im Großen und Ganzen',
        'darüber hinaus',
        'des Wei­te­ren',
        'ganz sicher',
        'auf jeden Fall',
        # 'jedenfalls',
        'zudem'
    ],
    'adjektiv': {
        'method': 'uniq',
        'rules': adjectives
    }
}

new_story = Story(grammar)
for step in range(0, 20):
    # print(f'Step {step}')
    new_story.tell()

print(new_story.text)
