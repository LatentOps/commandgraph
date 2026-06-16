from __future__ import annotations

import re
from dataclasses import dataclass

from . import RISK_SCHEMA_VERSION
from .data import load_risk_rules


RISK_ORDER = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


@dataclass(frozen=True)
class RiskReview:
    decision: str
    risk: str
    reasons: list[str]
    safer_next_step: str | None = None
    matched_rules: list[str] | None = None
    risk_categories: list[str] | None = None

    def as_dict(self) -> dict:
        return {
            "schema_version": RISK_SCHEMA_VERSION,
            "decision": self.decision,
            "risk": self.risk,
            "reasons": self.reasons,
            "safer_next_step": self.safer_next_step,
            "matched_rules": self.matched_rules or [],
            "risk_categories": self.risk_categories or [],
        }


def max_risk(current: str, candidate: str) -> str:
    return candidate if RISK_ORDER[candidate] > RISK_ORDER[current] else current


def decision_for_risk(risk: str) -> str:
    if risk in {"critical"}:
        return "block"
    if risk in {"high", "medium"}:
        return "warn"
    return "allow"


def check_command(command: str) -> RiskReview:
    normalized = command.strip()
    risk = "low"
    reasons: list[str] = []
    safer_next_steps: list[str] = []
    matched_rules: list[str] = []
    risk_categories: list[str] = []

    if not normalized:
        return RiskReview(
            decision="block",
            risk="critical",
            reasons=["empty command cannot be reviewed safely"],
            safer_next_step="Provide the command text before review.",
            matched_rules=["empty_command"],
            risk_categories=["invalid_input"],
        )

    for rule in load_risk_rules():
        pattern = rule["pattern"]
        if re.search(pattern, normalized, flags=re.IGNORECASE):
            rule_risk = rule["risk"]
            risk = max_risk(risk, rule_risk)
            reasons.append(rule["reason"])
            matched_rules.append(rule["id"])
            if rule.get("category"):
                risk_categories.append(rule["category"])
            if rule.get("safer_next_step"):
                safer_next_steps.append(rule["safer_next_step"])

    if not reasons:
        reasons.append("no high-risk command pattern matched")

    return RiskReview(
        decision=decision_for_risk(risk),
        risk=risk,
        reasons=reasons,
        safer_next_step=safer_next_steps[0] if safer_next_steps else None,
        matched_rules=matched_rules,
        risk_categories=sorted(set(risk_categories)),
    )
