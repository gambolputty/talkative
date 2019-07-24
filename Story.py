from collections import defaultdict
from functools import reduce
from Symbol import Symbol

class Story:
    grammar = {}
    state = defaultdict(dict)
    text = ''

    def __init__(self, grammar):
        self.grammar = {k: Symbol(k, v) for k, v in grammar.items()}


    def tell(self):
        self.clear_state()
        self.recursive('origin')
        self.generate_text()
    

    def generate_text(self):
        trash = []
        # for key, rules in self.state.items():
        #     for rule in rules:
        #         # check nodes of rule
        #         node_keys = [n.key for n in rule.nodes]
        #         # get rules from state
        #         wanted_rules = {k: [r for r in self.state[k] if r not in trash] for k in node_keys}
        #         print(rule.text)
        #         print(wanted_rules)
        #         print()
        

    def clear_state(self):
        self.state.clear()


    def get_nested_value(d, path=('origin')):
        return reduce(dict.get, path, d)


    def recursive(self, key='origin', path=('origin')):
        # pick rule
        rule = self.grammar[key].select_rule()

        # save to state
        nested_dict = get_nested_value(self.state, path)
        self.state[key].append(rule)
        
        # check nodes in rule
        if len(rule.nodes) > 0:
            for node in rule.nodes:
                self.recursive(node.key, (key, node.key))

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

