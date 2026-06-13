"""Format JSON and JSONC source files for development workflows."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.shared.jsonc import load_jsonc

DEFAULT_TARGET = Path("addons")
EXCLUDED_ROOT_NAMES = {"dist", "build", ".venv", ".uv-cache"}


@dataclass(frozen=True, slots=True)
class ParseErrorResult:
    """A JSON or JSONC parse failure for one file."""

    path: Path
    error: str


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for the formatter."""

    parser = argparse.ArgumentParser(
        description="Format JSON and JSONC files under addons or a specified path."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="Optional file or directory targets. Defaults to addons/.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report files that need formatting without rewriting them.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the JSON formatter CLI."""

    args = parse_args()
    targets = args.paths or [DEFAULT_TARGET]
    repo_root = REPO_ROOT

    try:
        files = collect_target_files(repo_root, targets)
    except FileNotFoundError as exc:
        print(str(exc))
        return 1

    parse_errors: list[ParseErrorResult] = []
    dirty_files: list[Path] = []
    changed_files: list[Path] = []

    for file_path in files:
        try:
            formatted_text = format_json_file_text(file_path)
        except (json.JSONDecodeError, UnicodeDecodeError, OSError, ValueError) as exc:
            parse_errors.append(ParseErrorResult(path=file_path, error=str(exc)))
            continue

        current_text = file_path.read_text(encoding="utf-8")
        if current_text == formatted_text:
            continue

        if args.check:
            dirty_files.append(file_path)
            continue

        file_path.write_text(formatted_text, encoding="utf-8")
        changed_files.append(file_path)

    for result in parse_errors:
        print(format_parse_error(result))

    if args.check:
        for file_path in dirty_files:
            print(display_path(file_path, repo_root))

        if parse_errors or dirty_files:
            return 1
        return 0

    for file_path in changed_files:
        print(display_path(file_path, repo_root))

    print(f"Changed files: {len(changed_files)}")
    return 1 if parse_errors else 0


def collect_target_files(repo_root: Path, targets: list[Path]) -> list[Path]:
    """Collect JSON files under the requested targets."""

    files: set[Path] = set()
    for target in targets:
        resolved_target = resolve_target_path(repo_root, target)
        if not resolved_target.exists():
            raise FileNotFoundError(f"Target path not found: {resolved_target}")

        if resolved_target.is_file():
            if resolved_target.suffix.lower() == ".json" and not is_excluded_path(
                repo_root,
                resolved_target,
            ):
                files.add(resolved_target)
            continue

        for file_path in resolved_target.rglob("*.json"):
            if is_excluded_path(repo_root, file_path):
                continue
            files.add(file_path)

    return sorted(files)


def resolve_target_path(repo_root: Path, target: Path) -> Path:
    """Resolve a user-supplied file or directory target."""

    if target.is_absolute():
        return target.resolve()
    return (repo_root / target).resolve()


def is_excluded_path(repo_root: Path, path: Path) -> bool:
    """Return whether a path should be excluded from formatting."""

    try:
        relative_parts = path.resolve().relative_to(repo_root).parts
    except ValueError:
        return False
    return any(part in EXCLUDED_ROOT_NAMES for part in relative_parts)


def format_json_file_text(path: Path) -> str:
    """Return the normalized JSON text for one file."""

    data = load_jsonc(path)
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def format_parse_error(result: ParseErrorResult) -> str:
    """Format a parse error for console output."""

    return (
        f"Failed to parse JSON:\n"
        f"{display_path(result.path, REPO_ROOT)}\n"
        f"{result.error}"
    )


def display_path(path: Path, repo_root: Path) -> str:
    """Return a repo-relative path when possible."""

    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return str(path)


if __name__ == "__main__":
    raise SystemExit(main())
