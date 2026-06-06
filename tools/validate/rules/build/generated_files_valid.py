"""Generated file content validation for build workspaces."""

from __future__ import annotations

import json
from pathlib import Path

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus
from tools.validate.rules.build.generated_files_exist import (
    get_workspace_path,
    has_textures_directory,
)


class GeneratedFilesValidRule:
    """Validate that generated JSON files have the expected basic structure."""

    rule_id = "generated_files_valid"
    category = "build"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """Check that generated JSON files have the expected minimal structure."""

        workspace_path = get_workspace_path(context)

        contents_result = validate_contents_json(workspace_path, self.rule_id, self.category)
        if contents_result is not None:
            return [contents_result]

        if has_textures_directory(workspace_path):
            textures_result = validate_textures_list_json(
                workspace_path,
                self.rule_id,
                self.category,
            )
            if textures_result is not None:
                return [textures_result]

        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.PASSED,
                target=str(workspace_path),
                message=None,
            )
        ]


def validate_contents_json(
    workspace_path: Path,
    rule_id: str,
    category: str,
) -> RuleResult | None:
    """Validate that ``contents.json`` is an empty JSON object."""

    file_path = workspace_path / "contents.json"
    if not file_path.is_file():
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message="Missing generated file:\ncontents.json",
        )

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message="contents.json is not valid JSON",
        )

    if not isinstance(data, dict):
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message="contents.json is not a JSON object",
        )

    if data:
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message="contents.json is not empty",
        )

    return None


def validate_textures_list_json(
    workspace_path: Path,
    rule_id: str,
    category: str,
) -> RuleResult | None:
    """Validate that ``textures/textures_list.json`` is a JSON array of strings."""

    file_path = workspace_path / "textures" / "textures_list.json"
    if not file_path.is_file():
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message="Missing generated file:\ntextures/textures_list.json",
        )

    try:
        data = json.loads(file_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message="textures/textures_list.json is not valid JSON",
        )

    if not isinstance(data, list):
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message="textures/textures_list.json is not a JSON array",
        )

    if any(not isinstance(entry, str) for entry in data):
        return RuleResult(
            rule_id=rule_id,
            category=category,
            status=ValidationStatus.FAILED,
            target=str(workspace_path),
            message="textures/textures_list.json contains non-string entries",
        )

    return None
