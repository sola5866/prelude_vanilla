"""Artifact filename convention validation for build outputs."""

from __future__ import annotations

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus
from tools.validate.rules.build.artifact_is_zip_readable import get_artifact_path


class ArtifactNameMatchesConventionRule:
    """Validate that the artifact filename matches the naming convention."""

    rule_id = "artifact_name_matches_convention"
    category = "build"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """Check the artifact filename against addon name and version."""

        artifact_path = get_artifact_path(context)
        addon = get_addon(context)
        version = get_version(context)
        expected_name = f"{addon.name}_{version}.mcpack"
        actual_name = artifact_path.name

        if actual_name == expected_name:
            return [
                RuleResult(
                    rule_id=self.rule_id,
                    category=self.category,
                    status=ValidationStatus.PASSED,
                    target=str(artifact_path),
                    message=None,
                )
            ]

        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.FAILED,
                target=str(artifact_path),
                message=(
                    "Artifact name does not match convention\n\n"
                    f"Expected:\n{expected_name}\n\n"
                    f"Actual:\n{actual_name}"
                ),
            )
        ]


def get_addon(context: ValidationContext):
    """Return the addon required for artifact naming validation."""

    if context.addon is None:
        raise ValueError("Artifact validation requires context.addon")
    return context.addon


def get_version(context: ValidationContext) -> str:
    """Return the version required for artifact naming validation."""

    if context.version is None:
        raise ValueError("Artifact validation requires context.version")
    return context.version
