"""Generate ``contents.json`` from a prepared addon workspace."""

from __future__ import annotations

import json
from pathlib import Path

from tools.shared.logging import get_logger

LOGGER = get_logger(__name__)


def generate_contents(workspace_path: Path) -> Path:
    """Generate ``contents.json`` from files under the workspace.

    Args:
        workspace_path: Root path of the prepared addon workspace.

    Returns:
        Path to the generated ``contents.json`` file.
    """

    entries = sorted(_collect_workspace_files(workspace_path))
    output_path = workspace_path / "contents.json"
    output_path.write_text(
        json.dumps(entries, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    LOGGER.info("contents.json generated")
    return output_path


def _collect_workspace_files(workspace_path: Path) -> list[str]:
    """Collect workspace file paths for ``contents.json`` generation."""

    files: list[str] = []
    for file_path in workspace_path.rglob("*"):
        if not file_path.is_file():
            continue

        relative_path = file_path.relative_to(workspace_path).as_posix()
        if relative_path == "contents.json":
            continue
        files.append(relative_path)

    return files
