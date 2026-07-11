from __future__ import annotations

from pathlib import Path
from typing import Dict


class ParserTool:
    """Parses PDF, DOCX, and TXT into plain text with minimal metadata."""

    def parse(self, input_path: Path) -> Dict[str, str]:
        suffix = input_path.suffix.lower()

        if suffix == ".txt":
            text = input_path.read_text(encoding="utf-8", errors="ignore")
        elif suffix == ".docx":
            text = self._parse_docx(input_path)
        elif suffix == ".pdf":
            text = self._parse_pdf(input_path)
        else:
            raise ValueError(f"Unsupported input format: {suffix}")

        return {
            "text": text,
            "format": suffix.lstrip("."),
            "source": str(input_path),
        }

    @staticmethod
    def _parse_docx(input_path: Path) -> str:
        try:
            from docx import Document  # type: ignore
        except ImportError as exc:
            raise RuntimeError("python-docx is required to parse DOCX files.") from exc

        document = Document(str(input_path))
        paragraphs = [p.text.strip() for p in document.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    @staticmethod
    def _parse_pdf(input_path: Path) -> str:
        try:
            from pypdf import PdfReader  # type: ignore
        except ImportError as exc:
            raise RuntimeError("pypdf is required to parse PDF files.") from exc

        reader = PdfReader(str(input_path))
        pages = []
        for page_index, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            pages.append(f"[Page {page_index}]\n{page_text.strip()}")
        return "\n\n".join(pages)
