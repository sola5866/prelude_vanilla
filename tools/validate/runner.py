"""Validation Rule の実行と集計を行う基盤を定義する。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from tools.validate.context import ValidationContext
from tools.validate.results import RuleResult, ValidationReport, ValidationStatus


class ValidationRule(Protocol):
    """Validation Rule が満たすべきインターフェース。"""

    rule_id: str
    category: str

    def validate(self, context: ValidationContext) -> list[RuleResult]:
        """指定されたコンテキストに対して Rule を評価する。"""


@dataclass(slots=True)
class ValidationRunner:
    """複数 Rule を実行して ValidationReport を生成する。"""

    rules: list[ValidationRule]

    def run(self, context: ValidationContext) -> ValidationReport:
        """登録された Rule を順に実行して結果を集約する。"""

        results: list[RuleResult] = []
        for rule in self.rules:
            results.extend(rule.validate(context))
        return build_validation_report(results)


def build_validation_report(results: list[RuleResult]) -> ValidationReport:
    """RuleResult の一覧から ValidationReport を組み立てる。"""

    successful = sum(1 for result in results if result.status is ValidationStatus.PASSED)
    failed = sum(1 for result in results if result.status is ValidationStatus.FAILED)
    return ValidationReport(successful=successful, failed=failed, results=results)
