"""LICENSE コピー元の存在を確認する Repository Rule。"""

from __future__ import annotations

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus


class LicenseSourceExistsRule:
    """build-addon.py が利用する LICENSE コピー元の存在を検証する。"""

    rule_id = "license_source_exists"
    category = "repository"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """リポジトリルートの LICENSE の存在有無を確認して結果を返す。"""

        license_path = context.repo_root / "LICENSE"
        if license_path.is_file():
            return [
                RuleResult(
                    rule_id=self.rule_id,
                    category=self.category,
                    status=ValidationStatus.PASSED,
                    target=str(context.repo_root),
                    message=None,
                )
            ]

        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.FAILED,
                target=str(context.repo_root),
                message="LICENSE not found at repository root",
            )
        ]
