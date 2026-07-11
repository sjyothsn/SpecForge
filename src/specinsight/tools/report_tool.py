from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

from ..models import Entity, KnowledgeGraph, Relationship, Section, ValidationIssue


class ReportTool:
    """Writes markdown, mermaid, json, and html artifacts."""

    def write_all(
        self,
        doc_name: str,
        output_dir: Path,
        sections: List[Section],
        entities: List[Entity],
        relationships: List[Relationship],
        graph: KnowledgeGraph,
        issues: List[ValidationIssue],
        diagrams: Dict[str, str],
    ) -> Dict[str, str]:
        paths: Dict[str, str] = {}

        markdown_text = self._build_markdown(doc_name, sections, entities, relationships, issues)

        structured_md = output_dir / "structured.md"
        structured_md.write_text(markdown_text, encoding="utf-8")
        paths["structured_markdown"] = str(structured_md)

        arch = output_dir / "architecture.mmd"
        arch.write_text(diagrams["architecture"], encoding="utf-8")
        paths["architecture_mermaid"] = str(arch)

        data_flow = output_dir / "data_flow.mmd"
        data_flow.write_text(diagrams["data_flow"], encoding="utf-8")
        paths["data_flow_mermaid"] = str(data_flow)

        dep = output_dir / "dependency_graph.mmd"
        dep.write_text(diagrams["dependency"], encoding="utf-8")
        paths["dependency_mermaid"] = str(dep)

        entities_json = output_dir / "entities.json"
        entities_json.write_text(
            json.dumps([asdict(entity) for entity in entities], indent=2), encoding="utf-8"
        )
        paths["entities_json"] = str(entities_json)

        relationships_json = output_dir / "relationships.json"
        relationships_json.write_text(
            json.dumps([asdict(relationship) for relationship in relationships], indent=2),
            encoding="utf-8",
        )
        paths["relationships_json"] = str(relationships_json)

        graph_json = output_dir / "knowledge_graph.json"
        graph_json.write_text(json.dumps(asdict(graph), indent=2), encoding="utf-8")
        paths["knowledge_graph_json"] = str(graph_json)

        validation_json = output_dir / "validation.json"
        validation_json.write_text(
            json.dumps([asdict(issue) for issue in issues], indent=2), encoding="utf-8"
        )
        paths["validation_json"] = str(validation_json)

        report_html = output_dir / "report.html"
        report_html.write_text(self._build_html(doc_name, markdown_text, diagrams), encoding="utf-8")
        paths["html_report"] = str(report_html)

        return paths

    def _build_markdown(
        self,
        doc_name: str,
        sections: List[Section],
        entities: List[Entity],
        relationships: List[Relationship],
        issues: List[ValidationIssue],
    ) -> str:
        lines: List[str] = [f"# Structured Specification: {doc_name}", ""]

        lines.extend(["## Hierarchical Sections", ""])
        for section in sections:
            prefix = "#" * min(section.level + 2, 6)
            lines.extend([f"{prefix} {section.title}", "", section.content, ""])

        lines.extend(["## Extracted Entities", ""])
        lines.append("| ID | Type | Name | Source Section |")
        lines.append("|---|---|---|---|")
        for entity in entities:
            lines.append(
                f"| {entity.entity_id} | {entity.entity_type} | {entity.name} | {entity.source_section or '-'} |"
            )
        lines.append("")

        lines.extend(["## Relationships", ""])
        lines.append("| Source | Relation | Target | Evidence |")
        lines.append("|---|---|---|---|")
        for rel in relationships:
            evidence = rel.evidence.replace("|", "\\|")
            lines.append(f"| {rel.source} | {rel.relation_type} | {rel.target} | {evidence} |")
        lines.append("")

        lines.extend(["## Validation Findings", ""])
        if issues:
            for issue in issues:
                context = f" ({issue.context})" if issue.context else ""
                lines.append(f"- [{issue.severity}] {issue.message}{context}")
        else:
            lines.append("- No validation issues detected.")
        lines.append("")

        return "\n".join(lines)

    @staticmethod
    def _build_html(doc_name: str, markdown_text: str, diagrams: Dict[str, str]) -> str:
        try:
            import markdown  # type: ignore

            rendered_markdown = markdown.markdown(
                markdown_text,
                extensions=["tables", "fenced_code"],
            )
        except ImportError:
            rendered_markdown = f"<pre>{markdown_text}</pre>"

        return f"""<!doctype html>
<html>
<head>
  <meta charset=\"utf-8\" />
  <title>SpecInsight Report - {doc_name}</title>
  <style>
    body {{ font-family: Segoe UI, sans-serif; margin: 2rem; line-height: 1.45; }}
    pre {{ background: #f4f4f4; padding: 1rem; overflow: auto; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background-color: #f2f2f2; }}
    h1, h2 {{ color: #0d3b66; }}
  </style>
</head>
<body>
  <h1>SpecInsight Report: {doc_name}</h1>
  {rendered_markdown}
  <h2>Architecture Diagram (Mermaid)</h2>
  <pre>{diagrams['architecture']}</pre>
  <h2>Data Flow Diagram (Mermaid)</h2>
  <pre>{diagrams['data_flow']}</pre>
  <h2>Dependency Graph (Mermaid)</h2>
  <pre>{diagrams['dependency']}</pre>
</body>
</html>
"""
