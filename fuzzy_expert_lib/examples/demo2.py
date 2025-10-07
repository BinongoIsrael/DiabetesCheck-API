from fuzzy_expert import FuzzyExpertSystem

if __name__ == "__main__":
    fes = FuzzyExpertSystem()
    
    # Add variables
    fes.add_variable('MaskedRegion', {
        'Very Low': (0, 5, 15),
        'Low': (10, 17.5, 25), 
        'Moderate': (20, 30, 40),
        'High': (35, 47.5, 60),
        'Very High': (55, 77.5, 100)
    })
    fes.add_variable('Variance', {
        'Very Low': (0, 40, 65),
        'Low': (50, 75, 100), 
        'Moderate': (85, 110, 135),
        'High': (120, 145, 170),
        'Very High': (155, 180, 300)
    })


    
    # Define output terms
    fes.add_output_term('Not Infected', (0,17.5, 35))
    fes.add_output_term('Moderately Infected', (30, 47.5, 65))
    fes.add_output_term('Highly Infected', (60, 75, 100))
    
    # Add rule: IF temp is hot THEN high_fan
    # Very Low MaskedRegion
    fes.add_rule([('MaskedRegion', 'Very Low'), ('Variance', 'Very Low')], 'Moderately Infected')
    fes.add_rule([('MaskedRegion', 'Very Low'), ('Variance', 'Low')], 'Moderately Infected')
    fes.add_rule([('MaskedRegion', 'Very Low'), ('Variance', 'Moderate')], 'Not Infected')
    fes.add_rule([('MaskedRegion', 'Very Low'), ('Variance', 'High')], 'Not Infected')
    fes.add_rule([('MaskedRegion', 'Very Low'), ('Variance', 'Very High')], 'Not Infected')

    # Low MaskedRegion
    fes.add_rule([('MaskedRegion', 'Low'), ('Variance', 'Very Low')], 'Highly Infected')
    fes.add_rule([('MaskedRegion', 'Low'), ('Variance', 'Low')], 'Moderately Infected')
    fes.add_rule([('MaskedRegion', 'Low'), ('Variance', 'Moderate')], 'Moderately Infected')
    fes.add_rule([('MaskedRegion', 'Low'), ('Variance', 'High')], 'Moderately Infected')
    fes.add_rule([('MaskedRegion', 'Low'), ('Variance', 'Very High')], 'Moderately Infected')

    # Moderate MaskedRegion
    fes.add_rule([('MaskedRegion', 'Moderate'), ('Variance', 'Very Low')], 'Highly Infected')
    fes.add_rule([('MaskedRegion', 'Moderate'), ('Variance', 'Low')], 'Highly Infected')
    fes.add_rule([('MaskedRegion', 'Moderate'), ('Variance', 'Moderate')], 'Moderately Infected')
    fes.add_rule([('MaskedRegion', 'Moderate'), ('Variance', 'High')], 'Moderately Infected')
    fes.add_rule([('MaskedRegion', 'Moderate'), ('Variance', 'Very High')], 'Moderately Infected')

    # High MaskedRegion
    fes.add_rule([('MaskedRegion', 'High'), ('Variance', 'Very Low')], 'Highly Infected')
    fes.add_rule([('MaskedRegion', 'High'), ('Variance', 'Low')], 'Highly Infected')
    fes.add_rule([('MaskedRegion', 'High'), ('Variance', 'Moderate')], 'Highly Infected')
    fes.add_rule([('MaskedRegion', 'High'), ('Variance', 'High')], 'Moderately Infected')
    fes.add_rule([('MaskedRegion', 'High'), ('Variance', 'Very High')], 'Moderately Infected')

    # Very High MaskedRegion
    fes.add_rule([('MaskedRegion', 'Very High'), ('Variance', 'Very Low')], 'Highly Infected')
    fes.add_rule([('MaskedRegion', 'Very High'), ('Variance', 'Low')], 'Highly Infected')
    fes.add_rule([('MaskedRegion', 'Very High'), ('Variance', 'Moderate')], 'Highly Infected')
    fes.add_rule([('MaskedRegion', 'Very High'), ('Variance', 'High')], 'Highly Infected')
    fes.add_rule([('MaskedRegion', 'Very High'), ('Variance', 'Very High')], 'Moderately Infected')


    
    # Assess input
    crisp_output, classification = fes.assess({'MaskedRegion': 0, 'Variance': 300})
    print("Centroid:", crisp_output)
    print("Classification:", classification)

