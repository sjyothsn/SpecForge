from __future__ import annotations

from typing import List

from ..models import Entity, Relationship


class DiagramTool:
    """Generates Mermaid diagrams from extracted knowledge."""

    @staticmethod
    def _node_id(name: str) -> str:
        sanitized = "".join(ch if ch.isalnum() else "_" for ch in name)
        if sanitized and sanitized[0].isdigit():
            sanitized = f"N_{sanitized}"
        return sanitized or "UNKNOWN"

    def architecture(self, entities: List[Entity], relationships: List[Relationship]) -> str:
        lines = ["graph TD"]

        components = [e for e in entities if e.entity_type in {"component", "interface"}]
        for entity in components:
            node = self._node_id(entity.name)
            label = f"{entity.name} ({entity.entity_type})"
            lines.append(f'    {node}["{label}"]')

        for rel in relationships:
            if rel.relation_type in {"connected_to", "communicates_with", "uses"}:
                src = self._node_id(rel.source)
                dst = self._node_id(rel.target)
                lines.append(f"    {src} -->|{rel.relation_type}| {dst}")

        return "\n".join(lines)

    def data_flow(self, entities: List[Entity], relationships: List[Relationship]) -> str:
        lines = ["flowchart LR"]

        flow_nodes = [
            e for e in entities if e.entity_type in {"component", "interface", "signal"}
        ]
        for entity in flow_nodes:
            lines.append(f'    {self._node_id(entity.name)}["{entity.name}"]')

        for rel in relationships:
            if rel.relation_type in {"flows_to", "flows_from", "writes_to", "reads_from"}:
                src = self._node_id(rel.source)
                dst = self._node_id(rel.target)
                lines.append(f"    {src} -->|{rel.relation_type}| {dst}")

        return "\n".join(lines)

    def dependency_graph(self, entities: List[Entity], relationships: List[Relationship]) -> str:
        lines = ["graph LR"]

        for entity in entities:
            lines.append(f'    {self._node_id(entity.name)}["{entity.name}"]')

        for rel in relationships:
            if rel.relation_type == "depends_on":
                src = self._node_id(rel.source)
                dst = self._node_id(rel.target)
                lines.append(f"    {src} -->|depends_on| {dst}")

        return "\n".join(lines)
