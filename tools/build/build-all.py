"""addons 配下の全アドオンを順番にビルドするツール。"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import importlib.util
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.shared.addons import Addon, discover_addons
from tools.shared.logging import get_logger
from tools.validate.context import ValidationContext
from tools.validate.results import ValidationReport
from tools.validate.runner import ValidationRunner
from tools.validate.rules.repository.addon_name_unique import AddonNameUniqueRule
from tools.validate.rules.repository.addon_uuid_unique import AddonUuidUniqueRule
from tools.validate.rules.repository.license_source_exists import LicenseSourceExistsRule
from tools.validate.rules.repository.repository_structure import RepositoryStructureRule

LOGGER = get_logger(__name__)


def load_build_addon_module():
    """build-addon.py をモジュールとして読み込んで返す。"""

    module_path = REPO_ROOT / "tools" / "build" / "build-addon.py"
    spec = importlib.util.spec_from_file_location("tools.build.build_addon_runtime", module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load build-addon module: {module_path}")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


_BUILD_ADDON_MODULE = load_build_addon_module()
AddonBuildResult = _BUILD_ADDON_MODULE.AddonBuildResult
build_addon = _BUILD_ADDON_MODULE.build_addon
get_repo_root = _BUILD_ADDON_MODULE.get_repo_root


@dataclass(frozen=True, slots=True)
class FailedAddonBuild:
    """ビルドに失敗したアドオン情報を表す。"""

    addon: Addon
    error: str


@dataclass(frozen=True, slots=True)
class AddonReport:
    """単一アドオンの Build Report 項目を表す。"""

    name: str
    status: str
    artifact: str | None
    error: str | None


@dataclass(frozen=True, slots=True)
class BuildReport:
    """全体ビルドの JSON 出力向けデータを表す。"""

    version: str
    successful: int
    failed: int
    addons: list[AddonReport]


@dataclass(frozen=True, slots=True)
class BuildAllResult:
    """全アドオンのビルド集計結果を表す。"""

    successful: list[AddonBuildResult]
    failed: list[FailedAddonBuild]
    report: BuildReport | None
    report_path: Path | None


def parse_args() -> argparse.Namespace:
    """コマンドライン引数を解析する。"""

    parser = argparse.ArgumentParser(
        description="Build all addons under the addons directory."
    )
    parser.add_argument(
        "--version",
        required=True,
        help="Artifact version string, for example 26.5.1.",
    )
    parser.add_argument(
        "--addons-root",
        type=Path,
        default=Path("addons"),
        help="Path to the addons root directory.",
    )
    parser.add_argument(
        "--keep-workspace",
        action="store_true",
        help="Keep each prepared workspace after the build finishes.",
    )
    return parser.parse_args()


def main() -> int:
    """全アドオンのビルドを実行して終了コードを返す。"""

    args = parse_args()
    try:
        result = build_all_addons(
            args.version,
            addons_root=args.addons_root,
            keep_workspace=args.keep_workspace,
        )
    except Exception:
        return 1
    return 0 if not result.failed else 1


def build_all_addons(
    version: str,
    *,
    addons_root: Path,
    keep_workspace: bool = False,
) -> BuildAllResult:
    """addons 配下の全アドオンを順番にビルドして集計結果を返す。"""

    repo_root = get_repo_root()
    resolved_addons_root = resolve_addons_root(repo_root, addons_root)

    LOGGER.info("Running repository validation")
    validation_report = run_repository_validation(repo_root, resolved_addons_root)
    ensure_validation_passed(validation_report)

    addons = discover_addons(resolved_addons_root)
    LOGGER.info("全体ビルド開始")

    successful: list[AddonBuildResult] = []
    failed: list[FailedAddonBuild] = []
    addon_reports: list[AddonReport] = []

    total = len(addons)
    for index, addon in enumerate(addons, start=1):
        LOGGER.info("[%s/%s] %s", index, total, addon.name)
        try:
            result = build_addon(
                addon.path,
                version,
                keep_workspace=keep_workspace,
            )
        except Exception as error:
            message = str(error)
            failed_build = FailedAddonBuild(addon=addon, error=message)
            failed.append(failed_build)
            addon_reports.append(
                AddonReport(
                    name=addon.name,
                    status="failed",
                    artifact=None,
                    error=message,
                )
            )
            continue

        successful.append(result)
        addon_reports.append(
            AddonReport(
                name=addon.name,
                status="success",
                artifact=result.artifact_path.name,
                error=None,
            )
        )

    report = BuildReport(
        version=version,
        successful=len(successful),
        failed=len(failed),
        addons=addon_reports,
    )
    report_path = write_build_report(repo_root, report)

    LOGGER.info("全体ビルド完了")
    LOGGER.info("Successful: %s", report.successful)
    LOGGER.info("Failed: %s", report.failed)

    for failed_build in failed:
        LOGGER.error("%s: %s", failed_build.addon.path, failed_build.error)

    return BuildAllResult(
        successful=successful,
        failed=failed,
        report=report,
        report_path=report_path,
    )


def run_repository_validation(repo_root: Path, addons_root: Path) -> ValidationReport:
    """Repository Rule を実行して ValidationReport を返す。"""

    context = ValidationContext(
        repo_root=repo_root,
        addons_root=addons_root,
        addon=None,
        version=None,
    )
    runner = ValidationRunner(
        rules=[
            RepositoryStructureRule(),
            AddonNameUniqueRule(),
            AddonUuidUniqueRule(),
            LicenseSourceExistsRule(),
        ]
    )
    return runner.run(context)


def ensure_validation_passed(report: ValidationReport) -> None:
    """Validation 失敗時に全体ビルドを中断する。"""

    if report.failed == 0:
        return

    LOGGER.error("Validation failed")
    raise ValueError("Repository validation failed")


def resolve_addons_root(repo_root: Path, addons_root: Path) -> Path:
    """addons ルートの入力をリポジトリ基準の絶対パスへ解決する。"""

    if addons_root.is_absolute():
        return addons_root
    return (repo_root / addons_root).resolve()


def write_build_report(repo_root: Path, report: BuildReport) -> Path:
    """Build Report を dist 配下へ JSON として保存する。"""

    report_path = repo_root / "dist" / f"v{report.version}" / "build-report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with report_path.open("w", encoding="utf-8") as file:
        json.dump(asdict(report), file, ensure_ascii=False, indent=2)
        file.write("\n")

    return report_path


if __name__ == "__main__":
    raise SystemExit(main())
