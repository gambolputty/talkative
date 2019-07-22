from pdb import set_trace as bp
from pprint import pprint
import random
from Ruleset import Ruleset


class Story:
    def __init__(self, ruleset):
        # init ruleset
        self.ruleset = Ruleset(ruleset)


    def flatten(self, key='origin'):
        # pick rule
        rule_index, rule_text = self.pick_rule(key)
        
        # handle None
        # rule_text can be none
        if rule_index is None:
            raise Exception(f'No rule found for key "{key}"')

        # search symbols
        # when found, recursivly execute this function again


        # add to history
        self.ruleset.add_to_history(key=key, index=rule_index)
        print()


    # return index of rule and rule text
    def pick_rule(self, key):
        try:
            rules, unique, history = self.ruleset.get(key=key).values()
        except KeyError:
            raise Exception(f'Cannot find key "{key}" in ruleset')

        # if every rule only has a divider of "1",
        # return early with random rule
        pick_random = all(max(r[1:]) == 1 for r in rules)
        if pick_random is True:
            random_rule = random.choice(rules)
            return [rules.index(random_rule), random_rule[0]]
        
        # filter rules
        # n % k == 0
        # evaluates true if n is an exact multiple of k
        # https://stackoverflow.com/a/8002234/5732518
        rule_steps_count = len(history) + 1
        rules_filtered = [r for r in rules if any(rule_steps_count % divider == 0 for divider in r[1:])]

        rules_count = len(rules_filtered)
        if rules_count == 1:
            return [0, rules_filtered[0][0]]
        elif rules_count > 1:
            # sort
            # hightest divider at the bottom
            rules_sorted = sorted(rules_filtered, key=lambda x: x[1:])
            # print(f'Rules sorted: {rules_sorted}')
            # pick last rule (with highest divider)
            last_rule = rules_sorted[-1]
            return [rules.index(last_rule), last_rule[0]]
        else:
            return [None, None]
    
