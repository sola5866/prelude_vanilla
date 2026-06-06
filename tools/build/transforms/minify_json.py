"""Minify JSON and JSONC files in a prepared addon workspace."""

from __future__ import annotations

import json
from pathlib import Path

from tools.shared.logging import get_logger

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
        return json.loads(_strip_json_comments(source_text))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Failed to parse JSON:\n{relative_path}") from exc


def _strip_json_comments(source_text: str) -> str:
    """Remove JSONC comments while preserving string contents."""

    output: list[str] = []
    index = 0
    in_string = False
    escape = False
    length = len(source_text)

    while index < length:
        current = source_text[index]
        next_char = source_text[index + 1] if index + 1 < length else ""

        if in_string:
            output.append(current)
            if escape:
                escape = False
            elif current == "\\":
                escape = True
            elif current == '"':
                in_string = False
            index += 1
            continue

        if current == '"':
            in_string = True
            output.append(current)
            index += 1
            continue

        if current == "/" and next_char == "/":
            index = _skip_single_line_comment(source_text, index + 2)
            continue

        if current == "/" and next_char == "*":
            index = _skip_multi_line_comment(source_text, index + 2)
            continue

        output.append(current)
        index += 1

    return "".join(output)


def _skip_single_line_comment(source_text: str, index: int) -> int:
    """Skip a single-line comment and preserve the line ending."""

    length = len(source_text)
    while index < length and source_text[index] not in "\r\n":
        index += 1
    return index


def _skip_multi_line_comment(source_text: str, index: int) -> int:
    """Skip a multi-line comment."""

    length = len(source_text)
    while index < length - 1:
        if source_text[index] == "*" and source_text[index + 1] == "/":
            return index + 2
        index += 1
    return length


def _normalize_relative_path(path: str) -> str:
    """Normalize a workspace-relative path to POSIX separators."""

    return Path(path).as_posix()
