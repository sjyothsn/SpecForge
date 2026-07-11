from __future__ import annotations

from collections import defaultdict
from typing import Dict, List

from ..models import Entity, KnowledgeGraph, Relationship


class KnowledgeGraphTool:
    """Builds an agent-friendly knowledge graph from entities and relationships."""

    def build(self, entities: List[Entity], relationships: List[Relationship]) -> KnowledgeGraph:
        adjacency: Dict[str, List[Dict[str, str]]] = defaultdict(list)

        for rel in relationships:
            adjacency[rel.source].append(
                {
                    "target": rel.target,
                    "relation": rel.relation_type,
                    "evidence": rel.evidence,
                }
            )

        return KnowledgeGraph(
            nodes=entities,
            edges=relationships,
            adjacency=dict(adjacency),
        )
