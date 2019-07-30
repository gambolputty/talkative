import re
from talkative.Node import Node


class Rule:
    def __init__(self, index, rule):
        self.index = index
        self.is_touched = False
        self.raw = ''
        self.freq = [1]
        self.nodes = []
        
        # set text and frequency
        if isinstance(rule, str):
            self.raw = rule
        elif isinstance(rule, list):
            rule_size = len(rule)
            if rule_size == 0:
                raise ValueError(f'Empty rule found')

            # check if rule has valid frequency dividers from 1 - X
            if not all(isinstance(d, int) and d >= 1 for d in rule[1:]):
                raise ValueError(f'Rule with invalid divider (must be a number > 1): {rule}')

            # check rule text type
            if not isinstance(rule[0], str):
                raise ValueError(f'Rule text is not of type "string" (is {type(rule[0])})')

            self.raw = rule[0]
            self.freq = rule[1:]            
        else:
            raise ValueError(f'Wrong rule format "{rule}"')

        # parse nodes only if rule text not empty
        self.nodes = self.parse_nodes()

    
    def parse_nodes(self):
        result = []

        # handle empty rule text
        # useful for skipping 
        if self.raw.strip() == '':
            return [Node(type=0, text=self.raw)]

        match_iter = re.finditer(r'(?P<text>[^#]+)|(?:#(?P<tag>[^.#]+)(?:\.(?P<mod>[^#]+))?#)', self.raw)
        for match in match_iter:
            node = None
            if match.group('text'):
                node = Node(type=0, text=match.group('text'))
            elif match.group('tag'):
                node = Node(type=1, text=match.group('tag'))
                if match.group('mod'):
                    node.mod = match.group('mod').split('.')
            if node is None:
                raise ValueError(f'Something is wrong with the nodes found in rule {self.raw}')

            result.append(node)

        return result


    def flatten(self, state):
        text_list = []
        self.is_touched = True

        # loop nodes, check for expandable
        for node in self.nodes:
            if node.type == 0:
                text_list.append(node.text)
            elif node.type == 1:
                # pick rule from state for node
                rule = next((r for r in state[node.text] if r.is_touched is False), False)
                if rule is False:
                    raise ValueError(f'No next rule found in state for node "{node.text}", type {node.type}')

                # expand rule
                text_list.extend(rule.flatten(state))

        return text_list
