"""Generate ``contents.json`` from a prepared addon workspace."""

from __future__ import annotations

import json
from pathlib import Path

from tools.shared.logging import get_logger

LOGGER = get_logger(__name__)


def generate_contents(workspace_path: Path) -> Path:
    """Generate ``contents.json`` as an empty JSON object.

    Returns:
        Path to the generated ``contents.json`` file.
    """

    entries = {}
    output_path = workspace_path / "contents.json"
    output_path.write_text(
        json.dumps(entries, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    LOGGER.info("contents.json generated")
    return output_path
