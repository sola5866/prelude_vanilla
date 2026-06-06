"""Shared context for validation rule execution."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from tools.shared.addons import Addon


@dataclass(frozen=True, slots=True)
class ValidationContext:
    """Inputs shared across validation rules."""

    repo_root: Path
    addons_root: Path | None
    addon: Addon | None
    version: str | None
    workspace_path: Path | None = None
    artifact_path: Path | None = None
