import json
import math

# =========================================================
# Load Inputs
# =========================================================

with open("structural_requirements.json") as f:
    structural = json.load(f)

with open("geometry_intelligence_v3.json") as f:
    geometry = json.load(f)

with open("material.json") as f:
    materials = json.load(f)

required_yield = structural["required_yield_strength_MPa"]
structural_demand = structural["structural_demand_index"]

stress_concentration = geometry["structural_signals"]["stress_concentration_proxy"]

# =========================================================
# Utility
# =========================================================

def clamp01(x):
    return max(0.0, min(1.0, x))

# =========================================================
# Estimate stress amplitude
# =========================================================

stress_amplitude = required_yield * structural_demand
stress_amplitude *= (1 + stress_concentration)

# Safety lower bound
stress_amplitude = max(stress_amplitude, 1e-6)

# =========================================================
# Fatigue Analysis
# =========================================================

results = []

for m in materials:

    mech = m.get("mechanical", {})

    fatigue_limit = mech.get("fatigue_strength_MPa")

    # Fallback if fatigue not provided
    if fatigue_limit is None:
        uts = mech.get("ultimate_tensile_strength_MPa")
        if uts:
            fatigue_limit = 0.4 * uts  # common engineering estimate
        else:
            continue

    margin_ratio = fatigue_limit / stress_amplitude

    # Smooth scoring curve
    fatigue_score = clamp01(math.tanh(margin_ratio / 6))

    results.append({
        "material": m["name"],
        "fatigue_margin_ratio": round(margin_ratio, 4),
        "fatigue_score": round(fatigue_score, 4)
    })

# Sort by fatigue performance
results.sort(key=lambda x: x["fatigue_score"], reverse=True)

output = {
    "fatigue_analysis": results
}

with open("fatigue_analysis.json", "w") as f:
    json.dump(output, f, indent=4)

print(json.dumps(output, indent=4))
print("✅ fatigue_analysis.json saved.")