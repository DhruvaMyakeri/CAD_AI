import json
import math
from collections import Counter

# ==========================================
# Load Inputs
# ==========================================

with open("geometry_signature.json") as f:
    sig = json.load(f)

with open("geometry.json") as f:
    geometry = json.load(f)

faces = geometry.get("faces", [])
volume = geometry["global"]["volume"]
bbox = sig["bounding_box"]["dimensions_mm"]

# ==========================================
# 1️⃣ Surface Intelligence
# ==========================================

total_surface_area = sum(f.get("area", 0) for f in faces)

surface_to_volume_ratio = (
    total_surface_area / volume if volume > 0 else 0
)

compactness_index = (
    (volume ** (2/3)) / total_surface_area
    if total_surface_area > 0 else 0
)

cyl_area = sum(f["area"] for f in faces if f.get("type") == "cylinder")
plane_area = sum(f["area"] for f in faces if f.get("type") == "plane")

curvature_ratio = cyl_area / total_surface_area if total_surface_area else 0

# ==========================================
# 2️⃣ Cavity & Material Removal Intelligence
# ==========================================

bbox_volume = sig["bounding_box"]["bbox_volume_mm3"]
volume_efficiency = sig["bounding_box"]["volume_efficiency"]

material_removal_ratio = 1 - volume_efficiency

cavity_index = material_removal_ratio * curvature_ratio

# ==========================================
# 3️⃣ Structural Signals
# ==========================================

min_dim = min(bbox)
max_dim = max(bbox)

slenderness_index = max_dim / min_dim if min_dim else 0

thinness_risk_score = 1 - (min_dim / max_dim) if max_dim else 0

stress_concentration_proxy = (
    sig["feature_metrics"]["feature_density"] *
    curvature_ratio *
    slenderness_index
)

section_instability_index = thinness_risk_score * slenderness_index

# ==========================================
# 4️⃣ Hole Intelligence
# ==========================================

cylinders = [f for f in faces if f.get("type") == "cylinder"]

diameters = []
axes = []

for c in cylinders:
    r = c.get("radius")
    if r:
        diameters.append(round(2 * r, 3))
    if "axis" in c:
        axes.append(tuple(c["axis"]))

diameter_distribution = Counter(diameters)
axis_distribution = Counter(axes)

unique_diameter_count = len(diameter_distribution)
hole_density = len(cylinders) / volume if volume else 0

large_bore_presence = any(d > 20 for d in diameters)

multi_axis_drilling_index = len(axis_distribution)

# ==========================================
# 5️⃣ Manufacturing Geometry Signals
# ==========================================

dominant_axis_ratio = sig["axis_distribution"]["dominant_axis_ratio"]
axis_count = sig["axis_distribution"]["axis_count"]

axis_accessibility_score = dominant_axis_ratio

multi_axis_difficulty_index = 1 - dominant_axis_ratio

overhang_risk = curvature_ratio * thinness_risk_score

developability_index = plane_area / total_surface_area if total_surface_area else 0

undercut_proxy = multi_axis_difficulty_index * curvature_ratio

draft_feasibility_score = developability_index * (1 - curvature_ratio)

# ==========================================
# 6️⃣ Symmetry Intelligence
# ==========================================

rotational_symmetry_likelihood = dominant_axis_ratio * curvature_ratio
prismatic_symmetry_likelihood = developability_index * (1 - curvature_ratio)

# ==========================================
# Final Intelligence Object
# ==========================================

intelligence = {
    "surface_metrics": {
        "total_surface_area": round(total_surface_area, 4),
        "surface_to_volume_ratio": round(surface_to_volume_ratio, 6),
        "compactness_index": round(compactness_index, 6),
        "curvature_ratio": round(curvature_ratio, 4)
    },
    "cavity_metrics": {
        "volume_efficiency": round(volume_efficiency, 4),
        "material_removal_ratio": round(material_removal_ratio, 4),
        "cavity_index": round(cavity_index, 4)
    },
    "structural_signals": {
        "slenderness_index": round(slenderness_index, 4),
        "thinness_risk_score": round(thinness_risk_score, 4),
        "stress_concentration_proxy": round(stress_concentration_proxy, 6),
        "section_instability_index": round(section_instability_index, 6)
    },
    "hole_intelligence": {
        "total_cylindrical_features": len(cylinders),
        "unique_diameter_count": unique_diameter_count,
        "diameter_distribution": dict(diameter_distribution),
        "multi_axis_drilling_index": multi_axis_drilling_index,
        "large_bore_presence": large_bore_presence,
        "hole_density": round(hole_density, 8)
    },
    "manufacturing_geometry_signals": {
        "axis_accessibility_score": round(axis_accessibility_score, 4),
        "multi_axis_difficulty_index": round(multi_axis_difficulty_index, 4),
        "overhang_risk": round(overhang_risk, 4),
        "undercut_proxy": round(undercut_proxy, 4),
        "draft_feasibility_score": round(draft_feasibility_score, 4),
        "developability_index": round(developability_index, 4)
    },
    "symmetry_metrics": {
        "rotational_symmetry_likelihood": round(rotational_symmetry_likelihood, 4),
        "prismatic_symmetry_likelihood": round(prismatic_symmetry_likelihood, 4)
    }
}

with open("geometry_intelligence_v3.json", "w") as f:
    json.dump(intelligence, f, indent=4)

print(json.dumps(intelligence, indent=4))
print("✅ geometry_intelligence_v3.json saved.")