import json
import math

# =========================================================
# Load Inputs
# =========================================================

with open("geometry_intelligence_v3.json") as f:
    intel = json.load(f)

with open("advanced_part_classifier_v4.json") as f:
    classification = json.load(f)["classification"]

with open("structural_requirements.json") as f:
    structural = json.load(f)

archetype = classification["archetype"]
structural_demand = structural["structural_demand_index"]

surface = intel["surface_metrics"]
cavity = intel["cavity_metrics"]
mfg = intel["manufacturing_geometry_signals"]

production_volume = 500  # configurable later

# =========================================================
# Utility
# =========================================================

def clamp01(x):
    return max(0.0, min(1.0, x))

# =========================================================
# 1️⃣ Geometry Feasibility (Process Capability)
# =========================================================

def geometry_feasibility(process):

    if process == "CNC_Milling":
        return clamp01(
            mfg["axis_accessibility_score"] * 0.5 +
            (1 - cavity["material_removal_ratio"]) * 0.5
        )

    if process == "CNC_Turning":
        return classification["all_scores"]["rotational_part"]

    if process == "Casting":
        return clamp01(
            cavity["cavity_index"] * 0.6 +
            mfg["draft_feasibility_score"] * 0.4
        )

    if process == "Additive_Manufacturing":
        return clamp01(
            (1 - mfg["overhang_risk"]) * 0.5 +
            cavity["material_removal_ratio"] * 0.5
        )

    if process == "Sheet_Metal":
        return clamp01(
            mfg["developability_index"] * 0.7 +
            (1 - surface["curvature_ratio"]) * 0.3
        )

    return 0.3

# =========================================================
# 2️⃣ Production Economics (Industrial Curves)
# =========================================================

def production_scaling(process):

    if process == "Additive_Manufacturing":
        # exponential decay (realistic additive behavior)
        return clamp01(math.exp(-production_volume / 300))

    if process == "Casting":
        # logistic growth (tooling amortization behavior)
        return clamp01(1 / (1 + math.exp(- (production_volume - 400) / 100)))

    if process == "Sheet_Metal":
        # moderate scaling
        return clamp01(min(production_volume / 800, 1))

    if process in ["CNC_Milling", "CNC_Turning"]:
        # weak volume sensitivity
        return clamp01(1 - production_volume / 2500)

    return 0.5

# =========================================================
# 3️⃣ Tooling Amortization
# =========================================================

def tooling_factor(process):

    if process == "Casting":
        return clamp01(1 / (1 + math.exp(- (production_volume - 500) / 150)))

    if process == "Sheet_Metal":
        return clamp01(production_volume / 1000)

    if process == "Additive_Manufacturing":
        return 0.95  # minimal tooling

    if process in ["CNC_Milling", "CNC_Turning"]:
        return 0.7

    return 0.5

# =========================================================
# 4️⃣ Structural Compatibility
# =========================================================

def structural_compatibility(process):

    if structural_demand < 0.2:
        return 1.0

    if process == "Sheet_Metal":
        return clamp01(1 - structural_demand * 0.7)

    if process == "Additive_Manufacturing":
        return clamp01(1 - structural_demand * 0.6)

    if process == "Casting":
        return clamp01(1 - structural_demand * 0.4)

    return 1.0

# =========================================================
# 5️⃣ Sustainability (Low Weight)
# =========================================================

def sustainability(process):

    waste = cavity["material_removal_ratio"]

    if process in ["CNC_Milling", "CNC_Turning"]:
        return clamp01(1 - waste)

    if process == "Additive_Manufacturing":
        return clamp01(1 - mfg["overhang_risk"])

    if process == "Casting":
        return 0.6

    if process == "Sheet_Metal":
        return 0.75

    return 0.5

# =========================================================
# 6️⃣ Final Weighted Model
# Economics Dominant
# =========================================================

processes = [
    "CNC_Milling",
    "CNC_Turning",
    "Casting",
    "Additive_Manufacturing",
    "Sheet_Metal"
]

results = []

for p in processes:

    geo = geometry_feasibility(p)
    prod = production_scaling(p)
    tool = tooling_factor(p)
    struct_fit = structural_compatibility(p)
    sustain = sustainability(p)

    manufacturability_index = clamp01(
        geo * 0.25 +
        prod * 0.45 +      # dominant economic driver
        tool * 0.15 +
        struct_fit * 0.10 +
        sustain * 0.05
    )

    results.append({
        "process": p,
        "geometry_feasibility": round(geo, 4),
        "production_scaling": round(prod, 4),
        "tooling_factor": round(tool, 4),
        "structural_compatibility": round(struct_fit, 4),
        "sustainability_index": round(sustain, 4),
        "manufacturability_index": round(manufacturability_index, 4)
    })

results.sort(key=lambda x: x["manufacturability_index"], reverse=True)

final = {
    "archetype_considered": archetype,
    "production_volume": production_volume,
    "structural_demand_index": structural_demand,
    "process_rankings": results
}

with open("industrial_manufacturing_analysis_v6.json", "w") as f:
    json.dump(final, f, indent=4)

print(json.dumps(final, indent=4))
print("✅ industrial_manufacturing_analysis_v6.json saved.")