## SpecInsight VS Code Plugin — Quick Launch Guide

### What You'll See

The plugin adds a **new icon** in VS Code's Activity Bar (left sidebar) that opens a dedicated panel.

```
┌─────────────────────────────────────┐
│ VS Code Window                      │
├──────┬──────────────────────────────┤
│ ⚙️   │   (Settings, Extensions...)  │
│ 🔍   │   (Search)                   │
│ 📄   │   (Explorer)                 │
│ ▶️   │   (Run & Debug)              │
│ 🧪  │   (Testing)                  │
│ 😊   │   (SpecInsight) ← NEW!       │
│      │                              │
│      │ ┌──────────────────────────┐ │
│      │ │ Run SpecInsight          │ │
│      │ │                          │ │
│      │ │ Input: examples          │ │
│      │ │ Output: outputs          │ │
│      │ │                          │ │
│      │ │ [Run SpecInsight]        │ │
│      │ │ [Open Latest Report]     │ │
│      │ └──────────────────────────┘ │
└──────┴──────────────────────────────┘
```

### Launch Steps (Copy-Paste Ready)

#### In PowerShell (Admin or Regular):
```powershell
cd "c:\Users\sjyothsn\OneDrive - Intel Corporation\SpecForge\vscode-plugin"
code .
```

#### Then in VS Code:
1. Press **F5** (or Debug > Start Debugging)
2. Wait for new window to open (~10 seconds)
3. In new window: **File > Open Folder** → select main SpecForge folder
4. Look for **😊 icon** in Activity Bar
5. Click it to open SpecInsight panel

### What the Panel Does

**Input Field:** Path to spec files (e.g., "examples/sample_spec.txt" or "examples/dev_set")  
**Output Field:** Where results are saved (e.g., "outputs")

**Run Button:** 
- Executes: `python -m specinsight.cli --input <path> --output <path>`
- Runs in integrated terminal below
- Processes all specs and generates artifacts

**Open Report Button:**
- Finds the latest `report.html`
- Opens it in your default browser
- Shows rendered markdown + diagrams

### Example Workflow

1. Plugin panel opens with defaults
2. Click "Run SpecInsight" 
3. Terminal shows: `Processed: examples/sample_spec.txt -> outputs/sample_spec`
4. Click "Open Latest Report"
5. Browser opens with: Architecture diagrams, markdown, extracted entities

### Troubleshooting

**Plugin icon not showing?**
- Make sure you're in Extension Development Host window (new window from F5)
- Not in the original VS Code window

**Button doesn't run?**
- Check Python is installed: `python --version`
- Check requirements: `pip install -r requirements.txt`
- Terminal should show errors if something fails

**Report doesn't open?**
- Run SpecInsight first (click Run button)
- Wait for terminal to show "Run summary:"
- Then try Open Report

### One-Command Full Demo

Instead of using the plugin UI, you can run the full demo:

```powershell
cd "c:\Users\sjyothsn\OneDrive - Intel Corporation\SpecForge"
$env:PYTHONPATH = "src"
.\run_demo.ps1
```

This processes all dev + eval specs and generates quality metrics.
