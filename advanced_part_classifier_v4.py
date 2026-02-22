import json
import math

# =========================================================
# Load Inputs
# =========================================================

with open("geometry_signature.json") as f:
    sig = json.load(f)

with open("geometry_intelligence_v3.json") as f:
    intel = json.load(f)

face = sig["face_distribution"]
bbox = sig["bounding_box"]
axis_sig = sig["axis_distribution"]

surface = intel["surface_metrics"]
cavity = intel["cavity_metrics"]
struct = intel["structural_signals"]
holes = intel["hole_intelligence"]
mfg = intel["manufacturing_geometry_signals"]
sym = intel["symmetry_metrics"]

# =========================================================
# Utility
# =========================================================

def clamp01(x):
    return max(0.0, min(1.0, x))

def safe_div(a, b):
    return a / b if b != 0 else 0

# =========================================================
# Archetype Scoring (Geometry-Strict)
# =========================================================

scores = {}

# ---------------------------------------------------------
# 1️⃣ Rotational Part
# Dominant cylindrical area + strong axis symmetry
# ---------------------------------------------------------

rotational_score = (
    sym["rotational_symmetry_likelihood"] * 0.5 +
    face["cylindrical_ratio"] * 0.3 +
    axis_sig["dominant_axis_ratio"] * 0.2
)

scores["rotational_part"] = clamp01(rotational_score)

# ---------------------------------------------------------
# 2️⃣ Beam / Frame Member
# High slenderness + structural instability tendency
# ---------------------------------------------------------

beam_score = (
    clamp01(safe_div(struct["slenderness_index"], 5)) * 0.6 +
    clamp01(struct["section_instability_index"]) * 0.4
)

scores["beam_or_frame_member"] = clamp01(beam_score)

# ---------------------------------------------------------
# 3️⃣ Plate-like
# Low slenderness + high developability + planar dominance
# ---------------------------------------------------------

plate_score = (
    face["planar_ratio"] * 0.4 +
    mfg["developability_index"] * 0.4 +
    (1 - struct["slenderness_index"] / 5) * 0.2
)

scores["plate_like"] = clamp01(plate_score)

# ---------------------------------------------------------
# 4️⃣ Thin Shell / Housing
# High cavity + high material removal + thinness risk
# ---------------------------------------------------------

shell_score = (
    cavity["material_removal_ratio"] * 0.4 +
    struct["thinness_risk_score"] * 0.3 +
    cavity["cavity_index"] * 0.3
)

scores["thin_shell_or_housing"] = clamp01(shell_score)

# ---------------------------------------------------------
# 5️⃣ Bracket / Prismatic
# High prismatic symmetry + moderate holes + moderate curvature
# ---------------------------------------------------------

bracket_score = (
    sym["prismatic_symmetry_likelihood"] * 0.4 +
    clamp01(safe_div(holes["total_cylindrical_features"], 20)) * 0.3 +
    (1 - surface["curvature_ratio"]) * 0.3
)

scores["bracket_or_prismatic"] = clamp01(bracket_score)

# ---------------------------------------------------------
# 6️⃣ Feature Dense Component
# Many unique diameters + multi-axis drilling
# ---------------------------------------------------------

feature_dense_score = (
    clamp01(safe_div(holes["unique_diameter_count"], 10)) * 0.4 +
    clamp01(safe_div(holes["multi_axis_drilling_index"], 5)) * 0.4 +
    clamp01(holes["hole_density"] * 100) * 0.2
)

scores["feature_dense_component"] = clamp01(feature_dense_score)

# =========================================================
# Normalize Scores
# =========================================================

max_score = max(scores.values()) if scores else 0

normalized_scores = {}

for k, v in scores.items():
    normalized_scores[k] = round(safe_div(v, max_score), 4) if max_score else 0

# =========================================================
# Confidence Calculation
# Based on separation between top two scores
# =========================================================

sorted_scores = sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True)

if len(sorted_scores) >= 2:
    separation = sorted_scores[0][1] - sorted_scores[1][1]
else:
    separation = 0

confidence = clamp01(separation + sorted_scores[0][1] * 0.5)

# =========================================================
# Final Output
# =========================================================

result = {
    "classification": {
        "archetype": sorted_scores[0][0],
        "confidence": round(confidence, 4),
        "all_scores": normalized_scores,
        "raw_scores": {k: round(v, 4) for k, v in scores.items()},
        "decision_basis": {
            "slenderness_index": struct["slenderness_index"],
            "thinness_risk_score": struct["thinness_risk_score"],
            "curvature_ratio": surface["curvature_ratio"],
            "material_removal_ratio": cavity["material_removal_ratio"],
            "hole_count": holes["total_cylindrical_features"],
            "unique_diameters": holes["unique_diameter_count"],
            "dominant_axis_ratio": axis_sig["dominant_axis_ratio"],
            "developability_index": mfg["developability_index"]
        }
    }
}

with open("advanced_part_classifier_v4.json", "w") as f:
    json.dump(result, f, indent=4)

print(json.dumps(result, indent=4))
print("✅ advanced_part_classifier_v4.json saved.")