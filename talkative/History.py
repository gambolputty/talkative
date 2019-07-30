class History:
    """History
    Each time a rule is selected, its index is stored in the history.
    """
    def __init__(self, rules_count):
        self.steps = []
        self.rules_count = rules_count

    
    def add(self, index):
        self.steps.append(index)


    @property
    def recently_used_steps(self):
        """
        Return step indexes that were used recently 
        """
        result = []
        steps_count = len(self.steps)

        if steps_count == 0:
            return result
        
        if self.rules_count <= 2:
            result = [self.steps[-1]]
        else:
            if steps_count < self.rules_count:
                result = self.steps
            else:
                # calculate 80% percent of the total number of rules
                # exclude these last 80% for the next selection
                ignore_from = int(round((80 * self.rules_count) / 100.0))
                result = self.steps[-ignore_from:]

        return result



