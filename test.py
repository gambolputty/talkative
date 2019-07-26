from pdb import set_trace as bp
from pprint import pprint
from random import shuffle
from Story import Story


with open('material/zu.txt', 'r', encoding='utf-8') as f:
    adjectives = f.read().split('\n')
shuffle(adjectives)

grammar = {
    'origin': [
        '#es-ist# #viel# zu #adjektiv# #continue#',
        '#zudem# #ist-es# #viel# zu #adjektiv# #continue#',
        # '#es-ist# zu #adjektiv#, zu #adjektiv# und #zudem# zu #adjektiv#',
        # '#es-ist# #zudem# #viel# zu #adjektiv#',
        # 'Zu #adjektiv#, zu #adjektiv#, zu #adjektiv#',
    ],
    'continue': {
        'method': 'freq',
        'rules': [
            ['', 1],
            ['und #zudem# #viel# zu #adjektiv#', 3]
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
    'ist-es': [
        'ist es'
    ],
    'viel': {
        'method': 'freq',
        'rules': [
            ['', 1],
            ['viel', 3],
            ['weitaus', 4],
            ['enorm', 5],
            ['x-fach', 7],
        ]
    },
    'zudem': [
        'im Allgemeinen',
        'im Wesentlichen',
        'in erster Linie',
        'im Speziellen', 
        # gemeinhin, gewöhnlich, im Regelfall, in der Regel, meist, meistens, normalerweise, zumeist
        'von wenigen Ausnahmen abgesehen',
        # wenn man spezielle Einzelfälle außer Acht lässt
        'weitgehend',
        'im Großen und Ganzen',
        # insgesamt betrachtet, allgemein
        'darüber hinaus',
        'des Wei­te­ren',
        'ganz sicher',
        'auf jeden Fall',
        # 'jedenfalls',
        'zudem',
        # hinzu kommt ...
        'außerdem',
        # überdies, zudem, ferner, nebenher, nebenbei, des Weiteren, weiterführend, im Weiteren, in der weiteren Folge, darüber hinaus, auch, zusätzlich
        'häufig',
        'wiederholt',
        'generell',
        'oft',
        'sehr oft',
        'manchmal',
        'immer wieder',
        'etliche male',
        
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
