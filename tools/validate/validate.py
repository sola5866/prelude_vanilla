"""Validation システムのエントリーポイント。"""

from __future__ import annotations

from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus
from tools.validate.runner import ValidationRunner
from tools.validate.rules.repository.addon_name_unique import AddonNameUniqueRule
from tools.validate.rules.repository.addon_uuid_unique import AddonUuidUniqueRule
from tools.validate.rules.repository.license_source_exists import LicenseSourceExistsRule
from tools.validate.rules.repository.repository_structure import RepositoryStructureRule


def main() -> int:
    """Repository Rule を実行して結果を表示する。"""

    context = build_context()
    rules = build_rules()
    runner = ValidationRunner(rules)

    print("Validation started")
    print()
    report = runner.run(context)

    for result in report.results:
        print_result(result)

    print()
    print(f"Successful: {report.successful}")
    print(f"Failed: {report.failed}")
    return 0 if report.failed == 0 else 1


def build_context() -> ValidationContext:
    """Repository Validation 用の ValidationContext を構築する。"""

    return ValidationContext(
        repo_root=REPO_ROOT,
        addons_root=REPO_ROOT / "addons",
        addon=None,
        version=None,
    )


def build_rules() -> list:
    """初期実装で実行する Repository Rule 一覧を返す。"""

    return [
        RepositoryStructureRule(),
        AddonNameUniqueRule(),
        AddonUuidUniqueRule(),
        LicenseSourceExistsRule(),
    ]


def print_result(result: RuleResult) -> None:
    """RuleResult を CLI 向けの表示形式で出力する。"""

    prefix = "PASS" if result.status is ValidationStatus.PASSED else "FAIL"
    print(f"{prefix} {result.rule_id}")
    if result.status is ValidationStatus.FAILED and result.message:
        print()
        print(result.message)
        print()


if __name__ == "__main__":
    raise SystemExit(main())
