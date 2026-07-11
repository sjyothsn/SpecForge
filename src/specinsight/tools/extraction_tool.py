from __future__ import annotations

import re
from typing import Dict, List, Set

from ..models import Entity, Section


class ExtractionTool:
    """Extracts hardware entities from normalized sections using heuristics."""

    ENTITY_PATTERNS: Dict[str, List[re.Pattern[str]]] = {
        "component": [
            re.compile(r"(?:component|module|block)\s*[:\-]\s*([A-Za-z0-9_\-/ ]+)", re.IGNORECASE),
            re.compile(r"\b([A-Z][A-Za-z0-9_]{2,})\s+(?:block|module)\b"),
        ],
        "interface": [
            re.compile(r"(?:interface|bus|protocol)\s*[:\-]\s*([A-Za-z0-9_\-/ ]+)", re.IGNORECASE),
            re.compile(r"\b(AXI|APB|I2C|SPI|UART|PCIe|CXL|JTAG|GPIO)\b", re.IGNORECASE),
        ],
        "register": [
            re.compile(r"\b([A-Z][A-Z0-9_]*_(?:REG|CSR))\b"),
            re.compile(r"(?:register)\s*[:\-]\s*([A-Za-z0-9_]+)", re.IGNORECASE),
        ],
        "signal": [
            re.compile(r"(?:signal)\s*[:\-]\s*([A-Za-z0-9_]+)", re.IGNORECASE),
            re.compile(r"\b([a-z][a-z0-9_]*(?:_in|_out|_n|_clk|_rst))\b"),
        ],
        "state_machine": [
            re.compile(r"(?:state machine|fsm)\s*[:\-]\s*([A-Za-z0-9_\-/ ]+)", re.IGNORECASE),
        ],
        "requirement": [
            re.compile(r"\b(REQ[-_ ]?\d{2,})\b", re.IGNORECASE),
            re.compile(r"\b(shall|must|should)\b", re.IGNORECASE),
        ],
    }

    def extract_entities(self, sections: List[Section]) -> List[Entity]:
        entities: List[Entity] = []
        seen: Set[str] = set()
        counter = 1

        for section in sections:
            text = f"{section.title}\n{section.content}"
            for entity_type, patterns in self.ENTITY_PATTERNS.items():
                for pattern in patterns:
                    for match in pattern.finditer(text):
                        name = self._extract_name(entity_type, match)
                        if not name:
                            continue

                        key = f"{entity_type}:{name.lower()}"
                        if key in seen:
                            continue
                        seen.add(key)

                        entities.append(
                            Entity(
                                entity_id=f"E{counter:04d}",
                                name=name,
                                entity_type=entity_type,
                                description=f"Extracted from section '{section.title}'",
                                source_section=section.title,
                            )
                        )
                        counter += 1

        return entities

    @staticmethod
    def _extract_name(entity_type: str, match: re.Match[str]) -> str:
        if entity_type == "requirement":
            if match.lastindex:
                return match.group(1).strip()
            return "normative_requirement"

        if match.lastindex:
            return match.group(1).strip()
        return match.group(0).strip()
