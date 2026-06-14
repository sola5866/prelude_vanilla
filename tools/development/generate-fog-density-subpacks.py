"""Generate Cinematic Fog density files from Main addon fog JSON files."""

from __future__ import annotations

import argparse
import copy
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.shared.jsonc import load_jsonc

DEFAULT_MAIN_FOGS = REPO_ROOT / "addons" / "Prelude_Vanilla_Main" / "fogs"
DEFAULT_CINEMATIC_ROOT = (
    REPO_ROOT / "addons" / "Prelude_Vanilla_Cinematic_Fog"
)
SUBPACK_FOLDERS = [str(index) for index in range(21)] + ["default"]
FILENAME_DEFAULTS = {
    "default_fog_setting.json": Decimal("0.005000"),
    "pale_garden_fog_setting.json": Decimal("0.010000"),
    "sulfur_cave_fog_setting.json": Decimal("0.010000"),
}


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Generate Cinematic Fog files from Main addon fog JSON files."
        )
    )
    parser.add_argument(
        "paths",
        nargs="+",
        type=Path,
        help="Main addon fog JSON files to copy.",
    )
    parser.add_argument(
        "--cinematic-root",
        type=Path,
        default=DEFAULT_CINEMATIC_ROOT,
        help="Cinematic Fog addon root directory.",
    )
    parser.add_argument(
        "--mode",
        choices=("fogs", "subpacks", "both"),
        default="both",
        help="Choose whether to copy into fogs, subpacks, or both.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the fog density file generator."""

    args = parse_args()
    cinematic_root = resolve_path(args.cinematic_root)
    cinematic_fogs = cinematic_root / "fogs"
    subpacks_root = cinematic_root / "subpacks"
    errors: list[str] = []
    changed: list[Path] = []

    for source_path in args.paths:
        resolved_source = resolve_path(source_path)
        if not resolved_source.is_file():
            errors.append(f"Source file not found: {resolved_source}")
            continue

        try:
            source_data = load_jsonc(resolved_source)
        except Exception as exc:  # noqa: BLE001 - CLI should report the file
            errors.append(f"Failed to read JSON: {resolved_source}\n{exc}")
            continue

        file_name = resolved_source.name
        if file_name not in FILENAME_DEFAULTS:
            errors.append(
                f"Unsupported fog file name: {resolved_source.name}"
            )
            continue

        if args.mode in {"fogs", "both"}:
            target_path = cinematic_fogs / file_name
            write_json_file(
                target_path,
                update_density(source_data, FILENAME_DEFAULTS[file_name]),
            )
            changed.append(target_path)

        if args.mode in {"subpacks", "both"}:
            for folder in SUBPACK_FOLDERS:
                density = density_for_folder(
                    FILENAME_DEFAULTS[file_name],
                    folder,
                )
                target_path = subpacks_root / folder / "fogs" / file_name
                write_json_file(target_path, update_density(source_data, density))
                changed.append(target_path)

    for error in errors:
        print(error)

    for file_path in changed:
        print(display_path(file_path))

    if errors:
        return 1

    print(f"Changed files: {len(changed)}")
    return 0


def resolve_path(path: Path) -> Path:
    """Resolve a user-supplied path against the repository root."""

    if path.is_absolute():
        return path.resolve()
    return (REPO_ROOT / path).resolve()


def density_for_folder(base: Decimal, folder: str) -> Decimal:
    """Calculate a density value for one subpack folder."""

    if folder == "default":
        folder_index = 15
    else:
        folder_index = int(folder)

    value = float(base) * (10 ** ((folder_index - 10) / 10))
    return Decimal(str(value)).quantize(Decimal("0.000001"), rounding=ROUND_HALF_UP)


def update_density(data: object, density: Decimal) -> object:
    """Update the air density in a loaded fog JSON object."""

    updated = copy.deepcopy(data)
    updated["minecraft:fog_settings"]["volumetric"]["density"]["air"][
        "max_density"
    ] = float(density)
    return updated


def write_json_file(path: Path, data: object) -> None:
    """Write a JSON file with the project standard indentation."""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def display_path(path: Path) -> str:
    """Return a repository-relative path for console output."""

    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
