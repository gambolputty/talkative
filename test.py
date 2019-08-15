from talkative.Story import Story

grammar = {
    'origin': {
        'method': 'rand',
        'rules': [
            'Das ist ein #kleiner-text#',
            'Das ist ein #bug#',
        ]
    },
    'kleiner-text': {
        'method': 'rand',
        'rules': [
            'kleiner #text# #test1#'
        ]
    },
    'text': {
        'method': 'rand',
        'rules': [
            'Text', 
            'Witz'
        ]
    },
    'test1': {
        'method': 'rand',
        'rules': []
    },
        
}

new_story = Story(grammar, separator='.\n')
new_story.tell()
print(new_story.text)
