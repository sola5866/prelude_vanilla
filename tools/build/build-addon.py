"""Build a single addon workspace into an mcpack artifact."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import shutil
import stat
import sys
from zipfile import ZIP_DEFLATED, ZipFile

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.build.generators import generate_contents, generate_textures_list
from tools.build.transforms import minify_json_files
from tools.shared.addons import Addon, load_addon
from tools.shared.logging import get_logger
from tools.validate.context import ValidationContext
from tools.validate.results import ValidationReport
from tools.validate.runner import ValidationRunner
from tools.validate.rules.addon.addon_recognizable import AddonRecognizableRule
from tools.validate.rules.addon.manifest_exists import ManifestExistsRule
from tools.validate.rules.build.artifact_contains_generated_files import (
    ArtifactContainsGeneratedFilesRule,
)
from tools.validate.rules.build.artifact_is_zip_readable import ArtifactIsZipReadableRule
from tools.validate.rules.build.artifact_name_matches_convention import (
    ArtifactNameMatchesConventionRule,
)
from tools.validate.rules.build.generated_files_exist import GeneratedFilesExistRule
from tools.validate.rules.build.generated_files_valid import GeneratedFilesValidRule

LOGGER = get_logger(__name__)


@dataclass(frozen=True, slots=True)
class AddonBuildResult:
    """Result of building one addon."""

    addon: Addon
    workspace_path: Path
    artifact_path: Path


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for single-addon build."""

    parser = argparse.ArgumentParser(
        description="Build a single addon directory into an mcpack artifact."
    )
    parser.add_argument("addon_path", type=Path, help="Path to the addon directory.")
    parser.add_argument(
        "--version",
        required=True,
        help="Artifact version string, for example 26.5.1.",
    )
    parser.add_argument(
        "--keep-workspace",
        action="store_true",
        help="Keep the prepared workspace after the build finishes.",
    )
    return parser.parse_args()


def main() -> int:
    """Run the single-addon build CLI."""

    args = parse_args()
    try:
        result = build_addon(
            args.addon_path,
            args.version,
            keep_workspace=args.keep_workspace,
        )
    except Exception:
        return 1

    print(result.artifact_path)
    return 0


def build_addon(
    addon_path: Path,
    version: str,
    *,
    keep_workspace: bool = False,
) -> AddonBuildResult:
    """Build the addon at the provided path into an mcpack artifact."""

    try:
        repo_root = get_repo_root()
        addon = load_addon(addon_path)

        LOGGER.info("ビルド開始: %s", addon.name)
        LOGGER.info("Running addon validation")
        validation_report = run_addon_validation(repo_root, addon, version)
        ensure_validation_passed(validation_report)

        LOGGER.info("Workspace作成: %s", addon.name)
        workspace_path = prepare_workspace(repo_root, addon)

        LOGGER.info("Addonコピー: %s", addon.name)
        copy_addon_to_workspace(addon, workspace_path)

        LOGGER.info("LICENSEコピー: %s", addon.name)
        copy_license_to_workspace(repo_root, workspace_path)

        transformed_count = minify_json_files(workspace_path)
        LOGGER.info("JSON files transformed: %s", transformed_count)

        generate_textures_list(workspace_path)
        generate_contents(workspace_path)

        LOGGER.info("Running build artifact validation")
        build_artifact_validation_report = run_build_artifact_validation(
            repo_root,
            addon,
            version,
            workspace_path,
        )
        ensure_build_artifact_validation_passed(build_artifact_validation_report)

        LOGGER.info("mcpack生成: %s", addon.name)
        artifact_path = build_mcpack(repo_root, workspace_path, addon, version)

        LOGGER.info("Running artifact validation")
        artifact_validation_report = run_artifact_validation(
            repo_root,
            addon,
            version,
            workspace_path,
            artifact_path,
        )
        ensure_artifact_validation_passed(artifact_validation_report)

        result = AddonBuildResult(
            addon=addon,
            workspace_path=workspace_path,
            artifact_path=artifact_path,
        )

        if not keep_workspace:
            cleanup_workspace(workspace_path)

        LOGGER.info("ビルド成功: %s", addon.name)

        # TODO: changelog generation
        # TODO: version update
        # TODO: GitHub Release integration
        return result
    except Exception:
        LOGGER.error("ビルド失敗: %s", addon_path)
        raise


def run_addon_validation(repo_root: Path, addon: Addon, version: str) -> ValidationReport:
    """Run addon validation rules for the provided addon."""

    context = ValidationContext(
        repo_root=repo_root,
        addons_root=repo_root / "addons",
        addon=addon,
        version=version,
    )
    runner = ValidationRunner(
        rules=[
            ManifestExistsRule(),
            AddonRecognizableRule(),
        ]
    )
    return runner.run(context)


