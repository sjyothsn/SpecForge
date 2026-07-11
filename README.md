# SpecInsight AI

SpecInsight AI is a **single-agent** system that converts hardware specification documents (PDF, DOCX, TXT) into agent-friendly structured outputs.

## What It Produces

For each input specification, the system generates:

- Structured Markdown
- Mermaid architecture diagram
- Mermaid data flow diagram
- Mermaid dependency graph
- Machine-readable JSON artifacts
- HTML report

## Architecture (Single Orchestrator Agent)

The `SpecInsightAgent` is the central orchestrator. It calls modular tools:

- Parser Tool
- Normalization Tool
- Extraction Tool
- Relationship Discovery Tool
- Knowledge Graph Tool
- Validation Tool
- Diagram Tool
- Report Tool

## Quick Start

### 1. Install Dependencies
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run Full Demo (All Dev + Eval Sets)
```powershell
$env:PYTHONPATH = "src"
.\run_demo.ps1
```

### 3. Process Individual Files or Folders
```bash
$env:PYTHONPATH = "src"
python -m specinsight.cli --input "examples\sample_spec.txt" --output "outputs"
python -m specinsight.cli --input "examples\dev_set" --output "outputs\dev"
```

### 4. Evaluate Quality
```bash
$env:PYTHONPATH = "src"
python -m specinsight.evaluator --output "outputs\dev" --docs "memory_controller_spec" "pcie_root_complex_spec"
```

## Input Formats

- `.pdf`
- `.docx`
- `.txt`

## Output Layout

For each processed document, an output folder is created:

- `structured.md`
- `architecture.mmd`
- `data_flow.mmd`
- `dependency_graph.mmd`
- `entities.json`
- `relationships.json`
- `knowledge_graph.json`
- `validation.json`
- `report.html`

## Notes for Hackathon Demo

- Uses heuristic information extraction (no hardcoded template).
- Preserves source traceability for extracted entities and relationships.
- Robust to varying styles through normalization plus pattern-based extraction.
- Easy to extend with LLM-based extraction later.
