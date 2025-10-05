class Rule:
    def __init__(self, antecedents, consequent):
        """
        Initialize a fuzzy rule.
        
        :param antecedents: A list of tuples (variable_name, term) representing the rule's conditions.
        :param consequent: A tuple (variable_name, term) representing the rule's conclusion.
        """
        self.antecedents = antecedents
        self.consequent = consequent
    
    def evaluate(self, fuzzified_inputs):
        """
        Evaluate the rule based on fuzzified inputs.
        
        :param fuzzified_inputs: A dictionary where keys are variable names and values are dictionaries
                                of linguistic terms and their corresponding membership degrees.
        :return: The degree of membership for the consequent term based on the rule evaluation.
        """
        degrees = []
        for var, term in self.antecedents:
            if var in fuzzified_inputs and term in fuzzified_inputs[var]:
                degrees.append(fuzzified_inputs[var][term])
            else:
                degrees.append(0)
        
        # Use the minimum degree of membership for AND operation
        rule_strength = min(degrees) if degrees else 0
        
        return (self.consequent, rule_strength)