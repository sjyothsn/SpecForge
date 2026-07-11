from __future__ import annotations

import re
from typing import Dict, List

from ..models import Entity, Relationship, Section


class RelationshipDiscoveryTool:
    """Identifies relationships between extracted entities from section text."""

    RELATION_KEYWORDS: Dict[str, str] = {
        "depends on": "depends_on",
        "requires": "depends_on",
        "uses": "uses",
        "connected to": "connected_to",
        "communicates with": "communicates_with",
        "writes to": "writes_to",
        "reads from": "reads_from",
        "sends": "flows_to",
        "receives": "flows_from",
    }

    def discover(self, sections: List[Section], entities: List[Entity]) -> List[Relationship]:
        if len(entities) < 2:
            return []

        entity_names = sorted({e.name for e in entities}, key=len, reverse=True)
        relationships: List[Relationship] = []
        seen = set()

        for section in sections:
            sentences = re.split(r"(?<=[.!?])\s+", section.content)
            for sentence in sentences:
                lowered = sentence.lower()
                relation_type = self._relation_from_sentence(lowered)
                if not relation_type:
                    continue

                mentioned = [name for name in entity_names if re.search(rf"\b{re.escape(name)}\b", sentence)]
                if len(mentioned) < 2:
                    continue

                source = mentioned[0]
                target = mentioned[1]
                key = (source.lower(), target.lower(), relation_type)
                if key in seen:
                    continue
                seen.add(key)

                relationships.append(
                    Relationship(
                        source=source,
                        target=target,
                        relation_type=relation_type,
                        evidence=sentence.strip(),
                    )
                )

        return relationships

    def _relation_from_sentence(self, lowered_sentence: str) -> str | None:
        for keyword, rel_type in self.RELATION_KEYWORDS.items():
            if keyword in lowered_sentence:
                return rel_type
        return None
