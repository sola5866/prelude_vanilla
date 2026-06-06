"""成果物名の衝突を確認する Release Rule。"""

from __future__ import annotations

from tools.shared.addons import discover_addons
from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus


class ArtifactNameCollisionRule:
    """version を含む成果物名が大小文字を無視して一意であることを検証する。"""

    rule_id = "artifact_name_collision"
    category = "release"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """<addon_name>_<version>.mcpack の衝突有無を確認して結果を返す。"""

        addons_root = get_addons_root(context)
        version = get_version(context)
        addons = discover_addons(addons_root)
        artifact_names = [f"{addon.name}_{version}.mcpack" for addon in addons]
        collisions = collect_casefold_collisions(artifact_names)

        if not collisions:
            return [
                RuleResult(
                    rule_id=self.rule_id,
                    category=self.category,
                    status=ValidationStatus.PASSED,
                    target=f"{addons_root}@{version}",
                    message=None,
                )
            ]

        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.FAILED,
                target=f"{addons_root}@{version}",
                message=f"成果物名が衝突します: {', '.join(collisions)}",
            )
        ]


def get_addons_root(context: ValidationContext):
    """ValidationContext から addons ルートを取得する。"""

    if context.addons_root is None:
        raise ValueError("Release validation requires context.addons_root")
    return context.addons_root


def get_version(context: ValidationContext) -> str:
    """ValidationContext から release 対象 version を取得する。"""

    if context.version is None or not context.version.strip():
        raise ValueError("Release validation requires context.version")
    return context.version


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
