from __future__ import annotations

import re
from typing import Dict, List

from ..models import Section


class NormalizationTool:
    """Normalizes text and preserves a lightweight section hierarchy."""

    HEADING_PATTERNS = [
        re.compile(r"^\d+(?:\.\d+)*\s+.+"),
        re.compile(r"^[A-Z][A-Z\s0-9\-_/]{3,}$"),
        re.compile(r"^[A-Za-z].*:$"),
    ]

    def normalize(self, raw_text: str) -> Dict[str, List[Section]]:
        cleaned = self._clean_text(raw_text)
        sections = self._to_sections(cleaned)
        return {"sections": sections}

    @staticmethod
    def _clean_text(text: str) -> str:
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = re.sub(r"[ \t]+", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _to_sections(self, text: str) -> List[Section]:
        lines = [line.strip() for line in text.split("\n")]
        sections: List[Section] = []

        current_title = "Document Overview"
        current_level = 1
        buffer: List[str] = []

        def flush() -> None:
            nonlocal buffer, current_title, current_level
            content = "\n".join(buffer).strip()
            if content:
                sections.append(
                    Section(title=current_title, level=current_level, content=content)
                )
            buffer = []

        for line in lines:
            if not line:
                continue
            if self._is_heading(line):
                flush()
                current_title = line.rstrip(":")
                current_level = self._infer_level(line)
            else:
                buffer.append(line)

        flush()
        if not sections and text:
            sections.append(Section(title="Document Overview", level=1, content=text))

        return sections

    def _is_heading(self, line: str) -> bool:
        return any(pattern.match(line) for pattern in self.HEADING_PATTERNS)

    @staticmethod
    def _infer_level(line: str) -> int:
        numeric_match = re.match(r"^(\d+(?:\.\d+)*)\s+", line)
        if numeric_match:
            return numeric_match.group(1).count(".") + 1
        return 1
