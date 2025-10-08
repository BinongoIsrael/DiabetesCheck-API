import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

VARIABLES = {
    "FBS (mg/dL)": {
        "low": (50, 70, 90),
        "normal": (85, 95, 106),
        "prediabetic": (98, 110, 122), 
        "diabetic": (120, 150, 180),
        "range": (50, 200),
    },
    "BMI": {
        "underweight": (10, 15, 18.5),
        "normal": (17, 22, 24.9),
        "overweight": (23, 26, 30),  
        "obese": (28, 35, 45),
        "range": (10, 45),
    },
    "Age": {
        "young": (15, 25, 35),
        "middle": (33, 45, 57),  
        "old": (53, 65, 77),
        "very_old": (72, 80, 90),
        "range": (15, 90),
    },
    "Physical Activity (mins/week)": {
        "low": (0, 40, 80),
        "moderate": (60, 110, 170),
        "high": (150, 200, 300),
        "range": (0, 300),
    },
    "Risk (Output)": {
        "low_risk": (0.0, 20, 40.0),
        "moderate_risk": (30.0, 50.0, 60.0),
        "high_risk": (58, 80.0, 100.0),
        "range": (0, 100),
    },
}

def trimf_shoulder(x, a, b, c, kind="normal"):
    """Triangular membership function with shoulder support"""
    y = np.zeros_like(x)
    if kind == "left-shoulder":
        y = np.where(x <= b, 1, np.maximum((c - x) / (c - b + 1e-6), 0))
    elif kind == "right-shoulder":
        y = np.where(x >= b, 1, np.maximum((x - a) / (b - a + 1e-6), 0))
    else:
        y = np.maximum(np.minimum((x - a) / (b - a + 1e-6), (c - x) / (c - b + 1e-6)), 0)
    return y

def plot_variable(ax, var_name, terms):
    """Helper function to plot a single variable's membership functions"""
    x = np.linspace(*terms["range"], 300)
    term_labels = [t for t in terms if t != "range"]
    
    colors = plt.cm.Set2(np.linspace(0, 1, len(term_labels)))
    
    for i, label in enumerate(term_labels):
        params = terms[label]
        
        if i == 0:
            kind = "left-shoulder"
        elif i == len(term_labels) - 1:
            kind = "right-shoulder"
        else:
            kind = "normal"
        
        y = trimf_shoulder(x, *params, kind=kind)
        ax.plot(x, y, label=label.replace('_', ' ').title(), 
               linewidth=2.5, color=colors[i])
        ax.fill_between(x, 0, y, alpha=0.1, color=colors[i])
    
    ax.set_title(var_name, fontweight="bold", fontsize=13, pad=12)
    ax.set_xlabel("Value", fontsize=11, fontweight='medium')
    ax.set_ylabel("Membership Degree (μ)", fontsize=11, fontweight='medium')
    ax.set_ylim(-0.05, 1.05)
    ax.legend(loc='best', fontsize=9, framealpha=0.9)
    ax.grid(True, linestyle="--", alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

print("Generating all variables graph...")
fig, axes = plt.subplots(5, 1, figsize=(12, 18))
fig.suptitle("Fuzzy Membership Functions - Diabetes Risk Assessment", 
            fontsize=18, fontweight="bold", y=0.995)

for ax, (var_name, terms) in zip(axes, VARIABLES.items()):
    plot_variable(ax, var_name, terms)

plt.tight_layout()
plt.savefig("all.png", dpi=120, bbox_inches='tight', 
           facecolor='white', edgecolor='none')
plt.close()
print("✓ Saved: all.png")

variable_map = {
    "fbs": "FBS (mg/dL)",
    "bmi": "BMI",
    "age": "Age",
    "physical": "Physical Activity (mins/week)",
    "risk": "Risk (Output)",
}

for var_id, var_name in variable_map.items():
    print(f"Generating {var_id} graph...")
    terms = VARIABLES[var_name]
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    fig.suptitle(f"Fuzzy Membership Functions - {var_name}", 
                fontsize=16, fontweight="bold")
    plot_variable(ax, var_name, terms)
    
    plt.tight_layout()
    plt.savefig(f"{var_id}.png", dpi=120, bbox_inches='tight', 
               facecolor='white', edgecolor='none')
    plt.close()
    print(f"✓ Saved: {var_id}.png")

print("\n✅ All graphs generated in current directory")
print("\nGenerated files:")
print("  - all.png")
print("  - fbs.png")
print("  - bmi.png")
print("  - age.png")
print("  - physical.png")
print("  - risk.png")