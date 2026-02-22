# precision_intelligence.py

import json
import math

def clamp(x, low=0.0, high=1.0):
    return max(low, min(high, x))

def normalize(x):
    return round(x, 4)

# ---------------------------------------------
# Load Geometry Intelligence
# ---------------------------------------------

def load_geometry():
    with open("geometry_intelligence_v2.json", "r") as f:
        return json.load(f)

# ---------------------------------------------
# Precision Complexity Model
# ---------------------------------------------

def evaluate_precision():

    gi = load_geometry()

    axis_count = gi["accessibility"]["axis_count"]
    cavity = gi["material_distribution"]["cavity_index"]
    complexity_3d = gi["manufacturing_constraints"]["complexity_3d_index"]
    slenderness = gi["dimensional_profile"]["slenderness_index"]

    micro_feature_factor = cavity
    alignment_sensitivity = axis_count / 5
    geometric_precision_risk = complexity_3d

    precision_difficulty_index = (
        0.3 * micro_feature_factor +
        0.3 * alignment_sensitivity +
        0.4 * geometric_precision_risk
    )

    precision_difficulty_index = clamp(precision_difficulty_index)

    # Classification
    if precision_difficulty_index < 0.3:
        tolerance_class = "Standard Industrial"
    elif precision_difficulty_index < 0.6:
        tolerance_class = "Moderate Precision"
    else:
        tolerance_class = "High Precision Required"

    output = {
        "precision_analysis": {
            "precision_difficulty_index": normalize(precision_difficulty_index),
            "recommended_tolerance_class": tolerance_class,
            "axis_count": axis_count,
            "complexity_index": normalize(complexity_3d),
            "slenderness_index": normalize(slenderness)
        }
    }

    with open("precision_analysis.json", "w") as f:
        json.dump(output, f, indent=4)

    print(json.dumps(output, indent=4))

if __name__ == "__main__":
    evaluate_precision()