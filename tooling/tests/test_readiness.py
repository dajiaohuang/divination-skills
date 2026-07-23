from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

from divination_skills.readiness import (
    _deployment_privacy_policy_errors,
    _validate_evidence,
    audit_readiness,
)
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[2]


def test_release_signoff_schema_rejects_machine_placeholder_acceptance() -> None:
    schema = json.loads(
        (ROOT / "common/evaluation/release-signoff.schema.json").read_text(encoding="utf-8")
    )
    signoff = json.loads(
        (ROOT / "systems/tarot/reviews/release-signoff.json").read_text(encoding="utf-8")
    )
    changed = copy.deepcopy(signoff)
    changed["signoffs"][0]["status"] = "accepted"
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(changed))
    assert errors


def test_all_systems_are_technically_complete_but_fail_closed() -> None:
    report = audit_readiness(ROOT)
    assert report["summary"] == {
        "system_count": 11,
        "technical_complete": 11,
        "release_ready": 0,
        "project_license_status": "selected",
        "deployment_privacy_status": "undecided",
    }
    assert all(not item["release_ready"] for item in report["systems"])
    assert all(item["domain_review"] == "pending" for item in report["systems"])
    assert all(
        set(item["signoffs"]) == {"domain", "rights", "privacy"} for item in report["systems"]
    )


def test_domain_acceptance_requires_hashed_evidence() -> None:
    schema = json.loads(
        (ROOT / "common/evaluation/domain-review.schema.json").read_text(encoding="utf-8")
    )
    review = json.loads(
        (ROOT / "systems/tarot/reviews/domain-review.json").read_text(encoding="utf-8")
    )
    changed = copy.deepcopy(review)
    changed.update(
        status="accepted",
        reviewer_id="real-reviewer-id",
        reviewed_at="2026-07-23T00:00:00Z",
    )
    for case in changed["case_reviews"]:
        case["decision"] = "accepted"
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(changed))
    assert errors


def test_retained_evidence_hash_is_verified(tmp_path: Path) -> None:
    evidence_path = tmp_path / "review-evidence.txt"
    evidence_path.write_text("reviewed by a real person\n", encoding="utf-8")
    digest = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    evidence = {
        "locator": "review-evidence.txt",
        "sha256": digest,
        "retained_in_repository": True,
    }
    assert _validate_evidence(tmp_path, evidence) == []
    evidence["sha256"] = "0" * 64
    assert _validate_evidence(tmp_path, evidence) == ["evidence hash mismatch: review-evidence.txt"]


def test_selected_project_license_is_complete_and_cannot_disable_distribution() -> None:
    schema = json.loads(
        (ROOT / "common/licensing/project-license.schema.json").read_text(encoding="utf-8")
    )
    decision = json.loads(
        (ROOT / "common/licensing/PROJECT_LICENSE.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(decision)
    assert decision["status"] == "selected"
    assert decision["license_identifier"] == "Apache-2.0"
    changed = copy.deepcopy(decision)
    changed["distribution_allowed"] = False
    assert list(validator.iter_errors(changed))


def test_deployment_privacy_is_fail_closed_and_enforces_stored_data_controls() -> None:
    schema = json.loads(
        (ROOT / "common/deployment/deployment-privacy.schema.json").read_text(encoding="utf-8")
    )
    decision = json.loads(
        (ROOT / "common/deployment/DEPLOYMENT_PRIVACY.json").read_text(encoding="utf-8")
    )
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    validator.validate(decision)

    partial = copy.deepcopy(decision)
    partial["stores"]["birth_data"] = False
    assert list(validator.iter_errors(partial))

    configured = copy.deepcopy(decision)
    configured.update(
        status="configured",
        deployment_id="production",
        purposes=["provide requested readings"],
        minors_policy="not offered to minors",
        incident_contact="privacy@example.invalid",
        decided_by="owner-record-id",
        decided_at="2026-07-23T00:00:00Z",
    )
    configured["stores"] = dict.fromkeys(configured["stores"], True)
    configured["retention_days"] = {"primary": 30, "backups": 30, "logs": 7}
    configured["controls"] = dict.fromkeys(configured["controls"], True)
    configured["user_rights"] = {
        "export_supported": True,
        "deletion_supported": True,
        "deletion_sla_days": 30,
    }
    validator.validate(configured)
    assert _deployment_privacy_policy_errors(configured) == []
    configured["controls"]["log_redaction"] = False
    assert _deployment_privacy_policy_errors(configured) == [
        "stored user data requires controls.log_redaction=true"
    ]
