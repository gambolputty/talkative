import re

class Rule:
    def __init__(self, index, rule):
        self.index = index
        self.is_touched = False
        
        # set text and frequency
        self.text = ''
        self.frequency = [1]
        if isinstance(rule, str):
            self.text = rule
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

            self.text = rule[0]
            self.frequency = rule[1:]            
        else:
            raise ValueError(f'Wrong rule format "{rule}"')

        # parse nodes only if rule text not empty
        if self.text.strip():
            self.nodes = self.parse_nodes()

    
    def parse_nodes(self):
        result = []
        match_iter = re.finditer(r'(?P<text>[^#]+)|(?:#(?P<tag>[^.#]+)(?:\.(?P<mod>[^#]+))?#)', self.text)
        for match in match_iter:
            node = None
            if match.group('text'):
                node = Node(type=0, text=match.group('text'), span=match.span('text'))
            elif match.group('tag'):
                node = Node(type=1, text=match.group('tag'), span=match.span('tag'))
                if match.group('mod'):
                    node.mod = match.group('mod').split('.')

            if node is None:
                raise ValueError(f'Something is wrong with the nodes found in rule {self.text}')

            result.append(node)

        return result


    def flatten(self, state):
        text = ''
        self.is_touched = True

        # loop nodes, check for expandable
        for node in self.nodes:
            if node.type == 0:
                text += node.text
            elif node.type == 1:
                # pick rules from state
                try:
                    rule = next(r for r in state[node.text] if r.is_touched is False)
                    text += rule.flatten(state)
                except StopIteration:
                    raise ValueError(f'No next rule found in state for node "{node.text}", type {node.type}')

        return text


class Node:
    """
    Types of nodes:
    0: Plain text
    1: Tag (e. g. #adjective.mod.mod#)
    """
    def __init__(self, type, text=None, span=None, mod=None):
        self.type = type
        self.text = text
        self.span = span
        self.mod = mod
