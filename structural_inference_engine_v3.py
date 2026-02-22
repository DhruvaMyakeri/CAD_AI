import json
import math

# =========================================================
# Load Inputs
# =========================================================

with open("geometry_intelligence_v3.json") as f:
    intel = json.load(f)

with open("advanced_part_classifier_v4.json") as f:
    classification = json.load(f)["classification"]

archetype = classification["archetype"]

struct = intel["structural_signals"]
surface = intel["surface_metrics"]
cavity = intel["cavity_metrics"]
holes = intel["hole_intelligence"]

# =========================================================
# Utility
# =========================================================

def clamp01(x):
    return max(0.0, min(1.0, x))

# =========================================================
# Failure Mode Weighting by Archetype
# =========================================================

mode_weights = {
    "bending": 0,
    "torsion": 0,
    "buckling": 0,
    "membrane": 0,
    "stress_concentration": 0
}

if archetype == "beam_or_frame_member":
    mode_weights.update({
        "bending": 0.5,
        "buckling": 0.3,
        "stress_concentration": 0.2
    })

elif archetype == "rotational_part":
    mode_weights.update({
        "torsion": 0.5,
        "bending": 0.2,
        "stress_concentration": 0.3
    })

elif archetype == "thin_shell_or_housing":
    mode_weights.update({
        "membrane": 0.4,
        "buckling": 0.4,
        "stress_concentration": 0.2
    })

elif archetype == "plate_like":
    mode_weights.update({
        "bending": 0.5,
        "membrane": 0.3,
        "stress_concentration": 0.2
    })

elif archetype == "feature_dense_component":
    mode_weights.update({
        "stress_concentration": 0.6,
        "bending": 0.2,
        "torsion": 0.2
    })

else:  # bracket_or_prismatic default
    mode_weights.update({
        "bending": 0.4,
        "stress_concentration": 0.4,
        "torsion": 0.2
    })

# =========================================================
# Demand Estimation (Deterministic)
# =========================================================

slenderness = struct["slenderness_index"]
thinness = struct["thinness_risk_score"]
instability = struct["section_instability_index"]
hole_factor = clamp01(holes["total_cylindrical_features"] / 20)

bending_demand = slenderness * 15
torsion_demand = surface["curvature_ratio"] * 120
buckling_demand = instability * 100
membrane_demand = cavity["material_removal_ratio"] * 60
stress_concentration_demand = hole_factor * 120

required_yield_strength = (
    bending_demand * mode_weights["bending"] +
    torsion_demand * mode_weights["torsion"] +
    buckling_demand * mode_weights["buckling"] +
    membrane_demand * mode_weights["membrane"] +
    stress_concentration_demand * mode_weights["stress_concentration"]
)

required_modulus = (
    slenderness * 2.5 +
    instability * 50 +
    thinness * 30
)

structural_demand_index = clamp01(required_yield_strength / 500)

result = {
    "archetype_considered": archetype,
    "failure_mode_weights": mode_weights,
    "required_yield_strength_MPa": round(required_yield_strength, 3),
    "required_modulus_GPa": round(required_modulus, 3),
    "structural_demand_index": round(structural_demand_index, 4)
}

with open("structural_requirements.json", "w") as f:
    json.dump(result, f, indent=4)

print(json.dumps(result, indent=4))
print("✅ structural_requirements.json saved.")