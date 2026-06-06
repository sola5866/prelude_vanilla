"""アドオン UUID の重複を確認する Repository Rule。"""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path

from tools.shared.addons import Addon, discover_addons
from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationStatus


@dataclass(frozen=True, slots=True)
class UuidUsage:
    """1つの UUID がどこで使われているかを表す。"""

    addon_name: str
    location: str


class AddonUuidUniqueRule:
    """アドオン間で UUID が重複していないことを検証する。"""

    rule_id = "addon_uuid_unique"
    category = "repository"

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """addons 配下の UUID 重複有無を確認して結果を返す。"""

        addons_root = get_addons_root(context)
        addons = discover_addons(addons_root)
        uuid_usage = collect_uuid_usage(addons)
        collisions = {
            uuid: usages
            for uuid, usages in uuid_usage.items()
            if len({usage.addon_name.casefold() for usage in usages}) > 1
        }

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

        messages = [
            format_collision_message(uuid, addon_names)
            for uuid, addon_names in sorted(collisions.items(), key=lambda item: item[0].casefold())
        ]
        return [
            RuleResult(
                rule_id=self.rule_id,
                category=self.category,
                status=ValidationStatus.FAILED,
                target=str(addons_root),
                message="\n".join(messages),
            )
        ]


def get_addons_root(context: ValidationContext) -> Path:
    """ValidationContext から addons ルートを取得する。"""

    if context.addons_root is None:
        raise ValueError("Repository validation requires context.addons_root")
    return context.addons_root


def collect_uuid_usage(addons: list[Addon]) -> dict[str, list[UuidUsage]]:
    """manifest.json から UUID とアドオン名の対応表を構築する。"""

    usage: dict[str, list[UuidUsage]] = {}
    for addon in addons:
        for uuid, location in collect_manifest_uuids(addon.manifest_path):
            usage.setdefault(uuid, []).append(
                UuidUsage(addon_name=addon.name, location=location)
            )
    return usage


def collect_manifest_uuids(manifest_path: Path) -> list[tuple[str, str]]:
    """manifest.json から header.uuid と modules[].uuid を収集する。"""

    with manifest_path.open("r", encoding="utf-8") as file:
        manifest = json.load(file)

    if not isinstance(manifest, dict):
        raise ValueError(f"Manifest root must be an object: {manifest_path}")

    uuids: list[tuple[str, str]] = []

    header = manifest.get("header")
    if isinstance(header, dict):
        header_uuid = header.get("uuid")
        if isinstance(header_uuid, str) and header_uuid.strip():
            uuids.append((header_uuid, "header.uuid"))

    modules = manifest.get("modules")
    if isinstance(modules, list):
        for index, module in enumerate(modules):
            if not isinstance(module, dict):
                continue
            module_uuid = module.get("uuid")
            if isinstance(module_uuid, str) and module_uuid.strip():
                uuids.append((module_uuid, f"modules[{index}].uuid"))

    return uuids


def format_collision_message(uuid: str, usages: list[UuidUsage]) -> str:
    """UUID 衝突内容を人間向けメッセージに整形する。"""

    lines = [f"UUID {uuid} is used by:"]
    for usage in sorted(usages, key=lambda item: (item.addon_name.casefold(), item.location)):
        lines.append(f"- {usage.addon_name} ({usage.location})")
    return "\n".join(lines)
