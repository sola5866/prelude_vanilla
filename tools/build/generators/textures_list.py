"""Generate ``textures/textures_list.json`` from a prepared addon workspace."""

from __future__ import annotations

import json
from pathlib import Path

from tools.shared.logging import get_logger

LOGGER = get_logger(__name__)


def generate_textures_list(workspace_path: Path) -> Path:
    """Generate ``textures/textures_list.json`` from ``textures/**/*.png`` files.

    Args:
        workspace_path: Root path of the prepared addon workspace.

    Returns:
        Path to the generated ``textures/textures_list.json`` file.
    """

    output_path = workspace_path / "textures" / "textures_list.json"
    textures_path = workspace_path / "textures"
    if not textures_path.is_dir():
        return output_path

    entries = sorted(_collect_texture_entries(workspace_path))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    LOGGER.info("textures/textures_list.json generated")
    return output_path


def _collect_texture_entries(workspace_path: Path) -> list[str]:
    """Collect texture paths without the ``.png`` suffix."""

    textures_path = workspace_path / "textures"
    if not textures_path.is_dir():
        return []

    entries: list[str] = []
    for file_path in textures_path.rglob("*"):
        if not file_path.is_file():
            continue
        if file_path.suffix.lower() != ".png":
            continue

        relative_path = file_path.relative_to(workspace_path).with_suffix("")
        entries.append(relative_path.as_posix())

    return entries
