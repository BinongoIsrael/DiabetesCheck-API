from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fuzzy_expert_lib.fuzzy_expert.system import FuzzyExpertSystem
from typing import Dict, Any

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

FUZZY_SYSTEM = None

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