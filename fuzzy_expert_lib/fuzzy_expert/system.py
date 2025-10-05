# fuzzy_expert/system.py
from .fuzzify import fuzzify_variable
from .rules import Rule
from .inference import evaluate_rules
from .defuzzify import defuzzify_centroid
from .membership import triangular, trapezoidal

class FuzzyExpertSystem:
    def __init__(self):
        """
        Initialize a fuzzy expert system (Mamdani type).
        """
        self.rules = []
        self.variables = {}      # input variables
        self.output_terms = {}   # output fuzzy sets

    def add_variable(self, name, terms):
        """
        Add a linguistic input variable (e.g., 'temp' with terms 'low', 'high').

        Args:
            name (str): Variable name (e.g., 'temp').
            terms (dict): Terms and their membership parameters (triangular (a,b,c) or trapezoidal (a,b,c,d)).
        """
        self.variables[name] = terms

    def add_output_term(self, term, params):
        """
        Define an output fuzzy set term with triangular or trapezoidal membership function.

        Args:
            term (str): Output term name (e.g., 'slow').
            params (tuple): Membership parameters (3 for triangular, 4 for trapezoidal).
        """
        if len(params) not in (3, 4):
            raise ValueError("Output term must be defined by 3 (triangular) or 4 (trapezoidal) parameters.")
        self.output_terms[term] = params

    def add_rule(self, conditions, output_term):
        """
        Add a fuzzy rule (e.g., IF temp is high AND humidity is high THEN fan is fast).

        Args:
            conditions (list): List of (var_name, term) pairs.
            output_term (str): Output fuzzy set name.
        """
        self.rules.append(Rule(conditions, output_term))

    def assess(self, inputs, resolution=100):
        """
        Assess crisp inputs and return both crisp output and classification.

        Args:
            inputs (dict): Crisp input values (e.g., {'temp': 28, 'humidity': 70}).
            resolution (int): Number of points to sample the output universe.

        Returns:
            (float, str): Crisp output value and the best matching output term.
        """
        # 1. Fuzzify inputs
        fuzzified_inputs = {}
        for var_name, value in inputs.items():
            fuzzified_inputs[var_name] = fuzzify_variable(value, self.variables[var_name])

        # 2. Evaluate rules
        rule_outputs = evaluate_rules(self.rules, fuzzified_inputs)

        # 3. Build aggregated membership function for output
        rules_output = []
        for term, strength in rule_outputs.items():
            params = self.output_terms[term]

            if len(params) == 3:  # triangular
                low, mid, high = params
                a = (high - low)/2
                centroid = mid
                area = a *(2*strength - strength**2)
            elif len(params) == 4:  # trapezoidal
                a, b, c, d = params
                centroid = (a + 2*b + 2*c + d) / 6
                base1 = b - a
                base2 = d - c
                top = c - b
                area = ((base1 + top + base2) / 2) * strength
            else:
                continue  # ignore invalid

            rules_output.append((term, strength, params, centroid, area))

        crisp_value = defuzzify_centroid(rules_output, debug=True)

        # 5. Classification step → pick output term with max membership
        best_term = None
        best_degree = -1
        for term, params in self.output_terms.items():
            if len(params) == 3:
                degree = triangular(crisp_value, params)
            elif len(params) == 4:
                degree = trapezoidal(crisp_value, params)
            else:
                continue
            if degree > best_degree:
                best_degree = degree
                best_term = term

        return crisp_value, best_term
