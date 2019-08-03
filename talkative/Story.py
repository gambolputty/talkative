from collections import defaultdict
from copy import deepcopy
from talkative.Symbol import Symbol


class Story:
    def __init__(self, grammar, separator='\n'):
        self.origin = 'origin'
        self.separator = separator
        self.symbols = {k: Symbol(k, v) for k, v in grammar.items()}
        self.state = defaultdict(list)
        self.text = ''


    def tell(self):
        self.state.clear()
        self.build_state(self.origin)
        self.generate_text()


    def build_state(self, key):
        if key not in self.symbols:
            raise KeyError(f'"#{key}#" not found in grammar')
        # pick rule, copy instance
        rule = deepcopy(self.symbols[key].select_rule())

        # save to state
        self.state[key].append(rule)
        
        # check for expandable nodes in rule
        for node in [n for n in rule.nodes if n.type == 1]:
            self.build_state(node.text)


    def generate_text(self):
        origin_rule = self.state[self.origin][0]
        flattened = origin_rule.flatten(self.state)

        # join text chunks
        text = ''.join(flattened)

        # remove duplicate spaces
        text = ' '.join(text.split())

        # save
        self.text += text + self.separator
