class Ruleset:
    ruleset = {}

    def __init__(self, ruleset):
        # normalize rules
        # make every rule a list
        # check if every rule has a divider, if not add "1"
        for key, values in ruleset.items():
            # check unique property
            if 'unique' in values and isinstance(values['unique'], bool) is False:
                raise Exception(f'Property "unique" not of type Boolean in "{key}"')

            found_rules = []
            for rule in values['rules']:
                new_rule = False
                if isinstance(rule, str):
                    new_rule = [rule, 1]
                elif isinstance(rule, list):
                    rule_size = len(rule)
                    if rule_size == 1:
                        new_rule = [rule[0], 1]
                    elif rule_size > 1:
                        new_rule = rule
                    elif rule_size == 0:
                        print(f'Warning: skipped empty rule in {key}')
                        continue
                else:
                    raise Exception(f'Wrong rule format "{rule}"')

                # check if rule has valid dividers from 1 - X
                has_valid_dividers = all(isinstance(d, int) and d >= 1 for d in new_rule[1:])
                if has_valid_dividers is False:
                    print(f'Warning: skipped rule in "{key}" with invalid divider (must be a number > 1): {new_rule}')
                    continue

                # append to found
                found_rules.append(new_rule)

            # add to new_sets
            self.ruleset[key] = {
                'rules': found_rules,
                'unique': values['unique'] if 'unique' in values else False,
                'history': []
            }


    def get(self, key=None):
        return self.ruleset[key] if key is not None and key in self.ruleset else self.ruleset

    def add_to_history(self, key, index):
        self.ruleset[key]['history'].append(index)
