import json
from google import genai

# ==============================
# CONFIG
# ==============================

API_KEY = "apikey"
MODEL_NAME = "gemini-2.5-flash"

INPUT_PATH = "final_design_report_v5.json"
OUTPUT_PATH = "executive_engineering_report.txt"

# ==============================
# LOAD FINAL REPORT
# ==============================

with open(INPUT_PATH, "r") as f:
    report = json.load(f)

report_json = json.dumps(report, indent=2)

# ==============================
# STRONG SINGLE PROMPT
# ==============================

prompt = f"""
You are a senior mechanical design engineer conducting a formal internal design review.

This is not a summary.
This is a technical design critique and evaluation.

You must:
- Use ONLY the provided structured data.
- Explicitly reference numeric values where relevant.
- Interpret relationships between geometry, structural demand, fatigue, manufacturing, and materials.
- Identify trade-offs.
- Identify contradictions.
- Identify design intent where it can be inferred from metrics.
- Avoid generic language.
- Avoid marketing tone.
- Avoid repeating raw JSON.
- Avoid inventing missing data.
- Avoid claiming FEA or simulation was performed.

Write a professional Executive Engineering Review Report with deep analytical reasoning.

Required Sections:

1. Design Character & Archetype Interpretation
   - Explain what kind of engineering problem this component likely solves.
   - Interpret classification confidence and overlap scores.
   - Infer structural behavior from geometry signals.

2. Structural Logic Evaluation
   - Analyze slenderness, thinness risk, stress concentration proxy together.
   - Evaluate whether structural demand index aligns with geometric robustness.
   - Identify if the design is over-engineered or under-utilized.

3. Fatigue & Material Envelope Analysis
   - Interpret fatigue margin distribution.
   - Explain why metallic materials cluster high.
   - Identify material classes that are structurally incompatible.

4. Manufacturing–Geometry Coupling
   - Critically evaluate why the top-ranked process was selected.
   - Explain the impact of material removal ratio (0.9036).
   - Analyze production volume (500) vs process scaling.
   - Identify whether geometry favors forming, machining, or hybrid strategy.

5. Material–Process Compatibility Discussion
   - Explain why Magnesium AZ31B, Carbon Steel 1018, and Aluminum 6061 rank highest.
   - Evaluate density implications.
   - Discuss precision requirement (0.6963 index) impact on process-material pairing.

6. Engineering Risk Assessment
   - Identify real engineering flags supported by numeric evidence.
   - Discuss cost risk, manufacturing risk, and structural margin risk.

7. Engineering Decision & Next Steps
   - Provide a firm engineering position.
   - State whether the design is mature or concept-level.
   - Recommend next technical validation step.

Minimum length: 900 words.
Maximum length: 1300 words.

This should read like an internal engineering design review memo written by a senior engineer.

Structured Engineering Intelligence Data:
{report_json}
"""

# ==============================
# CALL GEMINI (SIMPLE)
# ==============================

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model=MODEL_NAME,
    contents=prompt
)

report_text = response.text

# ==============================
# SAVE OUTPUT
# ==============================

with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    f.write("EXECUTIVE ENGINEERING REVIEW REPORT\n")
    f.write("=" * 60 + "\n\n")
    f.write(report_text)

print("✅ Executive report generated.")
print(f"📄 Saved to {OUTPUT_PATH}")