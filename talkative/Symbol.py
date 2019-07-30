from pdb import set_trace as bp
from pprint import pprint
import random
from talkative.History import History
from talkative.Rule import Rule


class Symbol:
    """
    method:
        rand (default):
            Select a random rule from the list.

        freq:
            Select a rule whose frequency value is divisible by the number
            of all previous occurrences of the rule inside the "history".
            Prefer rule with hightest freqency value. If multiple rules of
            that rule are found, select random one.

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
        self.history = None

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

        # init history
        self.history = History(len(self.rules))


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
        self.history.add(found_rule.index)

        # return
        return found_rule


    def select_rule_random(self):
        if len(self.rules) == 1:
            return self.rules[0]
        
        # get indexes to exclude for next selection
        indexes_to_exlude = self.history.recently_used_steps
        if indexes_to_exlude:
            # filter rules
            rule_candidates = [r for r in self.rules if r.index not in indexes_to_exlude]
        else:
            rule_candidates = self.rules

        return random.choice(rule_candidates)


    def select_rule_freq(self):
        # filter rules
        # n % k == 0
        # evaluates true if n is an exact multiple of k
        # https://stackoverflow.com/a/8002234/5732518
        next_step = len(self.history.steps) + 1
        rules_filtered = [r for r in self.rules if any(next_step % divider == 0 for divider in r.freq)]

        # sort (hightest freq. value at the top)
        rules_sorted = sorted(rules_filtered, key=lambda x: x.freq, reverse=True)
        if not rules_sorted:
            raise ValueError(f'No rule found for step "{next_step}" in "{self.key}"')

        # get first rule (with highest freq. value)
        wanted_rule = rules_sorted[0]

        # check if there are multiple rules with same frequency value
        # select random rule from there
        same_freq_rules = [r for r in rules_sorted if r != wanted_rule and \
            all(f in wanted_rule.freq for f in r.freq)]
        if same_freq_rules:
            indexes_to_exlude = self.history.recently_used_steps
            rule_candidates = [r for r in same_freq_rules if r.index not in indexes_to_exlude]
            # if all rules with same freq. used recently, select randomly from all rules
            if not rule_candidates:
                rule_candidates = same_freq_rules
            return random.choice(rule_candidates)            

        return wanted_rule


    def select_rule_uniq(self):
        # find next unique rule
        for rule in self.rules:
            if rule.index not in self.history.steps:
                return rule
        else:
            raise ValueError(f'No unique rule found in "{self.key}" (all used)')
