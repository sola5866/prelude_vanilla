"""Artifact zip readability validation for build outputs."""

from __future__ import annotations

from pathlib import Path
from zipfile import BadZipFile, ZipFile

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus


class ArtifactIsZipReadableRule:
    """Validate that the built mcpack artifact is a readable zip archive."""

    rule_id = "artifact_is_zip_readable"
    category = "build"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """Check whether the artifact can be opened as a zip archive."""

        artifact_path = get_artifact_path(context)
        try:
            with ZipFile(artifact_path, "r") as archive:
                archive.infolist()
        except (BadZipFile, OSError):
            return [
                RuleResult(
                    rule_id=self.rule_id,
                    category=self.category,
                    status=ValidationStatus.FAILED,
                    target=str(artifact_path),
                    message=format_invalid_zip_message(artifact_path),
                )
            ]

        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.PASSED,
                target=str(artifact_path),
                message=None,
            )
        ]


def get_artifact_path(context: ValidationContext) -> Path:
    """Return the artifact path required for artifact validation."""

    if context.artifact_path is None:
        raise ValueError("Artifact validation requires context.artifact_path")
    return context.artifact_path


def format_invalid_zip_message(artifact_path: Path) -> str:
    """Format an invalid zip archive message."""

    return f"Artifact is not a valid zip archive:\n{artifact_path.name}"
