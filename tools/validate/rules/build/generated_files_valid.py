"""Generated file content validation for build workspaces."""

from __future__ import annotations

import json
from pathlib import Path

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus
from tools.validate.rules.build.generated_files_exist import get_workspace_path

TARGET_FILES = ("contents.json", "textures/textures_list.json")


class GeneratedFilesValidRule:
    """Validate that generated JSON files have the expected basic structure."""

    rule_id = "generated_files_valid"
    category = "build"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """Check that generated JSON files are readable arrays of strings."""

        workspace_path = get_workspace_path(context)
        for relative_path in TARGET_FILES:
            result = validate_generated_file(workspace_path, relative_path, self.rule_id, self.category)
            if result is not None:
                return [result]

        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.PASSED,
                target=str(workspace_path),
                message=None,
            )
        ]


def validate_generated_file(
    workspace_path: Path,
    relative_path: str,
    rule_id: str,
    category: str,
) -> RuleResult | None:
    """Validate one generated JSON file and return a failure result when invalid."""

    file_path = workspace_path / relative_path
    if not file_path.is_file():
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message=f"Missing generated file:\n{relative_path}",
        )

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message=f"{relative_path} is not valid JSON",
        )

    if not isinstance(data, list):
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message=f"{relative_path} is not a JSON array",
        )

    if any(not isinstance(entry, str) for entry in data):
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message=f"{relative_path} contains non-string entries",
        )

    return None
