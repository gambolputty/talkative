from collections import defaultdict
from functools import reduce
from Symbol import Symbol

class Story:
    def __init__(self, grammar):
        self.grammar = {k: Symbol(k, v) for k, v in grammar.items()}
        self.state = defaultdict(list)
        self.text = ''


    def tell(self):
        self.clear_state()
        self.build_state('origin')
        # self.build_text('origin')
    

    def build_text(self, key='origin'):
        for rule in self.state[key]:
            # append to text
            self.text += rule.flatten(self.state) + '\n'

            # check tags in rule
            if len(rule.nodes) > 0:
                for node in rule.nodes:
                    self.build_text(node.key)


    def clear_state(self):
        self.state.clear()


    def build_state(self, key='origin'):
        # pick rule
        rule = self.grammar[key].select_rule()

        # save to state
        self.state[key].append(rule)
        
        # check for expandable nodes in rule
        for node in [n for n in rule.nodes if n.type == 1]:
            self.build_state(node.text)

        # # handle None
        # # rule_text can be none
        # if rule_index is None:
        #     raise Exception(f'No rule found for key "{key}"')

        # # search symbols
        # # when found, recursivly execute this function again

        # # add to history
        # self.grammar.add_to_history(key=key, index=rule_index)
        # print()

    # return index of rule and rule text

