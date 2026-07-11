from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Section:
    title: str
    level: int
    content: str


@dataclass
class Entity:
    entity_id: str
    name: str
    entity_type: str
    description: str
    source_section: Optional[str] = None


@dataclass
class Relationship:
    source: str
    target: str
    relation_type: str
    evidence: str


@dataclass
class ValidationIssue:
    severity: str
    message: str
    context: Optional[str] = None


@dataclass
class KnowledgeGraph:
    nodes: List[Entity] = field(default_factory=list)
    edges: List[Relationship] = field(default_factory=list)
    adjacency: Dict[str, List[Dict[str, str]]] = field(default_factory=dict)
