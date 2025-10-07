# fuzzy_expert/membership.py

def triangular(inputval, params, kind="normal"):
    """
    Triangular membership function with optional shoulder behavior.

    Args:
        inputval (float): Crisp input value.
        params (tuple): (lowval, midval, highval).
        kind (str): "normal", "left-shoulder", or "right-shoulder".

    Returns:
        float: Degree of membership (μ) in [0, 1].
    """
    lowval, midval, highval = params

    if not (lowval <= midval <= highval):
        raise ValueError("Triangular parameters must satisfy lowval <= midval <= highval")

    # --- Left shoulder: flat at μ=1 for left side ---
    if kind == "left-shoulder":
        if inputval <= lowval:
            return 1.0
        elif inputval >= highval:
            return 0.0
        elif inputval <= midval:
            return 1.0
        else:
            return (highval - inputval) / (highval - midval)

    # --- Right shoulder: flat at μ=1 for right side ---
    elif kind == "right-shoulder":
        if inputval >= highval:
            return 1.0
        elif inputval <= lowval:
            return 0.0
        elif inputval >= midval:
            return 1.0
        else:
            return (inputval - lowval) / (midval - lowval)

    # --- Normal triangular ---
    else:
        if inputval <= lowval or inputval >= highval:
            return 0.0
        elif inputval == midval:
            return 1.0
        elif lowval < inputval < midval:
            return (inputval - lowval) / (midval - lowval)
        else:
            return (highval - inputval) / (highval - midval)


def trapezoidal(inputval, params):
    """
    Trapezoidal membership function with correct open-end handling.
    Args:
        inputval (float): Crisp input.
        params (tuple): (a, b, c, d).
    """
    a, b, c, d = params
    if not (a <= b <= c <= d):
        raise ValueError("Trapezoidal parameters must satisfy a <= b <= c <= d")

    # Fully outside
    if inputval < a or inputval > d:
        return 0.0

    # Rising edge
    if a < inputval < b:
        return 1.0 if a == b else (inputval - a) / (b - a)

    # Plateau
    if b <= inputval <= c:
        return 1.0

    # Falling edge
    if c < inputval < d:
        return 1.0 if c == d else (d - inputval) / (d - c)

    # Handle open boundaries gracefully
    if inputval == a and a == b:
        return 1.0
    if inputval == d and c == d:
        return 1.0

    return 0.0
