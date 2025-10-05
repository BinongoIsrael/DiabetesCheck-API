from fuzzy_expert import FuzzyExpertSystem

if __name__ == "__main__":
    fes = FuzzyExpertSystem()
    
    # Add variables
    fes.add_variable('temp', {
        'low': (15, 20, 25), 
        'medium': (20, 25, 30),
        'high': (25, 30, 35)
    })
    fes.add_variable('humidity', {
        'low': (20, 40, 60),
        'high':(40, 60, 80)
    })


    
    # Define output terms
    fes.add_output_term('slow', (0,20, 40))
    fes.add_output_term('medium', (30, 50, 70))
    fes.add_output_term('fast', (60, 80, 100))
    
    # Add rule: IF temp is hot THEN high_fan
    fes.add_rule([('temp', 'low'), ('humidity', 'low')], 'slow')
    fes.add_rule([('temp', 'low'), ('humidity', 'high')], 'medium')
    fes.add_rule([('temp', 'medium'), ('humidity', 'low')], 'slow')
    fes.add_rule([('temp', 'medium'), ('humidity', 'high')], 'medium')
    fes.add_rule([('temp', 'high'), ('humidity', 'low')], 'medium')
    fes.add_rule([('temp', 'high'), ('humidity', 'high')], 'fast')


    
    # Assess input
    crisp_output, classification = fes.assess({'temp': 28 , 'humidity': 70})
    print("Fan speed:", crisp_output)
    print("Classification:", classification)
