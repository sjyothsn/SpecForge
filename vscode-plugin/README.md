# SpecInsight VS Code Plugin

This extension adds a dedicated **SpecInsight** tab in the VS Code Activity Bar.

## Features

- Side panel with Run and Open Report actions.
- Runs existing SpecInsight Python CLI from the workspace.
- Opens latest generated HTML report.

## Build and Run (Extension Development Host)

1. Open folder: `vscode-plugin`
2. Install deps:

   ```bash
   npm install
   ```

3. Compile:

   ```bash
   npm run compile
   ```

4. Press `F5` in VS Code to launch Extension Development Host.
5. In the new window, open your SpecForge workspace.
6. Click the **SpecInsight** icon in Activity Bar.

## Notes

- Default command assumes the Python project root contains `src/specinsight`.
- Change settings if needed:
  - `specinsight.pythonPath`
  - `specinsight.pyPathMode`
