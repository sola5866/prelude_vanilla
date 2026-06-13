from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path


def load_env(env_path: Path) -> dict[str, str]:
    values: dict[str, str] = {}

    if not env_path.exists():
        raise FileNotFoundError(f".env not found: {env_path}")

    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    return values


def is_addon_dir(path: Path) -> bool:
    return path.is_dir() and (path / "manifest.json").is_file()


def discover_addons(addons_dir: Path) -> list[Path]:
    return sorted(
        path
        for path in addons_dir.iterdir()
        if is_addon_dir(path)
    )


def create_junction(link_path: Path, target_path: Path, *, dry_run: bool) -> None:
    if link_path.exists():
        print(f"SKIP: already exists: {link_path}")
        return

    command = [
        "cmd",
        "/c",
        "mklink",
        "/J",
        str(link_path),
        str(target_path),
    ]

    if dry_run:
        print(f"DRY RUN: {' '.join(command)}")
        return

    print(f"LINK: {link_path} -> {target_path}")
    subprocess.run(command, check=True)


def remove_junction(link_path: Path, *, dry_run: bool) -> None:
    if not link_path.exists():
        print(f"SKIP: not found: {link_path}")
        return

    command = [
        "cmd",
        "/c",
        "rmdir",
        str(link_path),
    ]

    if dry_run:
        print(f"DRY RUN: {' '.join(command)}")
        return

    print(f"REMOVE: {link_path}")
    subprocess.run(command, check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create junctions from Prelude Vanilla addons to Minecraft development_resource_packs."
    )

    parser.add_argument(
        "--env",
        type=Path,
        default=Path(".env"),
        help="Path to .env file.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print actions without changing files.",
    )

    parser.add_argument(
        "--remove",
        action="store_true",
        help="Remove created junctions from Minecraft development_resource_packs.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if os.name != "nt":
        print("This script currently supports Windows only.", file=sys.stderr)
        return 1

    env = load_env(args.env)

    try:
        minecraft_resource_packs_dir = Path(
            env["MINECRAFT_RESOURCE_PACKS_DIR"])
        addons_dir = Path(env["PRELUDE_VANILLA_ADDONS_DIR"])
    except KeyError as error:
        print(f"Missing environment variable: {error}", file=sys.stderr)
        return 1

    if not minecraft_resource_packs_dir.exists():
        print(
            f"Minecraft resource packs directory not found: {minecraft_resource_packs_dir}",
            file=sys.stderr,
        )
        return 1

    if not addons_dir.exists():
        print(f"Addons directory not found: {addons_dir}", file=sys.stderr)
        return 1

    addons = discover_addons(addons_dir)

    if not addons:
        print(f"No addons found: {addons_dir}", file=sys.stderr)
        return 1

    for addon_path in addons:
        link_path = minecraft_resource_packs_dir / addon_path.name

        if args.remove:
            remove_junction(link_path, dry_run=args.dry_run)
        else:
            create_junction(link_path, addon_path, dry_run=args.dry_run)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
