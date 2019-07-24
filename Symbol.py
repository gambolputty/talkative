from pdb import set_trace as bp
from pprint import pprint
import random
from Rule import Rule

class Symbol:
    def __init__(self, key, options):
        self.key = key        
        self.history = []

        # options can be a list (of rules) or a dict
        # set list of rules to parse
        # optionally check types
        options_type = type(options).__name__
        if options_type == 'list':
            rules_to_parse = options
        elif options_type == 'dict':
            rules_to_parse = options['rules']
        else:
            raise ValueError(f'Wrong grammar format for "{key}"')

        # set method
        self.method = 'rand'  # method to select rules (rand, freq, uniq)
        if options_type == 'dict' and 'method' in options:
            # check provided method
            method = options['method']
            if method not in ['rand', 'freq', 'uniq']:
                raise ValueError(f'Invalid method in "{key}" (saw "{method}", excepted "rand", "uniq" or "freq")')
            self.method = method
        
        # init rules
        self.rules = [Rule(i, r) for i, r in enumerate(rules_to_parse)]


    def select_rule(self):
        found_rule = None
        if self.method == 'rand':
            found_rule = random.choice(self.rules)
        elif self.method == 'freq':
            # filter rules
            # n % k == 0
            # evaluates true if n is an exact multiple of k
            # https://stackoverflow.com/a/8002234/5732518
            next_step = len(self.history) + 1
            rules_filtered = [r for r in self.rules if any(next_step % divider == 0 for divider in r.frequency)]
            rules_count = len(rules_filtered)
            if rules_count == 1:
                found_rule = rules_filtered[0]
            elif rules_count > 1:
                # sort
                # hightest divider at the bottom
                rules_sorted = sorted(rules_filtered, key=lambda x: x.frequency)
                # pick last rule (with highest divider)
                found_rule = rules_sorted[-1]
            else:
                raise ValueError(f'No rule found for frequency "{next_step}" in "{self.key}"')
        elif self.method == 'uniq':
            # find next unique rule
            for rule in self.rules:
                if rule.index not in self.history:
                    found_rule = rule
                    break
            else:
                raise ValueError(f'No unique rule found in "{self.key}" (all used)')
        
        # add to history
        self.history.append(found_rule.index)

        # return
        return found_rule

