from pdb import set_trace as bp
from pprint import pprint
from random import shuffle
from Story import Story

with open('material/zu.txt', 'r', encoding='utf-8') as f:
    adjectives = f.read().split('\n')
shuffle(adjectives)

grammar = {
    'origin': [
        'Es #es-ist# #viel# zu #adjektiv.Upper# und #zudem# #viel# zu #adjektiv#',
        # 'Es #es-ist# zu #adjektiv#, zu #adjektiv# und #zudem# zu #adjektiv#',
        # 'Es #es-ist# #zudem# #viel# zu #adjektiv#',
        # 'Zu #adjektiv#, zu #adjektiv#, zu #adjektiv#',
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
            ['', 1],
            'viel',
            'häufig',
            'weitaus',
            'wiederholt',
            'generell',
            'oft',
            'sehr oft',
            'manchmal',
            'x-fach',
            'immer wieder',
            'etliche mal',
            'enorm'
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
