"""Deterministic helpers for cross-system session and report contracts."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable, Mapping
from copy import deepcopy
from datetime import datetime
from typing import Any

SCHEMA_VERSION = "0.1.0"

PRECISION_RANK = {
    "unknown": 0,
    "date_only": 1,
    "hour_range": 2,
    "minute_range": 3,
    "exact_minute": 4,
}

DEFAULT_MODULE_REQUIREMENTS = {
    "natal.date": "date_only",
    "natal.hour": "hour_range",
    "timing.year": "date_only",
    "timing.month": "hour_range",
    "timing.day": "minute_range",
    "minute_sensitive": "exact_minute",
    "rectification": "hour_range",
}

QUESTION_CATEGORIES = {
    "natal",
    "timing",
    "relationship",
    "career",
    "horary",
    "validation",
    "general",
}


def canonical_json(value: Any) -> bytes:
    """Serialize a JSON-compatible value without platform-dependent whitespace."""

    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def stable_identifier(prefix: str, value: Any) -> str:
    """Build an uppercase, content-addressed identifier without retaining input text."""

    digest = hashlib.sha256(canonical_json(value)).hexdigest()[:16].upper()
    return f"{prefix}-{digest}"


def normalize_question_category(category: str) -> str:
    """Require an explicit supported question category instead of guessing from prose."""

    normalized = category.strip().lower()
    if normalized not in QUESTION_CATEGORIES:
        allowed = ", ".join(sorted(QUESTION_CATEGORIES))
        raise ValueError(f"Unsupported question category {category!r}; choose one of {allowed}.")
    return normalized


def build_confidence_profile(
    *,
    level: str,
    source: str,
    requested_modules: Iterable[str],
    uncertainty_minutes: int | None = None,
    module_requirements: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    """Derive module access from declared input precision using explicit requirements."""

    if level not in PRECISION_RANK:
        raise ValueError(f"Unsupported precision level {level!r}.")
    if source not in {"recorded", "reported", "estimated", "synthetic"}:
        raise ValueError(f"Unsupported precision source {source!r}.")
    if uncertainty_minutes is not None and not 0 <= uncertainty_minutes <= 10080:
        raise ValueError("uncertainty_minutes must be between 0 and 10080.")

    requirements = dict(DEFAULT_MODULE_REQUIREMENTS)
    if module_requirements:
        requirements.update(module_requirements)
    modules = sorted(set(requested_modules))
    if not modules:
        raise ValueError("At least one requested module is required.")

    access: dict[str, str] = {}
    reasons: list[dict[str, str]] = []
    for module in modules:
        required_level = requirements.get(module)
        if required_level is None:
            raise ValueError(f"No precision requirement is registered for module {module!r}.")
        if required_level not in PRECISION_RANK:
            raise ValueError(
                f"Module {module!r} has unsupported precision requirement {required_level!r}."
            )
        difference = PRECISION_RANK[level] - PRECISION_RANK[required_level]
        if difference >= 0:
            access[module] = "allowed"
        elif difference == -1:
            access[module] = "degraded"
            reasons.append(
                {
                    "code": f"precision.degraded.{module}",
                    "message": (
                        f"{module} requires {required_level}; input precision is {level}."
                    ),
                }
            )
        else:
            access[module] = "blocked"
            reasons.append(
                {
                    "code": f"precision.blocked.{module}",
                    "message": (
                        f"{module} requires {required_level}; input precision is {level}."
                    ),
                }
            )

    input_precision: dict[str, Any] = {"level": level, "source": source}
    if uncertainty_minutes is not None:
        input_precision["uncertainty_minutes"] = uncertainty_minutes
    identity_payload = {
        "input_precision": input_precision,
        "module_access": access,
        "reasons": reasons,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "confidence_id": stable_identifier("CONFIDENCE", identity_payload),
        "input_precision": input_precision,
        "module_access": access,
        "disabled_modules": [
            module for module, module_access in access.items() if module_access == "blocked"
        ],
        "reasons": reasons,
    }


def build_reading_session(
    *,
    data_classification: str,
    question_category: str,
    question_text: str,
    chart_refs: list[dict[str, Any]],
    confidence_profile_ref: str | None = None,
    purpose: str = "ephemeral_reading",
    persistence: bool = False,
    third_party_data: str = "none",
    consent_record: str | None = None,
    retention_days: int = 0,
    status: str = "ready",
) -> dict[str, Any]:
    """Create a deterministic session envelope with privacy-safe defaults."""

    if data_classification not in {"synthetic", "public", "consented_private"}:
        raise ValueError(f"Unsupported data classification {data_classification!r}.")
    category = normalize_question_category(question_category)
    text = question_text.strip()
    if not text:
        raise ValueError("question_text must not be empty.")
    if not chart_refs:
        raise ValueError("At least one chart reference is required.")
    if purpose not in {"ephemeral_reading", "saved_reading", "expert_review"}:
        raise ValueError(f"Unsupported purpose {purpose!r}.")
    if purpose == "ephemeral_reading" and (persistence or retention_days != 0):
        raise ValueError("Ephemeral sessions must not persist and must have zero-day retention.")
    if purpose != "ephemeral_reading":
        if not persistence or retention_days < 1:
            raise ValueError("Saved or reviewed sessions require persistence and retention.")
        if not consent_record:
            raise ValueError("Saved or reviewed sessions require a consent record.")
    if not 0 <= retention_days <= 30:
        raise ValueError("retention_days must be between 0 and 30.")
    if status not in {"draft", "ready", "blocked", "completed"}:
        raise ValueError(f"Unsupported session status {status!r}.")

    consent: dict[str, Any] = {
        "purpose": purpose,
        "persistence": persistence,
        "third_party_data": third_party_data,
    }
    if consent_record:
        consent["consent_record"] = consent_record
    identity_payload: dict[str, Any] = {
        "data_classification": data_classification,
        "question": {"category": category, "text": text},
        "chart_refs": chart_refs,
        "confidence_profile_ref": confidence_profile_ref,
        "consent": consent,
        "privacy": {"log_policy": "redacted", "retention_days": retention_days},
    }
    result = {
        "schema_version": SCHEMA_VERSION,
        "session_id": stable_identifier("SESSION", identity_payload),
        **identity_payload,
        "status": status,
    }
    if confidence_profile_ref is None:
        result.pop("confidence_profile_ref")
    return result


def legacy_chart_reference(
    chart: Mapping[str, Any],
    *,
    system: str,
    role: str = "primary",
) -> dict[str, str]:
    """Wrap an existing v0.1 chart without changing or retaining its normalized input."""

    facts = chart.get("computed_facts")
    if not isinstance(facts, Mapping):
        raise ValueError("Legacy chart must contain computed_facts.")
    validation = chart.get("validation", {})
    old_status = validation.get("status") if isinstance(validation, Mapping) else None
    validation_status = "valid" if old_status == "valid" else "unvalidated"
    chart_hash = stable_identifier("CHART", {"system": system, "computed_facts": facts})
    return {
        "chart_id": chart_hash,
        "system": system,
        "role": role,
        "validation_status": validation_status,
    }


def redact_session_for_log(session: Mapping[str, Any]) -> dict[str, Any]:
    """Return operational metadata without question text, chart IDs, or consent records."""

    question = session.get("question", {})
    chart_refs = session.get("chart_refs", [])
    consent = session.get("consent", {})
    return {
        "schema_version": session.get("schema_version"),
        "session_id": session.get("session_id"),
        "question_category": (
            question.get("category") if isinstance(question, Mapping) else None
        ),
        "systems": sorted(
            {
                item.get("system")
                for item in chart_refs
                if isinstance(item, Mapping) and isinstance(item.get("system"), str)
            }
        ),
        "chart_count": len(chart_refs) if isinstance(chart_refs, list) else 0,
        "persistence": (
            bool(consent.get("persistence")) if isinstance(consent, Mapping) else False
        ),
        "status": session.get("status"),
    }


def validate_timeline_intervals(timeline: Mapping[str, Any]) -> list[str]:
    """Check interval order and duplicate entry IDs beyond JSON Schema constraints."""

    errors: list[str] = []
    seen: set[str] = set()
    for index, entry in enumerate(timeline.get("entries", [])):
        entry_id = entry.get("entry_id")
        if entry_id in seen:
            errors.append(f"entries[{index}] duplicates entry_id {entry_id!r}")
        elif isinstance(entry_id, str):
            seen.add(entry_id)
        try:
            start = datetime.fromisoformat(entry["start"].replace("Z", "+00:00"))
            end = datetime.fromisoformat(entry["end"].replace("Z", "+00:00"))
        except (KeyError, TypeError, ValueError):
            errors.append(f"entries[{index}] has an invalid interval")
            continue
        if end < start:
            errors.append(f"entries[{index}] ends before it starts")
    return errors


def select_report_sections(
    profile: Mapping[str, Any],
    *,
    available_fact_ids: Iterable[str],
    available_rule_ids: Iterable[str],
) -> dict[str, Any]:
    """Select supported report sections and explain every omitted required section."""

    fact_ids = tuple(sorted(set(available_fact_ids)))
    rule_ids = tuple(sorted(set(available_rule_ids)))
    included: list[str] = []
    omitted: list[dict[str, Any]] = []
    for section in profile.get("sections", []):
        fact_prefixes = section.get("required_fact_prefixes", [])
        rule_prefixes = section.get("required_rule_prefixes", [])
        missing_facts = [
            prefix
            for prefix in fact_prefixes
            if not any(item.startswith(prefix) for item in fact_ids)
        ]
        missing_rules = [
            prefix
            for prefix in rule_prefixes
            if not any(item.startswith(prefix) for item in rule_ids)
        ]
        if not missing_facts and not missing_rules:
            included.append(section["section_id"])
            continue
        omitted.append(
            {
                "section_id": section["section_id"],
                "optional": bool(section.get("optional")),
                "missing_fact_prefixes": missing_facts,
                "missing_rule_prefixes": missing_rules,
            }
        )
    return {
        "profile_id": profile.get("profile_id"),
        "included_sections": included,
        "omitted_sections": omitted,
        "ready": all(item["optional"] for item in omitted),
    }


def copy_without_sensitive_input(chart: Mapping[str, Any]) -> dict[str, Any]:
    """Copy a chart while dropping raw and normalized birth inputs for review fixtures."""

    result = deepcopy(dict(chart))
    result.pop("raw_input", None)
    result.pop("normalized_input", None)
    return result
