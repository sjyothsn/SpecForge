"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const vscode = require("vscode");
const path = require("path");
class SpecInsightViewProvider {
    constructor(extensionUri) {
        this.extensionUri = extensionUri;
    }
    resolveWebviewView(webviewView) {
        webviewView.webview.options = {
            enableScripts: true,
            localResourceRoots: [this.extensionUri],
        };
        webviewView.webview.html = this.getHtml(webviewView.webview);
        webviewView.webview.onDidReceiveMessage(async (message) => {
            if (message.type === "run") {
                await runSpecInsight(message.inputPath, message.outputPath);
            }
            if (message.type === "openReport") {
                await openLatestReport(message.outputPath);
            }
        });
    }
    getHtml(webview) {
        const nonce = getNonce();
        return `<!doctype html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <style>
    body { font-family: var(--vscode-font-family); padding: 12px; }
    .row { display: flex; flex-direction: column; gap: 6px; margin-bottom: 12px; }
    input { width: 100%; box-sizing: border-box; padding: 8px; border: 1px solid var(--vscode-input-border); background: var(--vscode-input-background); color: var(--vscode-input-foreground); }
    button { width: 100%; padding: 8px; border: 0; cursor: pointer; }
    #runBtn { background: var(--vscode-button-background); color: var(--vscode-button-foreground); }
    #reportBtn { background: var(--vscode-button-secondaryBackground); color: var(--vscode-button-secondaryForeground); margin-top: 8px; }
    small { opacity: 0.8; }
  </style>
</head>
<body>
  <div class="row">
    <label for="inputPath">Input file or folder</label>
    <input id="inputPath" value="examples" />
  </div>
  <div class="row">
    <label for="outputPath">Output folder</label>
    <input id="outputPath" value="outputs" />
  </div>
  <button id="runBtn">Run SpecInsight</button>
  <button id="reportBtn">Open Latest Report</button>
  <p><small>Use paths relative to workspace root.</small></p>
  <script nonce="${nonce}">
    const vscode = acquireVsCodeApi();
    const inputPath = document.getElementById('inputPath');
    const outputPath = document.getElementById('outputPath');
    document.getElementById('runBtn').addEventListener('click', () => {
      vscode.postMessage({ type: 'run', inputPath: inputPath.value, outputPath: outputPath.value });
    });
    document.getElementById('reportBtn').addEventListener('click', () => {
      vscode.postMessage({ type: 'openReport', outputPath: outputPath.value });
    });
  </script>
</body>
</html>`;
    }
}
SpecInsightViewProvider.viewType = "specinsight.panel";
function activate(context) {
    const provider = new SpecInsightViewProvider(context.extensionUri);
    context.subscriptions.push(vscode.window.registerWebviewViewProvider(SpecInsightViewProvider.viewType, provider));
    context.subscriptions.push(vscode.commands.registerCommand("specinsight.run", async () => {
        await runSpecInsight("examples", "outputs");
    }));
    context.subscriptions.push(vscode.commands.registerCommand("specinsight.openLatestReport", async () => {
        await openLatestReport("outputs");
    }));
}
function deactivate() {
    // no-op
}
async function runSpecInsight(inputPathText, outputPathText) {
    const workspace = vscode.workspace.workspaceFolders?.[0];
    if (!workspace) {
        void vscode.window.showErrorMessage("Open a workspace folder before running SpecInsight.");
        return;
    }
    const workspaceFsPath = workspace.uri.fsPath;
    const inputPath = path.join(workspaceFsPath, inputPathText || "examples");
    const outputPath = path.join(workspaceFsPath, outputPathText || "outputs");
    const pythonPath = vscode.workspace.getConfiguration().get("specinsight.pythonPath", "python");
    const mode = vscode.workspace.getConfiguration().get("specinsight.pyPathMode", "env");
    const terminal = vscode.window.createTerminal({ name: "SpecInsight" });
    terminal.show(true);
    const command = mode === "env"
        ? `$env:PYTHONPATH = \"src\"; ${pythonPath} -m specinsight.cli --input \"${inputPath}\" --output \"${outputPath}\"`
        : `${pythonPath} -m specinsight.cli --input \"${inputPath}\" --output \"${outputPath}\"`;
    terminal.sendText(`Set-Location \"${workspaceFsPath}\"`);
    terminal.sendText(command);
    void vscode.window.showInformationMessage("SpecInsight run started in terminal: SpecInsight");
}
async function openLatestReport(outputPathText) {
    const workspace = vscode.workspace.workspaceFolders?.[0];
    if (!workspace) {
        void vscode.window.showErrorMessage("Open a workspace folder before opening reports.");
        return;
    }
    const outputRoot = path.join(workspace.uri.fsPath, outputPathText || "outputs");
    const files = await vscode.workspace.findFiles(new vscode.RelativePattern(outputRoot, "**/report.html"), "**/node_modules/**", 1);
    if (files.length === 0) {
        void vscode.window.showWarningMessage("No report.html found yet. Run SpecInsight first.");
        return;
    }
    await vscode.env.openExternal(files[0]);
}
function getNonce() {
    let text = "";
    const possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    for (let i = 0; i < 32; i += 1) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
//# sourceMappingURL=extension.js.map