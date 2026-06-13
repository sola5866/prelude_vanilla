"""Minify JSON and JSONC files in a prepared addon workspace."""

from __future__ import annotations

import json
from pathlib import Path

from tools.shared.logging import get_logger
from tools.shared.jsonc import loads_jsonc

LOGGER = get_logger(__name__)


def minify_json_files(
    workspace_path: Path,
    *,
    excluded_paths: set[str] | None = None,
) -> int:
    """Minify JSON files under the workspace.

    Args:
        workspace_path: Root path of the prepared addon workspace.
        excluded_paths: Workspace-relative paths excluded from transformation.

    Returns:
        Number of transformed JSON files.
    """

    LOGGER.info("JSON minify started")
    normalized_exclusions = {
        _normalize_relative_path(path) for path in (excluded_paths or set())
    }
    transformed = 0

    for file_path in sorted(workspace_path.rglob("*.json")):
        relative_path = file_path.relative_to(workspace_path).as_posix()
        if relative_path in normalized_exclusions:
            continue

        LOGGER.info("Minifying: %s", relative_path)
        source_text = file_path.read_text(encoding="utf-8")
        data = _load_jsonc(source_text, relative_path)
        file_path.write_text(
            json.dumps(data, ensure_ascii=False, separators=(",", ":")),
            encoding="utf-8",
        )
        transformed += 1

    LOGGER.info("JSON minify completed")
    return transformed


def _load_jsonc(source_text: str, relative_path: str) -> object:
    """Parse JSONC text after removing comments."""

    try:
        return loads_jsonc(source_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse JSON:\n{relative_path}") from exc


def _normalize_relative_path(path: str) -> str:
    """Normalize a workspace-relative path to POSIX separators."""

    return Path(path).as_posix()
