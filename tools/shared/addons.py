"""アドオン判定、探索、情報ロードを提供する共通モジュール。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json


@dataclass(frozen=True, slots=True)
class Addon:
    """ビルドや検証で扱うアドオン情報を表す。"""

    name: str
    path: Path
    manifest_path: Path


def is_addon(path: Path) -> bool:
    """指定されたパスがアドオンディレクトリかどうかを返す。"""

    manifest_path = path / "manifest.json"
    return path.is_dir() and manifest_path.is_file()


def load_addon(path: Path) -> Addon:
    """アドオンディレクトリから最低限のアドオン情報を読み込む。"""

    addon_path = path.resolve()
    if not is_addon(addon_path):
        raise ValueError(f"Addon manifest was not found: {addon_path}")

    manifest_path = addon_path / "manifest.json"
    manifest = _load_manifest(manifest_path)
    header = manifest.get("header")
    if not isinstance(header, dict):
        raise ValueError(f"Addon manifest header is invalid: {manifest_path}")

    name = header.get("name")
    if not isinstance(name, str) or not name.strip():
        raise ValueError(f"Addon name is missing in manifest: {manifest_path}")

    return Addon(
        name=addon_path.name,
        path=addon_path,
        manifest_path=manifest_path,
    )


def discover_addons(root: Path) -> list[Addon]:
    """指定されたルート直下からアドオンディレクトリを探索する。"""

    root_path = root.resolve()
    if not root_path.is_dir():
        raise ValueError(f"Addon root directory was not found: {root_path}")

    addons: list[Addon] = []
    for child in sorted(root_path.iterdir(), key=lambda item: item.name):
        if is_addon(child):
            addons.append(load_addon(child))
    return addons


def _load_manifest(manifest_path: Path) -> dict[str, object]:
    """manifest.json を辞書として読み込む。"""

    with manifest_path.open("r", encoding="utf-8") as file:
        manifest = json.load(file)

    if not isinstance(manifest, dict):
        raise ValueError(f"Addon manifest root must be an object: {manifest_path}")
    return manifest
