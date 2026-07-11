from __future__ import annotations

from collections import Counter
from typing import List

from ..models import Entity, Relationship, Section, ValidationIssue


class ValidationTool:
    """Performs basic completeness and consistency checks."""

    def validate(
        self,
        sections: List[Section],
        entities: List[Entity],
        relationships: List[Relationship],
    ) -> List[ValidationIssue]:
        issues: List[ValidationIssue] = []

        if not sections:
            issues.append(
                ValidationIssue(
                    severity="error",
                    message="No sections were detected after normalization.",
                )
            )

        if not entities:
            issues.append(
                ValidationIssue(
                    severity="error",
                    message="No hardware entities were extracted.",
                )
            )

        type_counter = Counter(entity.entity_type for entity in entities)
        for expected in ["component", "interface", "register"]:
            if type_counter.get(expected, 0) == 0:
                issues.append(
                    ValidationIssue(
                        severity="warning",
                        message=f"No entities extracted for expected type: {expected}",
                    )
                )

        name_counter = Counter(e.name.lower() for e in entities)
        for name, count in name_counter.items():
            if count > 1:
                issues.append(
                    ValidationIssue(
                        severity="warning",
                        message=f"Potential duplicate entity name: {name}",
                        context=f"occurrences={count}",
                    )
                )

        known_names = {entity.name for entity in entities}
        for rel in relationships:
            if rel.source not in known_names or rel.target not in known_names:
                issues.append(
                    ValidationIssue(
                        severity="error",
                        message="Relationship references unknown entity.",
                        context=f"{rel.source} -> {rel.target}",
                    )
                )

        if not relationships and len(entities) > 3:
            issues.append(
                ValidationIssue(
                    severity="warning",
                    message="No relationships discovered despite multiple entities.",
                )
            )

        return issues
