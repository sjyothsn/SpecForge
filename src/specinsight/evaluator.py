"""
Evaluation harness for SpecInsight AI agent.

Computes metrics on extracted entities, relationships, and validation quality.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


class SpecEvaluator:
    """Evaluates extracted specs against expected ground truth."""

    def __init__(self, output_dir: Path) -> None:
        self.output_dir = output_dir

    def evaluate_document(self, doc_name: str) -> Dict[str, Any]:
        """Evaluate a single processed document."""
        doc_output = self.output_dir / doc_name
        if not doc_output.exists():
            return {"error": f"Output directory not found: {doc_output}"}

        entities_json = doc_output / "entities.json"
        relationships_json = doc_output / "relationships.json"
        validation_json = doc_output / "validation.json"
        structured_md = doc_output / "structured.md"
        diagrams = {
            "architecture": doc_output / "architecture.mmd",
            "data_flow": doc_output / "data_flow.mmd",
            "dependency": doc_output / "dependency_graph.mmd",
        }

        if not entities_json.exists():
            return {"error": "Artifacts missing"}

        entities = json.loads(entities_json.read_text())
        relationships = json.loads(relationships_json.read_text())
        validation_issues = json.loads(validation_json.read_text()) if validation_json.exists() else []

        entity_type_distribution = self._count_by_type(entities)
        relationship_type_distribution = self._count_by_type(relationships, key="relation_type")

        diagram_validity = {
            name: self._check_diagram_valid(path)
            for name, path in diagrams.items()
        }

        markdown_size = structured_md.stat().st_size if structured_md.exists() else 0
        markdown_sections = self._count_markdown_sections(structured_md) if structured_md.exists() else 0

        return {
            "document": doc_name,
            "metrics": {
                "entity_count": len(entities),
                "entity_type_distribution": entity_type_distribution,
                "relationship_count": len(relationships),
                "relationship_type_distribution": relationship_type_distribution,
                "validation_issues": len(validation_issues),
                "validation_error_count": sum(1 for v in validation_issues if v.get("severity") == "error"),
                "validation_warning_count": sum(1 for v in validation_issues if v.get("severity") == "warning"),
            },
            "artifacts": {
                "markdown_generated": structured_md.exists(),
                "markdown_size_bytes": markdown_size,
                "markdown_section_count": markdown_sections,
                "architecture_diagram_valid": diagram_validity.get("architecture", False),
                "data_flow_diagram_valid": diagram_validity.get("data_flow", False),
                "dependency_diagram_valid": diagram_validity.get("dependency", False),
            },
            "quality_score": self._compute_quality_score(
                len(entities),
                len(relationships),
                len(validation_issues),
                diagram_validity,
            ),
        }

    def evaluate_batch(self, doc_names: List[str]) -> Dict[str, Any]:
        """Evaluate multiple documents and produce summary."""
        results = []
        for doc_name in doc_names:
            result = self.evaluate_document(doc_name)
            results.append(result)

        total_entities = sum(r["metrics"]["entity_count"] for r in results if "metrics" in r)
        total_relationships = sum(r["metrics"]["relationship_count"] for r in results if "metrics" in r)
        total_issues = sum(r["metrics"]["validation_issues"] for r in results if "metrics" in r)
        avg_quality = sum(r.get("quality_score", 0) for r in results) / len(results) if results else 0

        return {
            "documents": results,
            "summary": {
                "total_documents": len(results),
                "total_entities": total_entities,
                "total_relationships": total_relationships,
                "total_validation_issues": total_issues,
                "average_quality_score": round(avg_quality, 2),
                "success_rate": f"{sum(1 for r in results if 'metrics' in r) / len(results) * 100:.1f}%",
            },
        }

    @staticmethod
    def _count_by_type(items: List[Dict[str, Any]], key: str = "entity_type") -> Dict[str, int]:
        """Count items by their type field."""
        counts: Dict[str, int] = {}
        for item in items:
            t = item.get(key, "unknown")
            counts[t] = counts.get(t, 0) + 1
        return counts

    @staticmethod
    def _check_diagram_valid(path: Path) -> bool:
        """Check if a Mermaid diagram file is non-empty and well-formed."""
        if not path.exists():
            return False
        content = path.read_text()
        return len(content) > 10 and ("graph" in content or "flowchart" in content)

    @staticmethod
    def _count_markdown_sections(path: Path) -> int:
        """Count markdown section headings."""
        if not path.exists():
            return 0
        content = path.read_text(encoding="utf-8", errors="ignore")
        return content.count("##")

    @staticmethod
    def _compute_quality_score(
        entity_count: int,
        relationship_count: int,
        issue_count: int,
        diagram_validity: Dict[str, bool],
    ) -> float:
        """Compute an overall quality score (0-100)."""
        score = 0.0

        if entity_count > 5:
            score += min(25, entity_count)
        else:
            score += entity_count * 5

        if relationship_count > 2:
            score += min(25, relationship_count * 2)
        else:
            score += relationship_count * 12.5

        valid_diagrams = sum(1 for v in diagram_validity.values() if v)
        score += valid_diagrams * 10

        if issue_count == 0:
            score += 15
        elif issue_count < 3:
            score += 10
        else:
            score = max(0, score - issue_count * 2)

        return min(100, max(0, score))


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate SpecInsight output quality.")
    parser.add_argument("--output", required=True, help="Output root directory")
    parser.add_argument("--docs", nargs="+", required=True, help="Document names to evaluate")
    args = parser.parse_args()

    output_dir = Path(args.output)
    evaluator = SpecEvaluator(output_dir)
    results = evaluator.evaluate_batch(args.docs)

    print(json.dumps(results, indent=2))

    eval_report = output_dir / "evaluation_report.json"
    eval_report.write_text(json.dumps(results, indent=2))
    print(f"\nEvaluation report: {eval_report}")


if __name__ == "__main__":
    main()
