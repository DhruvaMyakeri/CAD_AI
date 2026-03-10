# CAD_AI
### Pre-Analysis Engineering Intelligence for CAD Models

CAD_AI is an experimental **engineering intelligence pipeline** that analyzes CAD geometry and produces structured engineering insights before expensive simulation tools (like FEA) are used.

The system processes **STEP CAD files** and generates:

- Geometry intelligence
- Structural inference
- Fatigue evaluation
- Precision difficulty estimation
- Manufacturing process ranking
- Material recommendations
- Automated engineering review report

The goal is to assist engineers during **early design evaluation**.

---

# Motivation

Engineering design evaluation typically requires:

- CAD modeling
- Export to simulation software
- FEA setup
- Iterative analysis

This process is expensive and time consuming.

CAD_AI introduces a **pre-analysis intelligence layer** that provides quick insights such as:

- What type of part this likely is
- What structural behavior is expected
- Which materials are suitable
- Which manufacturing process is optimal
- Whether fatigue or precision risks exist

The system **does not replace simulation**.  
Instead it helps engineers **detect problems earlier** in the design process.

---

# System Architecture

The system is implemented as a **modular pipeline**.


STEP CAD Model
│
▼
geometry_extractor
│
▼
geometry_signature
│
▼
geometry_intelligence_v3
│
▼
advanced_part_classifier_v4
│
▼
structural_inference_engine_v3
│
▼
fatigue_intelligence_v3
│
▼
precision_intelligence
│
▼
industrial_manufacturing_engine_v6
│
▼
material_inference
│
▼
master_engine_v5
│
▼
LLM Engineering Report


Each stage performs a specific engineering analysis task.

---

# Pipeline Modules

## Geometry Extraction

**File**


geometry_extractor.py


Reads the STEP model and extracts geometric primitives such as:

- Faces
- Cylinders
- Planes
- Bounding box
- Surface area
- Volume

**Output**


geometry.json


---

## Geometry Signature

**File**


geometry_signature.py


Creates normalized geometric descriptors including:

- planar_ratio
- cylindrical_ratio
- aspect_ratio
- volume_efficiency
- axis_distribution

This acts as the **geometric fingerprint** of the part.

---

## Geometry Intelligence

**File**


geometry_intelligence_v3.py


Transforms geometry metrics into engineering signals.

Examples:

- slenderness_index
- thinness_risk_score
- stress_concentration_proxy
- hole_density
- developability_index
- axis_accessibility_score

These metrics capture **manufacturing and structural implications** of the geometry.

---

## Part Archetype Classification

**File**


advanced_part_classifier_v4.py


Determines the likely engineering archetype.

Possible classes:

- rotational_part
- beam_or_frame_member
- plate_like
- thin_shell_or_housing
- bracket_or_prismatic
- feature_dense_component

Classification influences structural and manufacturing inference.

---

## Structural Inference

**File**


structural_inference_engine_v3.py


Predicts structural requirements using heuristic models.

Outputs include:

- required_yield_strength
- required_modulus
- structural_demand_index
- failure_mode_weights

This is a **pre-FEA estimation**, not a replacement for simulation.

---

## Fatigue Intelligence

**File**


fatigue_intelligence_v3.py


Evaluates fatigue margins for materials.

Metrics include:

- fatigue_margin_ratio
- fatigue_score

These values help determine material durability under cyclic loading.

---

## Precision Intelligence

**File**


precision_intelligence.py


Estimates manufacturing precision difficulty based on:

- geometry complexity
- axis distribution
- slenderness
- feature density

Outputs:


precision_difficulty_index
recommended_tolerance_class


---

## Manufacturing Process Intelligence

**File**


industrial_manufacturing_engine_v6.py


Evaluates possible manufacturing processes:

- CNC Milling
- CNC Turning
- Sheet Metal Forming
- Casting
- Additive Manufacturing

Each process is scored using:

- geometry feasibility
- production scaling
- tooling complexity
- structural compatibility
- sustainability

Outputs a ranked manufacturability index.

---

## Material Inference

**File**


inference_material.py


Uses the material database:


material.json


Materials are evaluated using:

- yield strength
- modulus
- fatigue resistance
- density
- machinability
- ductility

Top materials are recommended based on the engineering requirements.

---

## Master Engine

**File**


master_engine_v5.py


This is the **pipeline orchestrator**.

It sequentially runs every module and produces the final structured report:


final_design_report_v5.json


---

## LLM Engineering Explanation

**File**


llm_explanation_v2.py


Generates a detailed **executive engineering report** using structured output from the pipeline.

Output:


executive_engineering_report.txt


---

# Current Status

The current repository implements the **core engineering intelligence engine**.

### Implemented

- Geometry analysis
- Structural inference
- Fatigue evaluation
- Precision estimation
- Manufacturing intelligence
- Material recommendation
- Automated engineering report

### Not yet implemented

- REST API
- Backend service
- Web interface

These will be developed in future versions.

---

# Running the Pipeline

Run the master engine:

```bash
python master_engine_v5.py

The pipeline will:

Analyze the STEP model

Run all engineering inference modules

Generate the final report

Output files will be produced automatically.

Example Outputs

Example outputs include:

geometry.json
geometry_signature.json
geometry_intelligence_v3.json
advanced_part_classifier_v4.json
structural_requirements.json
fatigue_analysis.json
precision_analysis.json
industrial_manufacturing_analysis_v6.json
material_recommendations.json
final_design_report_v5.json
executive_engineering_report.txt
Material Database

The system uses a structured material database:

material.json

Each material contains:

Mechanical properties

Thermal properties

Manufacturing compatibility

Environmental resistance

Economic indicators

This allows multi-criteria material evaluation.

Limitations

CAD_AI is not a replacement for simulation.

The system does not perform:

Finite Element Analysis

Stress tensor computation

Nonlinear deformation modeling

Thermal analysis

Modal analysis

Instead it provides engineering design intelligence before simulation.

Future Development

Planned improvements include:

FastAPI backend

Web interface for model upload

Interactive engineering dashboard

Integration with simulation tools

Design optimization suggestions

Real-time CAD feedback

Technologies Used

Python

Structured engineering heuristics

CAD geometry processing

Large Language Models for report generation

Repository Structure
CAD_AI
│
├── advanced_part_classifier_v4.py
├── fatigue_intelligence_v3.py
├── geometry_extractor.py
├── geometry_signature.py
├── geometry_intelligence_v3.py
├── industrial_manufacturing_engine_v6.py
├── inference_material.py
├── precision_intelligence.py
├── structural_inference_engine_v3.py
│
├── master_engine_v5.py
├── llm_explanation_v2.py
│
├── material.json
├── part.STEP
│
├── backend
├── frontend
License

This project is experimental and intended for research and educational purposes.

Author

Dhruva M
Computer Science Engineering Student

Focus areas:

AI systems

Engineering intelligence

CAD analysis

Simulation support tools
