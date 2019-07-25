from pdb import set_trace as bp
from pprint import pprint
import random
from Rule import Rule


class Symbol:
    """
    method:
        rand (default):
            Select a random rule from the list.

        freq:
            Select a rule whose frequency value is divisible by the number
            of all previous occurrences of the rule inside the "history".
            Prefer rule with hightest freq. value.

        uniq:
            Force the selection of unique rules (rules not in "history" yet).
            Rules are selected in linear order.
            Will throw an error if no new rule is found.

     rand_balanced: True (default)
        In order to keep the distribution of rules balanced, only rules that were
        not recently used are selected by Pythons builtin random module.

     history:
        Each time a rule is selected, its index is stored in the history.
        
        
    """
    def __init__(self, key, opts):
        self.key = key        
        self.method = 'rand'
        self.rand_balanced = True
        self.rules = []
        self.history = []

        # check options
        # options can be a list (of rules) or a dict (with options and rules)
        # make it a dict
        options = self.parse_options(opts)

        # rand_balanced
        if 'rand_balanced' in options:
            self.rand_balanced = options['rand_balanced']
        # set method
        if 'method' in options:
            self.method = options['method']

        # init rules
        self.rules = [Rule(i, r) for i, r in enumerate(options['rules'])]


    def parse_options(self, options):
        options_type = type(options).__name__
        if options_type == 'dict':
            if 'rules' not in options:
                raise ValueError(f'No "rules"-key found in "{self.key}"')
            if 'rules' in options and not options['rules']:
                raise ValueError(f'Empty rules-key in "{self.key}"')
            if 'rand_balanced' in options and not isinstance(options['rand_balanced'], bool):
                raise ValueError(f'Option "rand_balanced" is not of type Boolean in "{self.key}"')
            if 'method' in options and options['method'] not in ['rand', 'freq', 'uniq']:
                raise ValueError(f'Invalid method in "{self.key}" (expected "rand", "uniq" or "freq")')
            return options
        elif options_type == 'list':
            if not options:
                raise ValueError(f'Empty rules-key in "{self.key}"')
            return { 'rules': options }
        else:
            raise ValueError(f'"{self.key}" is of invalid type (must be "list" or "dict"')


    def select_rule(self):
        found_rule = None
        if self.method == 'rand':
            found_rule = self.select_rule_random()
        elif self.method == 'freq':
            found_rule = self.select_rule_freq()
        elif self.method == 'uniq':
            found_rule = self.select_rule_uniq()
            
        # add to history
        self.history.append(found_rule.index)

        # return
        return found_rule


    def select_rule_random(self):
        rules_count = len(self.rules)
        history_size = len(self.history)
        indexes_to_exlude = []
        if history_size > 0:
            if rules_count <= 2:
                indexes_to_exlude = self.history[-1]
            else:
                if history_size < rules_count:
                    indexes_to_exlude = self.history
                else:
                    # calculate 80% percent of the total number of rules
                    # exclude these last 80% for the next selection
                    ignore_from = int(round((80 * rules_count) / 100.0))
                    indexes_to_exlude = self.history[-ignore_from:]

        # filter rules
        rule_candidates = self.rules
        if indexes_to_exlude:
            rule_candidates = [r for r in self.rules if r.index not in indexes_to_exlude]

        return random.choice(rule_candidates)


    def select_rule_freq(self):
        # filter rules
        # n % k == 0
        # evaluates true if n is an exact multiple of k
        # https://stackoverflow.com/a/8002234/5732518
        next_step = len(self.history) + 1
        rules_filtered = [r for r in self.rules if any(next_step % divider == 0 for divider in r.frequency)]

        # sort
        # hightest divider at the top
        rules_sorted = sorted(rules_filtered, key=lambda x: x.frequency, reverse=True)

        if not rules_sorted:
            raise ValueError(f'No rule found for frequency "{next_step}" in "{self.key}"')

        # select first rule (with highest divider)
        return rules_sorted[0]


    def select_rule_uniq(self):
        # find next unique rule
        for rule in self.rules:
            if rule.index not in self.history:
                return rule
        else:
            raise ValueError(f'No unique rule found in "{self.key}" (all used)')
