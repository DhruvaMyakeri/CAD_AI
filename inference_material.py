import json
import math

GEOMETRY_PATH = r"D:\PROJECTS\CAD_ai\geometry.json"
FEATURES_PATH = r"D:\PROJECTS\CAD_ai\features.json"
MATERIAL_PATH = r"D:\PROJECTS\CAD_ai\material.json"

# --------------------------------------------------
# Load Data
# --------------------------------------------------

with open(GEOMETRY_PATH) as f:
    geometry = json.load(f)

with open(FEATURES_PATH) as f:
    features = json.load(f)

with open(MATERIAL_PATH) as f:
    materials = json.load(f)

bbox = geometry["global"]["bounding_box"]
wall_stats = geometry["wall_thickness_distribution"]

max_span = max(bbox["x"], bbox["y"], bbox["z"])
min_thickness = wall_stats.get("min", 1.0)

slenderness_ratio = max_span / min_thickness
thickness_ratio = min_thickness / max_span

axis_count = len(set(tuple(g["axis"]) for g in features["hole_groups"]))
total_features = (
    len(features["holes"]["through"]) +
    len(features["holes"]["blind"]) +
    len(features["slots"])
)

# --------------------------------------------------
# Material Evaluation
# --------------------------------------------------

ranked = []

for mat in materials:

    reasons = []
    penalties = 0

    mech = mat["mechanical"]
    manuf = mat["manufacturing"]
    env = mat["environmental"]
    econ = mat["economic"]

    E = mech["youngs_modulus_GPa"]
    yield_strength = mech["yield_strength_MPa"]
    elongation = mech["elongation_percent"]
    fatigue = mech["fatigue_strength_MPa"]
    density = mech["density_kg_m3"]

    machinability = manuf["machinability_rating_percent"] / 100

    # --------------------------------------------------
    # 1️⃣ Structural Stiffness
    # --------------------------------------------------

    required_modulus = 5 + slenderness_ratio * 0.5
    stiffness_factor = min(E / required_modulus, 1.0)

    if stiffness_factor < 0.5:
        penalties += 0.2
        reasons.append("low_stiffness")
    else:
        reasons.append("adequate_stiffness")

    # --------------------------------------------------
    # 2️⃣ Strength
    # --------------------------------------------------

    required_strength = 50 + slenderness_ratio * 5
    strength_factor = min(yield_strength / required_strength, 1.0)

    if strength_factor < 0.5:
        penalties += 0.2
        reasons.append("low_strength")
    else:
        reasons.append("adequate_strength")

    # --------------------------------------------------
    # 3️⃣ Ductility (New)
    # Thin + brittle = bad
    # --------------------------------------------------

    if slenderness_ratio > 15:
        if elongation < 5:
            penalties += 0.15
            reasons.append("brittle_for_slender_geometry")
        else:
            reasons.append("sufficient_ductility")

    # --------------------------------------------------
    # 4️⃣ Fatigue Sensitivity (New)
    # Many features → fatigue risk
    # --------------------------------------------------

    if total_features > 15:
        fatigue_required = 100
        fatigue_factor = min(fatigue / fatigue_required, 1.0)

        if fatigue_factor < 0.5:
            penalties += 0.1
            reasons.append("low_fatigue_resistance")
        else:
            reasons.append("adequate_fatigue_resistance")

    # --------------------------------------------------
    # 5️⃣ Manufacturability
    # --------------------------------------------------

    if axis_count >= 3 and machinability < 0.4:
        penalties += 0.1
        reasons.append("difficult_multi_axis_machining")
    else:
        reasons.append("machinable")

    # --------------------------------------------------
    # 6️⃣ Density Moderation
    # Heavy materials penalized slightly for large parts
    # --------------------------------------------------

    if density > 7500:
        penalties += 0.05
        reasons.append("high_density_weight_penalty")

    # --------------------------------------------------
    # 7️⃣ Economic
    # --------------------------------------------------

    penalties += econ["relative_cost_index_0_1"] * 0.05

    # --------------------------------------------------
    # Final Score
    # --------------------------------------------------

    base_score = (
        0.35 * stiffness_factor +
        0.35 * strength_factor +
        0.15 * machinability +
        0.15 * min(elongation / 20, 1.0)
    )

    score = base_score - penalties
    score = max(min(score, 1.0), 0.0)

    confidence = max(1 - penalties, 0)

    ranked.append({
        "material": mat["name"],
        "category": mat["category"],
        "score": round(score, 3),
        "confidence": round(confidence, 3),
        "reasons": reasons
    })

# --------------------------------------------------
# Sort & Output
# --------------------------------------------------

# --------------------------------------------------
# Sort & Output
# --------------------------------------------------

ranked_sorted = sorted(ranked, key=lambda x: x["score"], reverse=True)

output = {
    "material_recommendations": ranked_sorted[:5]
}

# ✅ Save to JSON (required by master_engine_v5)
with open("material_recommendations.json", "w") as f:
    json.dump(output, f, indent=4)

print(json.dumps(output, indent=4))
print("✅ material_recommendations.json saved.")