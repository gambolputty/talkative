from pdb import set_trace as bp
from pprint import pprint
from random import shuffle
from Story import Story


with open('material/zu.txt', 'r', encoding='utf-8') as f:
    adjectives = f.read().split('\n')
shuffle(adjectives)

grammar = {
    'origin': {
        'method': 'freq',
        'rules': [
            ['#es-ist# #steigerung1# zu #adjektiv#', 1],
            ['#es-ist# #zudem# #steigerung1# zu #adjektiv# #continue#', 3],
            ['#zudem# #ist-es# #steigerung1# zu #adjektiv# #continue#', 4],
            ['#es-ist# zu #adjektiv#, zu #adjektiv# und #zudem# zu #adjektiv#', 5],
            ['Zu #adjektiv#, zu #adjektiv#, zu #adjektiv# #continue#', 7],
        ]
    },
    'continue': {
        'method': 'freq',
        'rules': [
            ['', 1],
            ['und #zudem# #steigerung1# zu #adjektiv#', 3]
        ]
    },
    'es-ist': {
        'method': 'freq',
        'rules': [
            ['es ist', 1],
            ['es erscheint mir', 10],
            ['ich finde es', 5]
        ]
    },
    'ist-es': [
        ['ist es', 1],
        ['erscheint es mir', 10],
        ['finde ich es', 5]
    ],

    # Steigerung des Komparativs
    'steigerung1': {
        'method': 'freq',
        'rules': [
            ['', 1],
            ['viel', 3],
            ['deutlich', 4],
            # ['erheblich', 4],
            ['defintiv', 4],
            ['wesentlich', 4],
            ['vielfach', 4],
            ['weitgehend', 4],
            ['wirklich', 4],
            ['partout', 4],
            ['absolut', 4],
            ['allemal', 4],
            ['fraglos', 4],
            ['ganz bestimmt', 4],
            ['gewiss', 4],
            ['weitaus', 4],
            ['sehr viel', 8],
            ['immens', 7],
            ['allerhand', 7],
            ['eine gehörige Portion', 8],
            ['x-fach', 10],
        ]
    },
    
    # https://de.wiktionary.org/wiki/sehr
    'steigerung2': [
        'sehr', 
        'enorm'
        # ganz, recht, schwer, ausgesprochen,
        # äußerst, mordsmäßig, unheimlich, wahnsinnig
        # mächtig, tüchtig
    ],
    'zudem': [
        'im Allgemeinen',
        'im Wesentlichen',
        'in erster Linie',
        'im Speziellen', 
        'allgemein',
        'von wenigen Ausnahmen abgesehen',
        'im Großen und Ganzen',
        'insgesamt betrachtet',
        'darüber hinaus',
        'des Wei­te­ren',
        'im Weiteren',
        'sicher',
        'ganz sicher',
        'sicherlich',
        'mit Sicherheit',
        'auf jeden Fall',
        'in jeder Hinsicht',
        'ohne Frage',
        'ohne Zweifel',
        'zweifellos',
        'zudem',
        'außerdem',
        'auch',
        'zusätzlich',
        'nebenbei',
        'häufig',
        'wiederholt',
        'generell',
        'oft',
        'sehr oft',
        'manchmal',
        'immer wieder',

        # 'etliche male',
        # gemeinhin, gewöhnlich, im Regelfall, in der Regel, meist, meistens, normalerweise, zumeist
        # wenn man spezielle Einzelfälle außer Acht lässt
        # 'jedenfalls',
        # hinzu kommt ...
        # überdies, ferner, nebenher, in der weiteren Folge
        
    ],
    'adjektiv': {
        'method': 'uniq',
        'rules': adjectives
    }
}

new_story = Story(grammar)
for step in range(0, 50):
    # print(f'Step {step}')
    new_story.tell()

print(new_story.text)
