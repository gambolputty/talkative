from collections import defaultdict
from copy import deepcopy
from Symbol import Symbol

class Story:
    def __init__(self, grammar):
        self.grammar = {k: Symbol(k, v) for k, v in grammar.items()}
        self.state = defaultdict(list)
        self.text = ''


    def tell(self):
        self.clear_state()
        self.build_state('origin')
        self.generate_text('origin')
    

    def generate_text(self, key='origin'):
        origin_rule = self.state['origin'][0]
        self.text += origin_rule.flatten(self.state) + '\n'
        # for rule in self.state[key]:
        #     # append to text
        #     self.text += rule.flatten(self.state) + '\n'

        #     # check for expandable nodes in rule
        #     for node in [n for n in rule.nodes if n.type == 1]:
        #         self.build_text(node.key)


    def clear_state(self):
        self.state.clear()


    def build_state(self, key='origin'):
        # pick rule
        rule = deepcopy(self.grammar[key].select_rule())

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

