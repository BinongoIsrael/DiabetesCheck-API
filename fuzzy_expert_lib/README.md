# Fuzzy Expert System Library

A lightweight Python library for building **fuzzy expert systems**, useful for applications like medical risk assessment, control systems, and decision-making.

---

## 🚀 Features
- **Membership Functions**: Triangular and trapezoidal membership functions.
- **Fuzzification**: Convert crisp inputs to fuzzy values.
- **Rule Evaluation**: Define and evaluate fuzzy rules.
- **Defuzzification**: Centroid method for crisp output.
- **Modular Design**: Easy to extend and customize.

---

## 📦 Installation

Clone this repository and install it in editable mode:

```bash
git clone https://github.com/your_username/fuzzy_expert_system.git
cd fuzzy_expert_system
pip install -e .
```

```markdown
# Fuzzy Expert System Documentation

## 🔧 Usage

### Basic Example

```python
from fuzzy_expert.system import FuzzyExpertSystem

# Create a fuzzy expert system
system = FuzzyExpertSystem()

# Add input variables
system.add_variable('fbs', {
    'low': (50, 65, 80),
    'high': (90, 105, 125)
})

# Add output terms
system.add_output_term('low_risk', (0, 50, 100))   # triangular
system.add_output_term('high_risk', (50, 100, 150))

# Add rules
system.add_rule([('fbs', 'low')], 'low_risk')
system.add_rule([('fbs', 'high')], 'high_risk')

# Assess risk
crisp_value, classification = system.assess({'fbs': 60})
print(f"Crisp output: {crisp_value:.2f}, Classified as: {classification}")
```

## 📚 API Reference

### FuzzyExpertSystem Class

- `add_variable(name, terms)` → Add an input variable with membership terms.
- `add_output_term(term, params)` → Define an output fuzzy set (triangular/trapezoidal).
- `add_rule(conditions, output_term)` → Add a fuzzy rule.
- `assess(inputs)` → Run inference and return (crisp_value, best_term).

### Membership Functions

- `triangular(x, (a, b, c))` → Triangular membership.
- `trapezoidal(x, (a, b, c, d))` → Trapezoidal membership.

### Fuzzification

- `fuzzify_variable(value, terms)` → Convert crisp value to fuzzy terms.

### Rules

- `Rule(antecedents, consequent)` → Define a fuzzy rule.
- `.evaluate(fuzzified_inputs)` → Evaluate a rule given fuzzified values.

### Inference

- `evaluate_rules(rules, fuzzified_inputs)` → Aggregate rule outputs.

### Defuzzification

- `defuzzify_centroid(rules_output)` → Centroid defuzzification method.

## 🔄 System Flow

```mermaid
flowchart LR
    A[Crisp Inputs] --> B[Fuzzification]
    B --> C[Fuzzy Rules]
    C --> D[Inference Engine]
    D --> E[Defuzzification]
    E --> F[Crisp Output + Classification]
```

## 🧪 Running Tests

Run all tests with:

```bash
python -m pytest tests/
```

## 🤝 Contributing

Contributions are welcome!

- Open an issue to discuss new features or bugs.
- Submit a pull request with improvements.
