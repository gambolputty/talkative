class Node:
    """
    Types of nodes:
    0: Plain text
    1: Tag (e. g. #adjective.mod.mod#)
    """

    def __init__(self, type, text, mod=None):
        self.type = type
        self.text = text
        self.mod = mod
