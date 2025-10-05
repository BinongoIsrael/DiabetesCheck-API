# fuzzy_expert/defuzzify.py
# def defuzzify_centroid(rules_output):
#     """
#     Centroid defuzzification.
#     rules_output: list of tuples (term, strength, params, centroid, area)
#     """
#     numerator = 0.0
#     denominator = 0.0

#     for term, strength, params, centroid, area in rules_output:
#         if strength <= 0 or area <= 0:
#             continue
#         numerator += centroid * area
#         denominator += area

#     return numerator / denominator if denominator != 0 else 0.0

# fuzzy_expert/defuzzify.py
def defuzzify_centroid(rules_output, debug=False):
    """
    Centroid defuzzification with optional debug output.
    rules_output: list of tuples (term, strength, params, centroid, area)
    """
    numerator = 0.0
    denominator = 0.0

    if debug:
        print("\n--- Defuzzification Breakdown ---")

    for term, strength, params, centroid, area in rules_output:
        if strength <= 0 or area <= 0:
            continue

        contribution = centroid * area
        numerator += contribution
        denominator += area

        if debug:
            print(
                f"Output term: {term}\n"
                f"  Strength (μ): {strength:.4f}\n"
                f"  Params: {params}\n"
                f"  Centroid: {centroid:.4f}\n"
                f"  Area: {area:.4f}\n"
                f"  Contribution (centroid*area): {contribution:.4f}\n"
            )

    if debug:
        print(f"Total numerator = {numerator:.4f}")
        print(f"Total denominator = {denominator:.4f}")
        print(f"Crisp result = {numerator / denominator if denominator != 0 else 0.0:.4f}")
        print("--- End Debug ---\n")

    return numerator / denominator if denominator != 0 else 0.0

