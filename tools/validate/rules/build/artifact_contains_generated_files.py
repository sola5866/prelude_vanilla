"""Generated file presence validation for built artifacts."""

from __future__ import annotations

from zipfile import ZipFile

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus
from tools.validate.rules.build.artifact_is_zip_readable import get_artifact_path

REQUIRED_ARTIFACT_FILES = (
    "LICENSE",
    "contents.json",
    "textures_list.json",
)


class ArtifactContainsGeneratedFilesRule:
    """Validate that required generated files are present in the artifact."""

    rule_id = "artifact_contains_generated_files"
    category = "build"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """Check the artifact contents for required generated files."""

        artifact_path = get_artifact_path(context)
        with ZipFile(artifact_path, "r") as archive:
            names = {entry.filename for entry in archive.infolist()}

        for relative_path in REQUIRED_ARTIFACT_FILES:
            if relative_path not in names:
                return [
                    RuleResult(
                        rule_id=self.rule_id,
                        category=self.category,
                        status=ValidationStatus.FAILED,
                        target=str(artifact_path),
                        message=f"Artifact missing file:\n{relative_path}",
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
