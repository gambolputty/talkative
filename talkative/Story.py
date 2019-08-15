from collections import defaultdict
from copy import deepcopy
from talkative.Symbol import Symbol
from talkative.Exceptions import NoRulesError


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
            raise NoRulesError(f'"#{key}#" not found in grammar')

        saved_keys = []
        symbol = self.symbols[key]
        ignored_rules_indexes = set()
        while True:
            # if all rules tried, break while loop
            if len(ignored_rules_indexes) == len(symbol.rules):
                raise NoRulesError()

            # select rule, copy instance
            rule = deepcopy(symbol.select_rule(ignored_rules_indexes))
            
            # check for expandable nodes in rule
            try:
                for node in [n for n in rule.nodes if n.type == 1]:
                    saved_keys.append(self.build_state(node.text))
            except NoRulesError:
                # undo every step taken in 
                # --> remove symbol key from state and revert symbol history
                if saved_keys:
                    [self.undo(k) for k in saved_keys]
                
                # remember rule to exlcude next time
                ignored_rules_indexes.add(rule.index)
            else:
                # save rule to state
                self.state[key].append(rule)

                # add to history
                symbol.history.add(rule.index)

                return key


    def undo(self, key):
        """
        1. remove symbol key from state
        2. undo symbol history for count of rules in it
        """
        if key not in self.state:
            return
        
        # undo symbol history
        rules_count = len(self.state[key])
        for i in range(0, rules_count):
            self.symbols[key].history.undo()

        # delete key from state
        del self.state[key]


    def generate_text(self):
        origin_rule = self.state[self.origin][0]
        text = origin_rule.flatten(self.state)

        # remove duplicate spaces
        text = ' '.join(text.split())

        # save
        self.text += text + self.separator
