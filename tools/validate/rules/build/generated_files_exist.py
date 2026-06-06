"""Generated file existence validation for build workspaces."""

from __future__ import annotations

from pathlib import Path

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus

class GeneratedFilesExistRule:
    """Validate that required generated files exist in the workspace."""

    rule_id = "generated_files_exist"
    category = "build"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """Check the workspace for required generated files."""

        workspace_path = get_workspace_path(context)
        required_files = ["LICENSE", "contents.json"]
        if has_textures_directory(workspace_path):
            required_files.append("textures/textures_list.json")

        missing_files = [
            relative_path
            for relative_path in required_files
            if not (workspace_path / relative_path).is_file()
        ]

        if not missing_files:
            return [
                RuleResult(
                    rule_id=self.rule_id,
                    category=self.category,
                    status=ValidationStatus.PASSED,
                    target=str(workspace_path),
                    message=None,
                )
            ]

        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.FAILED,
                target=str(workspace_path),
                message=format_missing_file_message(missing_files[0]),
            )
        ]


def get_workspace_path(context: ValidationContext) -> Path:
    """Return the workspace path required for build validation."""

    if context.workspace_path is None:
        raise ValueError("Build validation requires context.workspace_path")
    return context.workspace_path


def format_missing_file_message(relative_path: str) -> str:
    """Format a human-readable missing generated file message."""

    return f"Missing generated file:\n{relative_path}"


def has_textures_directory(workspace_path: Path) -> bool:
    """Return whether the workspace contains a textures directory."""

    return (workspace_path / "textures").is_dir()