def ensure_validation_passed(report: ValidationReport) -> None:
    """Stop the build when validation fails."""

    if report.failed == 0:
        return

    LOGGER.error("Validation failed")
    raise ValueError("Addon validation failed")


def run_build_artifact_validation(
    repo_root: Path,
    addon: Addon,
    version: str,
    workspace_path: Path,
) -> ValidationReport:
    """Run build artifact validation for the prepared workspace."""

    context = ValidationContext(
        repo_root=repo_root,
        addons_root=repo_root / "addons",
        addon=addon,
        version=version,
        workspace_path=workspace_path,
    )
    runner = ValidationRunner(
        rules=[
            GeneratedFilesExistRule(),
            GeneratedFilesValidRule(),
        ]
    )
    return runner.run(context)


def ensure_build_artifact_validation_passed(report: ValidationReport) -> None:
    """Stop the build when generated files are missing or invalid."""

    if report.failed == 0:
        return

    LOGGER.error("Build artifact validation failed")
    raise ValueError("Build artifact validation failed")


def run_artifact_validation(
    repo_root: Path,
    addon: Addon,
    version: str,
    workspace_path: Path,
    artifact_path: Path,
) -> ValidationReport:
    """Run artifact validation for the built mcpack file."""

    context = ValidationContext(
        repo_root=repo_root,
        addons_root=repo_root / "addons",
        addon=addon,
        version=version,
        workspace_path=workspace_path,
        artifact_path=artifact_path,
    )
    runner = ValidationRunner(
        rules=[
            ArtifactIsZipReadableRule(),
            ArtifactContainsGeneratedFilesRule(),
            ArtifactNameMatchesConventionRule(),
        ]
    )
    return runner.run(context)


def ensure_artifact_validation_passed(report: ValidationReport) -> None:
    """Stop the build when artifact validation fails."""

    if report.failed == 0:
        return

    LOGGER.error("Artifact validation failed")
    raise ValueError("Artifact validation failed")


def get_repo_root() -> Path:
    """Return the repository root path."""

    return REPO_ROOT


def prepare_workspace(repo_root: Path, addon: Addon) -> Path:
    """Prepare a clean workspace directory for the addon."""

    workspace_path = repo_root / "build" / "workspaces" / addon.name
    if workspace_path.exists():
        archive_existing_workspace(workspace_path)
    workspace_path.mkdir(parents=True, exist_ok=True)
    return workspace_path


def archive_existing_workspace(workspace_path: Path) -> None:
    """Archive and remove an existing workspace before rebuilding."""

    stale_path = workspace_path.with_name(f"{workspace_path.name}.stale")
    if stale_path.exists():
        cleanup_workspace(stale_path)

    workspace_path.rename(stale_path)
    cleanup_workspace(stale_path)


def copy_addon_to_workspace(addon: Addon, workspace_path: Path) -> None:
    """Copy addon contents into the prepared workspace."""

    for source in addon.path.iterdir():
        destination = workspace_path / source.name
        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)


def copy_license_to_workspace(repo_root: Path, workspace_path: Path) -> None:
    """Copy the repository LICENSE file into the workspace."""

    license_path = repo_root / "LICENSE"
    if not license_path.is_file():
        raise FileNotFoundError(f"Repository LICENSE was not found: {license_path}")

    shutil.copy2(license_path, workspace_path / "LICENSE")


def build_mcpack(
    repo_root: Path,
    workspace_path: Path,
    addon: Addon,
    version: str,
) -> Path:
    """Create an mcpack archive from the prepared workspace."""

    dist_dir = repo_root / "dist" / f"v{version}"
    dist_dir.mkdir(parents=True, exist_ok=True)

    artifact_path = dist_dir / f"{addon.name}_{version}.mcpack"
    if artifact_path.exists():
        artifact_path.unlink()

    with ZipFile(artifact_path, "w", compression=ZIP_DEFLATED) as archive:
        for file_path in sorted(workspace_path.rglob("*")):
            if file_path.is_file():
                archive.write(file_path, file_path.relative_to(workspace_path))

    return artifact_path


def cleanup_workspace(workspace_path: Path) -> None:
    """Remove a workspace directory without failing the build on cleanup errors."""

    if not workspace_path.exists():
        return

    try:
        shutil.rmtree(workspace_path, onexc=handle_remove_readonly)
    except OSError:
        LOGGER.warning("Workspace削除失敗: %s", workspace_path)


def handle_remove_readonly(function, path: str, excinfo) -> None:
    """Retry deletion after clearing the readonly bit on Windows."""

    _ = excinfo
    os.chmod(path, stat.S_IWRITE)
    function(path)


if __name__ == "__main__":
    raise SystemExit(main())
