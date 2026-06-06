"""リポジトリ構成を確認する Repository Rule。"""

from __future__ import annotations

from pathlib import Path

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus


class RepositoryStructureRule:
    """必須ディレクトリと必須ファイルの存在を検証する。"""

    rule_id = "repository_structure"
    category = "repository"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """リポジトリの必須構成を確認して結果を返す。"""

        repo_root = context.repo_root
        required_paths = [
            repo_root / "addons",
            repo_root / "docs",
            repo_root / "tools",
            repo_root / "LICENSE",
        ]

        missing = [path.name for path in required_paths if not path.exists()]
        if not missing:
            return [
                RuleResult(
                    rule_id=self.rule_id,
                    category=self.category,
                    status=ValidationStatus.PASSED,
                    target=str(repo_root),
                    message=None,
                )
            ]

        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.FAILED,
                target=str(repo_root),
                message=f"必須構成が不足しています: {', '.join(missing)}",
            )
        ]
