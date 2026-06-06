"""アドオンとして認識できるかを確認する Addon Rule。"""

from __future__ import annotations

from pathlib import Path

from tools.shared.addons import is_addon
from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus


class AddonRecognizableRule:
    """tools.shared.addons.is_addon() による認識可否を検証する。"""

    rule_id = "addon_recognizable"
    category = "addon"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """対象ディレクトリがアドオンとして認識可能かを返す。"""

        addon_path = get_addon_path(context)
        if is_addon(addon_path):
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
                message="tools.shared.addons.is_addon() が False を返しました",
            )
        ]


def get_addon_path(context: ValidationContext) -> Path:
    """ValidationContext から対象アドオンのパスを取得する。"""

    if context.addon is None:
        raise ValueError("Addon validation requires context.addon")
    return context.addon.path
