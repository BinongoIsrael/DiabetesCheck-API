from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fuzzy_expert_lib.fuzzy_expert.system import FuzzyExpertSystem
from typing import Dict, Any
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io

# --- Initialization ---
app = FastAPI(
    title="Fuzzy Diabetes Risk Assessment",
    description="A fuzzy logic system for assessing diabetes risk based on key physiological and lifestyle factors."
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for input data validation
class Inputs(BaseModel):
    fbs: float  
    bmi: float 
    age: float
    physical_activity: float

# --- Variable Definitions for Plotting ---
VARIABLES = {
    "FBS (mg/dL)": {
        "low": (50, 70, 90),
        "normal": (85, 95, 106),
        "prediabetic": (99, 110, 125),
        "diabetic": (120, 150, 180),
        "range": (50, 200),
    },
    "BMI": {
        "underweight": (10.0, 15, 18.5),
        "normal": (17, 22, 24.9),
        "overweight": (24, 27, 30),
        "obese": (28, 35, 45),
        "range": (10, 45),
    },
    "Age": {
        "young": (15.0, 25.0, 35.0),
        "middle": (30.0, 45.0, 55.0),
        "old": (50.0, 65, 77.0),
        "very_old": (72.0, 80, 90.0),
        "range": (15, 90),
    },
    "Physical Activity (mins/week)": {
        "low":      (0, 40, 80),      
        "moderate": (60, 110, 170),   
        "high":     (150, 200, 300),
        "range": (0, 300),
    },
    "Risk (Output)": {
        "low_risk": (0.0, 20, 40.0),
        "moderate_risk": (30.0, 50.0, 60.0),
        "high_risk": (58, 80.0, 100.0),
        "range": (0, 100),
    },
}

FUZZY_SYSTEM = None

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

def initialize_fuzzy_system():
    system = FuzzyExpertSystem()

    system.add_variable("fbs", {
        "low": (50, 70, 90),
        "normal": (85, 95, 106),
        "prediabetic": (98, 110, 122), 
        "diabetic": (120, 150, 180),
    })

    system.add_variable("bmi", {
        "underweight": (10, 15, 18.5),
        "normal": (17, 22, 24.9),
        "overweight": (23, 26, 30),  
        "obese": (28, 35, 45),
    })

    system.add_variable("age", {
        "young": (15, 25, 35),
        "middle": (33, 45, 57),  
        "old": (53, 65, 77),
        "very_old": (72, 80, 90),
    })

    system.add_variable("physical_activity", {
        "low": (0, 40, 80),
        "moderate": (60, 110, 170),
        "high": (150, 200, 300),
    })

    # --- Output Terms ---
    system.add_output_term("low_risk", (0, 20, 40))
    system.add_output_term("moderate_risk", (30, 50, 60))
    system.add_output_term("high_risk", (58, 80, 100))

    # --- HIGH RISK RULES ---
    system.add_rule([("fbs", "diabetic")], "high_risk")
    system.add_rule([("fbs", "prediabetic"), ("bmi", "obese"), ("age", "old")], "high_risk")
    system.add_rule([("fbs", "prediabetic"), ("bmi", "obese"), ("physical_activity", "low")], "high_risk")
    system.add_rule([("bmi", "obese"), ("age", "very_old"), ("physical_activity", "low")], "high_risk")
    system.add_rule([("bmi", "obese"), ("age", "old"), ("physical_activity", "low")], "high_risk")
    system.add_rule([("fbs", "prediabetic"), ("bmi", "overweight"), ("age", "old"), ("physical_activity", "low")], "high_risk")
    system.add_rule([("fbs", "prediabetic"), ("age", "very_old")], "high_risk")
    system.add_rule([("fbs", "prediabetic"), ("age", "old"), ("physical_activity", "low")], "high_risk")
    system.add_rule([("age", "very_old"), ("physical_activity", "low")], "high_risk")
    system.add_rule([("age", "old"), ("bmi", "normal"), ("physical_activity", "low")], "high_risk")

    # --- MODERATE RISK RULES ---
    system.add_rule([("fbs", "prediabetic"), ("bmi", "normal"), ("age", "middle")], "moderate_risk")
    system.add_rule([("fbs", "prediabetic"), ("bmi", "normal"), ("age", "young")], "moderate_risk")
    system.add_rule([("fbs", "normal"), ("bmi", "obese"), ("age", "middle"), ("physical_activity", "moderate")], "moderate_risk")
    system.add_rule([("bmi", "overweight"), ("age", "middle"), ("physical_activity", "low")], "moderate_risk")
    system.add_rule([("bmi", "obese"), ("age", "young")], "moderate_risk")
    system.add_rule([("age", "old"), ("physical_activity", "low")], "moderate_risk")
    system.add_rule([("fbs", "prediabetic"), ("bmi", "overweight"), ("physical_activity", "moderate")], "moderate_risk")
    system.add_rule([("age", "old"), ("fbs", "normal"), ("physical_activity", "low")], "moderate_risk")
    system.add_rule([("age", "very_old"), ("fbs", "normal")], "moderate_risk")
    system.add_rule([("fbs", "prediabetic"), ("age", "middle")], "moderate_risk")
    system.add_rule([("fbs", "prediabetic"), ("bmi", "overweight")], "moderate_risk")
    system.add_rule([("fbs", "prediabetic"), ("physical_activity", "low")], "moderate_risk")
    system.add_rule([("fbs", "prediabetic"), ("bmi", "normal"), ("physical_activity", "moderate")], "moderate_risk")
    system.add_rule([("age", "very_old"), ("fbs", "normal"), ("physical_activity", "moderate")], "moderate_risk")
    system.add_rule([("fbs", "normal"), ("bmi", "normal"), ("age", "old"), ("physical_activity", "moderate")], "moderate_risk")
    system.add_rule([("fbs", "normal"), ("bmi", "overweight"), ("age", "middle"), ("physical_activity", "moderate")], "moderate_risk")
    system.add_rule([("fbs", "normal"), ("bmi", "obese"), ("age", "old"), ("physical_activity", "moderate")], "moderate_risk")
    system.add_rule([("fbs", "normal"), ("bmi", "obese"), ("age", "old"), ("physical_activity", "high")], "moderate_risk")
    system.add_rule([("fbs", "low"), ("bmi", "obese"), ("age", "young"), ("physical_activity", "high")], "moderate_risk") 

    # --- LOW RISK RULES ---
    system.add_rule([("fbs", "normal"), ("bmi", "normal"), ("age", "young"), ("physical_activity", "high")], "low_risk")
    system.add_rule([("fbs", "normal"), ("bmi", "normal"), ("age", "young")], "low_risk")
    system.add_rule([("fbs", "normal"), ("bmi", "normal"), ("physical_activity", "high")], "low_risk")
    system.add_rule([("fbs", "normal"), ("bmi", "normal"), ("age", "middle")], "low_risk")
    system.add_rule([("physical_activity", "high"), ("age", "young"), ("fbs", "normal")], "low_risk")
    system.add_rule([("physical_activity", "high"), ("age", "young"), ("bmi", "normal")], "low_risk")
    system.add_rule([("fbs", "normal"), ("physical_activity", "high"), ("age", "young"), ("bmi", "normal")], "low_risk")
    system.add_rule([("fbs", "low")], "low_risk")

    return system

FUZZY_SYSTEM = initialize_fuzzy_system()

@app.get("/")
def read_root():
    return {"message": "Fuzzy Diabetes Risk Assessment API is running"}

@app.post("/assess", response_model=Dict[str, Any])
def assess_risk(inputs: Inputs):
    """Calculates the diabetes risk using the fuzzy expert system."""
    global FUZZY_SYSTEM

    crisp_value, classification = FUZZY_SYSTEM.assess({
        "fbs": inputs.fbs,
        "bmi": inputs.bmi,
        "age": inputs.age,
        "physical_activity": inputs.physical_activity,
    })

    return {
        "crispValue": round(crisp_value, 2),
        "classification": classification.replace("_risk", "").capitalize() 
    }

@app.get("/plot/{variable}")
async def get_plot(variable: str):
    """
    Generate a membership function plot for a specific variable.
    
    Parameters:
    - variable: fbs, bmi, age, physical, risk, or all
    """
    variable_map = {
        "fbs": "FBS (mg/dL)",
        "bmi": "BMI",
        "age": "Age",
        "physical": "Physical Activity (mins/week)",
        "risk": "Risk (Output)",
        "all": "all"
    }
    
    if variable not in variable_map:
        return {"error": "Invalid variable. Use: fbs, bmi, age, physical, risk, or all"}
    
    try:
        plt.close('all')
        
        if variable == "all":
            fig, axes = plt.subplots(5, 1, figsize=(12, 18))
            fig.suptitle("Fuzzy Membership Functions - Diabetes Risk Assessment", 
                        fontsize=18, fontweight="bold", y=0.995)
            
            for ax, (var_name, terms) in zip(axes, VARIABLES.items()):
                plot_variable(ax, var_name, terms)
        else:
            var_name = variable_map[variable]
            terms = VARIABLES[var_name]
            
            fig, ax = plt.subplots(1, 1, figsize=(12, 6))
            fig.suptitle(f"Fuzzy Membership Functions - {var_name}", 
                        fontsize=16, fontweight="bold")
            plot_variable(ax, var_name, terms)
        
        plt.tight_layout()
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=120, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        buf.seek(0)
        plt.close('all')
        
        return StreamingResponse(buf, media_type="image/png")
    
    except Exception as e:
        plt.close('all') 
        return {"error": f"Failed to generate plot: {str(e)}"}