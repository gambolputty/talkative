from Symbol import Symbol

class Grammar:
    symbols = {}

    def __init__(self, grammar):
        self.symbols = {k: Symbol(k, v) for k, v in grammar.items()}                


    def get(self, key=None):
        return self.grammar[key] if key is not None and key in self.grammar else self.grammar


    def add_to_history(self, key, index):
        self.grammar[key]['history'].append(index)


    def flatten(self, key='origin'):
        # pick rule
        rule = self.symbols[key].select_rule()
        print()
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

