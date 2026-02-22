import subprocess
import json
import os
import time
import sys

# =========================================================
# Utility
# =========================================================

def run(script):
    print(f"\n🔄 Running {script} ...")
    result = subprocess.run(["python", script])
    if result.returncode != 0:
        print(f"❌ {script} failed.")
        sys.exit(1)
    print(f"✅ {script} completed.")

def load_json(path):
    if not os.path.exists(path):
        print(f"❌ Required file missing: {path}")
        sys.exit(1)
    with open(path) as f:
        return json.load(f)

# =========================================================
# Main Pipeline
# =========================================================

def main():

    start_time = time.time()

    print("\n🚀 Starting Full Engineering Intelligence Pipeline")

    # -----------------------------------------------------
    # 1️⃣ STEP → Geometry Extraction
    # -----------------------------------------------------
    run("geometry_extractor.py")
    run("geometry_signature.py")
    run("geometry_intelligence_v3.py")

    # -----------------------------------------------------
    # 2️⃣ Classification
    # -----------------------------------------------------
    run("advanced_part_classifier_v4.py")

    # -----------------------------------------------------
    # 3️⃣ Structural
    # -----------------------------------------------------
    run("structural_inference_engine_v3.py")

    # -----------------------------------------------------
    # 4️⃣ Fatigue
    # -----------------------------------------------------
    run("fatigue_intelligence_v3.py")

    # -----------------------------------------------------
    # 5️⃣ Precision
    # -----------------------------------------------------
    run("precision_intelligence.py")

    # -----------------------------------------------------
    # 6️⃣ Manufacturing
    # -----------------------------------------------------
    run("industrial_manufacturing_engine_v6.py")

    # -----------------------------------------------------
    # 7️⃣ Material Inference
    # -----------------------------------------------------
    run("inference_material.py")

    # =====================================================
    # Consolidation
    # =====================================================

    print("\n📊 Consolidating Results...")

    final_report = {
        "metadata": {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pipeline_version": "v5",
            "execution_time_seconds": round(time.time() - start_time, 2)
        },
        "geometry_intelligence": load_json("geometry_intelligence_v3.json"),
        "classification": load_json("advanced_part_classifier_v4.json"),
        "structural_requirements": load_json("structural_requirements.json"),
        "fatigue_analysis": load_json("fatigue_analysis.json"),
        "precision_analysis": load_json("precision_analysis.json"),
        "manufacturing_analysis": load_json("industrial_manufacturing_analysis_v6.json"),
        "material_recommendations": load_json("material_recommendations.json")
            if os.path.exists("material_recommendations.json")
            else None
    }

    with open("final_design_report_v5.json", "w") as f:
        json.dump(final_report, f, indent=4)

    print("🏁 final_design_report_v5.json generated successfully.")
    print(f"⏱ Total Execution Time: {round(time.time() - start_time, 2)} seconds")

if __name__ == "__main__":
    main()