from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from .agent import SpecInsightAgent

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def _collect_inputs(path: Path) -> List[Path]:
    if path.is_file():
        return [path]

    if not path.exists():
        raise FileNotFoundError(f"Input path does not exist: {path}")

    files = [
        file
        for file in path.rglob("*")
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    ]
    return sorted(files)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="SpecInsight AI: Convert hardware specs to structured outputs."
    )
    parser.add_argument("--input", required=True, help="Input file or directory")
    parser.add_argument("--output", required=True, help="Output directory")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_root = Path(args.output)

    files = _collect_inputs(input_path)
    if not files:
        raise RuntimeError("No supported input files found. Use PDF, DOCX, or TXT.")

    agent = SpecInsightAgent()
    summary = []

    for file in files:
        per_doc_output = output_root / file.stem
        result = agent.process_document(file, per_doc_output)
        summary.append(result)
        print(f"Processed: {file} -> {per_doc_output}")

    summary_path = output_root / "run_summary.json"
    output_root.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(f"Run summary: {summary_path}")


if __name__ == "__main__":
    main()
