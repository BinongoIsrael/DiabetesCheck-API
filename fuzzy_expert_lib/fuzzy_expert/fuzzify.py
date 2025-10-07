# fuzzy_expert/fuzzify.py
from .membership import triangular, trapezoidal

def fuzzify(value, membership_func, membership_params, kind="normal"):
    """Fuzzify a crisp value using the specified membership function and parameters."""
    # Pass 'kind' only if supported (triangular has it)
    if membership_func == triangular:
        return membership_func(value, membership_params, kind=kind)
    return membership_func(value, membership_params)


def fuzzify_variable(value, linguistic_terms):
    """
    Fuzzify a crisp value for all linguistic terms of a fuzzy variable.

    Automatically detects and applies shoulder behavior:
      - First term → left-shoulder
      - Last term → right-shoulder
      - Others → normal
    """
    fuzzified_values = {}
    term_labels = [t for t in linguistic_terms.keys() if t != "range"]

    for i, term in enumerate(term_labels):
        params = linguistic_terms[term]

        # Detect function type (triangular or trapezoidal)
        if len(params) == 3:
            if i == 0:
                kind = "left-shoulder"
            elif i == len(term_labels) - 1:
                kind = "right-shoulder"
            else:
                kind = "normal"
            fuzzified_values[term] = fuzzify(value, triangular, params, kind=kind)

        elif len(params) == 4:
            fuzzified_values[term] = fuzzify(value, trapezoidal, params)

        else:
            raise ValueError("Parameters must be a tuple of length 3 (triangular) or 4 (trapezoidal).")

    return fuzzified_values
