# fuzzy_expert/fuzzify.py
from .membership import triangular, trapezoidal

def fuzzify(value, membership_func, membership_params):
    """Fuzzify a crisp value using the specified membership function and parameters."""
    return membership_func(value, membership_params)

def fuzzify_variable(value, linguistic_terms):
    """Fuzzify a crisp value for all linguistic terms of a fuzzy variable."""
    fuzzified_values = {}
    for term, params in linguistic_terms.items():
        if len(params) == 3:
            fuzzified_values[term] = fuzzify(value, triangular, params)
        elif len(params) == 4:
            fuzzified_values[term] = fuzzify(value, trapezoidal, params)
        else:
            raise ValueError("Parameters must be a tuple of length 3 (triangular) or 4 (trapezoidal).")
    return fuzzified_values
