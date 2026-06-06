"""manifest.json の存在を確認する Addon Rule。"""

from __future__ import annotations

from pathlib import Path

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus


class ManifestExistsRule:
    """アドオンディレクトリに manifest.json が存在することを検証する。"""

    rule_id = "manifest_exists"
    category = "addon"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """manifest.json の存在有無を RuleResult として返す。"""

        addon_path = get_addon_path(context)
        manifest_path = addon_path / "manifest.json"
        if manifest_path.is_file():
            return [
                RuleResult(
                    rule_id=self.rule_id,
                    category=self.category,
                    status=ValidationStatus.PASSED,
                    target=str(addon_path),
                    message=None,
                )
            ]

        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.FAILED,
                target=str(addon_path),
                message="manifest.json が存在しません",
            )
        ]


def get_addon_path(context: ValidationContext) -> Path:
    """ValidationContext から対象アドオンのパスを取得する。"""

    if context.addon is None:
        raise ValueError("Addon validation requires context.addon")
    return context.addon.path
