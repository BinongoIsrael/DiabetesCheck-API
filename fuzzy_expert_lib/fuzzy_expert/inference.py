# fuzzy_expert/inference.py
from .rules import Rule
def evaluate_rules(rules, fuzzified_inputs):
    """
    Evaluate all fuzzy rules and aggregate their outputs.

    Args:
        rules (list): List of Rule objects.
        fuzzified_inputs (dict): Fuzzified input values (e.g., {'fbs': {'low': 0.2, 'high': 0.8}}).

    Returns:
        dict: Aggregated output (e.g., {'low_risk': 0.2, 'high_risk': 0.8}).
    """
    output = {}
    for rule in rules:
        consequent, strength = rule.evaluate(fuzzified_inputs)
        if strength > 0:
            # assume consequent is just a string like "high_risk"
            if consequent in output:
                output[consequent] = max(output[consequent], strength)
            else:
                output[consequent] = strength
    return output
