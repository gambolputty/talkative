import re

class Rule:
    index = -1
    text = ''
    frequency = [1]
    nodes = []

    def __init__(self, index, rule):
        # set index
        self.index = index
        
        # set text and frequency
        if isinstance(rule, str):
            if rule.strip() == '':
                raise ValueError('Empty rule text')
            self.text = rule
        elif isinstance(rule, list):
            rule_size = len(rule)
            if rule_size == 1:
                self.text = rule[0]
            elif rule_size > 1:
                # check if rule has valid frequency dividers from 1 - X
                if not all(isinstance(d, int) and d >= 1 for d in rule[1:]):
                    raise ValueError(f'Rule with invalid divider (must be a number > 1): {rule}')
                self.text = rule[0]
                self.frequency = rule[1:]
            elif rule_size == 0:
                raise ValueError(f'Empty rule')
        else:
            raise ValueError(f'Wrong rule format "{rule}"')

        # parse nodes
        self.parse_nodes()

    
    def parse_nodes(self):
        result = []
        for match in re.finditer(r'(?:#([^.#]+)(?:\.([^#]+))?#)', self.text):
            node = {
                'key': match.group(1),
                'modifiers': None
            }
            if match.group(1) is None:
                raise ValueError(f'Something is wrong with the nodes found in rule {self.text}')
            if match.group(2) is not None:
                node['modifiers'] = match.group(2).split('.')
            result.append(node)

        self.nodes = result
