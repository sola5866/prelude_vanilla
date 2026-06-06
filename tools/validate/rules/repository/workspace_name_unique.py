"""ワークスペース名の重複を確認する Repository Rule。"""

from __future__ import annotations

from tools.shared.addons import discover_addons
from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus


class WorkspaceNameUniqueRule:
    """workspace 名が大小文字を無視して一意であることを検証する。"""

    rule_id = "workspace_name_unique"
    category = "repository"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """build/workspaces/<addon_name> の衝突有無を確認して結果を返す。"""

        addons_root = get_addons_root(context)
        addons = discover_addons(addons_root)
        collisions = collect_casefold_collisions(addon.name for addon in addons)

        if not collisions:
            return [
                RuleResult(
                    rule_id=self.rule_id,
                    category=self.category,
                    status=ValidationStatus.PASSED,
                    target=str(addons_root),
                    message=None,
                )
            ]

        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.FAILED,
                target=str(addons_root),
                message=f"workspace 名が衝突します: {', '.join(collisions)}",
            )
        ]


def get_addons_root(context: ValidationContext):
    """ValidationContext から addons ルートを取得する。"""

    if context.addons_root is None:
        raise ValueError("Repository validation requires context.addons_root")
    return context.addons_root


def collect_casefold_collisions(values) -> list[str]:
    """大小文字を無視して衝突する値を収集する。"""

    seen: dict[str, str] = {}
    collisions: set[str] = set()
    for value in values:
        normalized = value.casefold()
        previous = seen.get(normalized)
        if previous is None:
            seen[normalized] = value
            continue
        collisions.add(previous)
        collisions.add(value)
    return sorted(collisions, key=str.casefold)
