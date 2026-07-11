from __future__ import annotations

from pathlib import Path
from typing import Dict, Any

from .tools.parser_tool import ParserTool
from .tools.normalization_tool import NormalizationTool
from .tools.extraction_tool import ExtractionTool
from .tools.relationship_tool import RelationshipDiscoveryTool
from .tools.graph_tool import KnowledgeGraphTool
from .tools.validation_tool import ValidationTool
from .tools.diagram_tool import DiagramTool
from .tools.report_tool import ReportTool


class SpecInsightAgent:
    """Single orchestrator agent that converts specs into structured outputs."""

    def __init__(self) -> None:
        self.parser = ParserTool()
        self.normalizer = NormalizationTool()
        self.extractor = ExtractionTool()
        self.relationships = RelationshipDiscoveryTool()
        self.graph_builder = KnowledgeGraphTool()
        self.validator = ValidationTool()
        self.diagram = DiagramTool()
        self.report = ReportTool()

    def process_document(self, input_path: Path, output_dir: Path) -> Dict[str, Any]:
        parsed = self.parser.parse(input_path)
        normalized = self.normalizer.normalize(parsed["text"])
        entities = self.extractor.extract_entities(normalized["sections"])
        rels = self.relationships.discover(normalized["sections"], entities)
        graph = self.graph_builder.build(entities, rels)
        issues = self.validator.validate(normalized["sections"], entities, rels)

        diagrams = {
            "architecture": self.diagram.architecture(entities, rels),
            "data_flow": self.diagram.data_flow(entities, rels),
            "dependency": self.diagram.dependency_graph(entities, rels),
        }

        output_dir.mkdir(parents=True, exist_ok=True)
        artifacts = self.report.write_all(
            doc_name=input_path.stem,
            output_dir=output_dir,
            sections=normalized["sections"],
            entities=entities,
            relationships=rels,
            graph=graph,
            issues=issues,
            diagrams=diagrams,
        )

        return {
            "input": str(input_path),
            "output": str(output_dir),
            "artifact_paths": artifacts,
            "entity_count": len(entities),
            "relationship_count": len(rels),
            "validation_issues": len(issues),
        }
