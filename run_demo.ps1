#!/usr/bin/env powershell

# SpecInsight Demo Runner
# Processes dev and eval specs, computes evaluation metrics, and generates a summary report.

param(
    [string]$PythonPath = "python",
    [string]$PyPathMode = "env"
)

$ErrorActionPreference = "Stop"
$rootDir = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $rootDir

Write-Host "====================================="
Write-Host "SpecInsight AI Demo Runner"
Write-Host "====================================="
Write-Host ""

Write-Host "Step 1: Process Development Specs..."
if ($PyPathMode -eq "env") {
    $env:PYTHONPATH = "src"
    & $PythonPath -m specinsight.cli --input "examples\dev_set" --output "outputs\dev"
}
else {
    & $PythonPath -m specinsight.cli --input "examples\dev_set" --output "outputs\dev"
}
Write-Host "✓ Dev specs processed" -ForegroundColor Green
Write-Host ""

Write-Host "Step 2: Process Evaluation Specs..."
if ($PyPathMode -eq "env") {
    $env:PYTHONPATH = "src"
    & $PythonPath -m specinsight.cli --input "examples\eval_set" --output "outputs\eval"
}
else {
    & $PythonPath -m specinsight.cli --input "examples\eval_set" --output "outputs\eval"
}
Write-Host "✓ Eval specs processed" -ForegroundColor Green
Write-Host ""

Write-Host "Step 3: Evaluating Dev Set Quality..."
if ($PyPathMode -eq "env") {
    $env:PYTHONPATH = "src"
    & $PythonPath -m specinsight.evaluator `
        --output "outputs\dev" `
        --docs "memory_controller_spec" "pcie_root_complex_spec"
}
else {
    & $PythonPath -m specinsight.evaluator `
        --output "outputs\dev" `
        --docs "memory_controller_spec" "pcie_root_complex_spec"
}
Write-Host "✓ Dev evaluation complete" -ForegroundColor Green
Write-Host ""

Write-Host "Step 4: Evaluating Eval Set Quality..."
if ($PyPathMode -eq "env") {
    $env:PYTHONPATH = "src"
    & $PythonPath -m specinsight.evaluator `
        --output "outputs\eval" `
        --docs "gpu_specification" "soc_specification"
}
else {
    & $PythonPath -m specinsight.evaluator `
        --output "outputs\eval" `
        --docs "gpu_specification" "soc_specification"
}
Write-Host "✓ Eval evaluation complete" -ForegroundColor Green
Write-Host ""

Write-Host "====================================="
Write-Host "Demo Complete!"
Write-Host "====================================="
Write-Host ""
Write-Host "Outputs:"
Write-Host "  Dev Results:  outputs\dev\evaluation_report.json"
Write-Host "  Eval Results: outputs\eval\evaluation_report.json"
Write-Host ""
Write-Host "Next Steps:"
Write-Host "  1. Open VS Code and view outputs\dev and outputs\eval"
Write-Host "  2. View any report.html for interactive demos"
Write-Host "  3. Open vscode-plugin and press F5 to launch plugin UI"
Write-Host ""
