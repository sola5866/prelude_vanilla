"""Validation の結果モデルを定義する。"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class ValidationStatus(StrEnum):
    """Validation Rule の実行結果を表す。"""

    PASSED = "passed"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class RuleResult:
    """単一 Rule の評価結果を表す。"""

    rule_id: str
    category: str
    status: ValidationStatus
    target: str
    message: str | None


@dataclass(frozen=True, slots=True)
class ValidationReport:
    """複数 Rule の実行結果を集約したレポート。"""

    successful: int
    failed: int
    results: list[RuleResult]
