"""Audit technical completeness and real per-system release approvals."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from divination_skills.validation import validate_system_completeness

REQUIRED_ROLES = {"domain", "rights", "privacy"}


def _count_json(path: Path) -> int:
    return len(list(path.glob("*.json"))) if path.is_dir() else 0


def _validate_evidence(root: Path, evidence: dict[str, Any]) -> list[str]:
    """Verify retained evidence bytes and reject paths outside the repository."""

    if not evidence.get("retained_in_repository"):
        return []
    locator = evidence.get("locator")
    if not isinstance(locator, str):
        return ["retained evidence requires a string locator"]
    path = (root / locator).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return [f"evidence locator escapes repository: {locator}"]
    if not path.is_file():
        return [f"retained evidence file is missing: {locator}"]
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != evidence.get("sha256"):
        return [f"evidence hash mismatch: {locator}"]
    return []


def _system_directories(root: Path) -> list[Path]:
    systems = root / "systems"
    if not systems.is_dir():
        return []
    return sorted(
        path for path in systems.iterdir() if path.is_dir() and (path / "skills").is_dir()
    )


def _load_project_license(root: Path) -> tuple[str, list[str]]:
    path = root / "common" / "licensing" / "PROJECT_LICENSE.json"
    schema_path = root / "common" / "licensing" / "project-license.schema.json"
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return "invalid", [f"could not load project license decision: {exc}"]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in validator.iter_errors(document)]
    status = document.get("status", "invalid")
    if status == "selected":
        locator = document.get("license_document")
        license_path = (root / locator).resolve() if isinstance(locator, str) else None
        try:
            if license_path is not None:
                license_path.relative_to(root.resolve())
        except ValueError:
            errors.append("license_document escapes repository")
        else:
            if license_path is None or not license_path.is_file():
                errors.append("selected project license document is missing")
    return status, errors


def _deployment_privacy_policy_errors(document: dict[str, Any]) -> list[str]:
    """Apply release policy that is stricter than the configuration schema."""

    if document.get("status") != "configured":
        return []
    errors: list[str] = []
    stores = document.get("stores", {})
    retains_user_data = any(value is True for value in stores.values())
    retention = document.get("retention_days", {})
    if not retains_user_data:
        for location in ("primary", "backups"):
            if retention.get(location) != 0:
                errors.append(f"non-storing deployments require retention_days.{location}=0")
        return errors

    controls = document.get("controls", {})
    for control in (
        "encryption_at_rest",
        "encryption_in_transit",
        "role_based_access",
        "log_redaction",
    ):
        if controls.get(control) is not True:
            errors.append(f"stored user data requires controls.{control}=true")
    rights = document.get("user_rights", {})
    for right in ("export_supported", "deletion_supported"):
        if rights.get(right) is not True:
            errors.append(f"stored user data requires user_rights.{right}=true")
    return errors


def _load_deployment_privacy(root: Path) -> tuple[str, list[str]]:
    path = root / "common" / "deployment" / "DEPLOYMENT_PRIVACY.json"
    schema_path = root / "common" / "deployment" / "deployment-privacy.schema.json"
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return "invalid", [f"could not load deployment privacy decision: {exc}"]
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in validator.iter_errors(document)]
    errors.extend(_deployment_privacy_policy_errors(document))
    return document.get("status", "invalid"), errors


def _load_signoff(root: Path, system: Path) -> tuple[dict[str, Any] | None, list[str]]:
    path = system / "reviews" / "release-signoff.json"
    schema_path = root / "common" / "evaluation" / "release-signoff.schema.json"
    if not path.is_file():
        return None, ["missing release-signoff.json"]
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return None, [f"could not load sign-off: {exc}"]

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in validator.iter_errors(document)]
    roles = [item.get("role") for item in document.get("signoffs", [])]
    if set(roles) != REQUIRED_ROLES or len(roles) != len(REQUIRED_ROLES):
        errors.append("signoffs must contain each required role exactly once")
    if document.get("system") != system.name:
        errors.append(f"system must equal directory name {system.name!r}")
    version_path = system / "VERSION"
    if (
        version_path.is_file()
        and document.get("release") != version_path.read_text(encoding="utf-8").strip()
    ):
        errors.append("release must match VERSION")
    for item in document.get("signoffs", []):
        if item.get("status") != "accepted":
            continue
        for evidence in item.get("evidence", []):
            if isinstance(evidence, dict):
                errors.extend(
                    f"{item.get('role')}: {message}"
                    for message in _validate_evidence(root, evidence)
                )
    return document, errors


def _load_domain_review(root: Path, system: Path) -> tuple[str, list[str]]:
    if system.name == "bazi":
        candidates = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in sorted((system / "evaluations" / "expert_candidates").glob("*.json"))
        ]
        accepted = sum(
            item["review"]["status"] == "reviewed" and item["review"]["decision"] == "accepted"
            for item in candidates
        )
        return ("accepted" if candidates and accepted == len(candidates) else "pending"), []

    path = system / "reviews" / "domain-review.json"
    schema_path = root / "common" / "evaluation" / "domain-review.schema.json"
    if not path.is_file():
        return "missing", ["missing domain-review.json"]
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        return "invalid", [f"could not load domain review: {exc}"]

    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = [error.message for error in validator.iter_errors(document)]
    case_ids = [item.get("case_id") for item in document.get("case_reviews", [])]
    expected_ids = []
    for relative in ("tests/golden", "tests/edge_cases", "tests/disputes"):
        for case_path in sorted((system / relative).glob("*.json")):
            expected_ids.append(json.loads(case_path.read_text(encoding="utf-8"))["case_id"])
    if len(case_ids) != len(set(case_ids)):
        errors.append("case_reviews must contain unique case IDs")
    if set(case_ids) != set(expected_ids):
        errors.append("case_reviews must cover every Golden, edge, and dispute case")
    if document.get("system") != system.name:
        errors.append(f"system must equal directory name {system.name!r}")
    if document.get("release") != (system / "VERSION").read_text(encoding="utf-8").strip():
        errors.append("release must match VERSION")
    status = document.get("status", "invalid")
    if status == "accepted" and any(
        item.get("decision") != "accepted" for item in document.get("case_reviews", [])
    ):
        errors.append("an accepted domain review requires every case to be accepted")
    if status == "accepted" and isinstance(document.get("evidence"), dict):
        errors.extend(_validate_evidence(root, document["evidence"]))
    return status, errors


def audit_readiness(root: Path) -> dict[str, Any]:
    """Return one deterministic readiness report for every packaged system."""

    root = root.resolve()
    completeness = validate_system_completeness(root)
    project_license, project_license_errors = _load_project_license(root)
    deployment_privacy, deployment_privacy_errors = _load_deployment_privacy(root)
    systems: list[dict[str, Any]] = []
    for system in _system_directories(root):
        prefix = system.relative_to(root).as_posix()
        structural_issues = [
            str(issue) for issue in completeness if issue.path.replace("\\", "/").startswith(prefix)
        ]
        signoff, signoff_errors = _load_signoff(root, system)
        domain_review, domain_review_errors = _load_domain_review(root, system)
        statuses = (
            {
                item["role"]: item["status"]
                for item in signoff.get("signoffs", [])
                if item.get("role") in REQUIRED_ROLES
            }
            if signoff
            else {}
        )
        technical_complete = (
            not structural_issues
            and not signoff_errors
            and not domain_review_errors
            and not project_license_errors
            and not deployment_privacy_errors
        )
        release_ready = (
            technical_complete
            and project_license == "selected"
            and deployment_privacy == "configured"
            and domain_review == "accepted"
            and all(statuses.get(role) == "accepted" for role in REQUIRED_ROLES)
        )
        systems.append(
            {
                "system": system.name,
                "release": (system / "VERSION").read_text(encoding="utf-8").strip()
                if (system / "VERSION").is_file()
                else None,
                "counts": {
                    "sources": _count_json(system / "sources"),
                    "rules": _count_json(system / "rules"),
                    "golden": _count_json(system / "tests" / "golden"),
                    "edge_cases": _count_json(system / "tests" / "edge_cases"),
                    "dispute_cases": _count_json(system / "tests" / "disputes"),
                    "disputes": _count_json(system / "disputes"),
                    "skills": len(
                        [path for path in (system / "skills").iterdir() if path.is_dir()]
                    ),
                },
                "technical_complete": technical_complete,
                "release_ready": release_ready,
                "domain_review": domain_review,
                "signoffs": statuses,
                "blocking_reasons": [
                    *[f"technical:{message}" for message in structural_issues],
                    *[f"signoff_record:{message}" for message in signoff_errors],
                    *[f"domain_review_record:{message}" for message in domain_review_errors],
                    *[f"project_license_record:{message}" for message in project_license_errors],
                    *[
                        f"deployment_privacy_record:{message}"
                        for message in deployment_privacy_errors
                    ],
                    *(
                        []
                        if project_license == "selected"
                        else [f"project_license:{project_license}"]
                    ),
                    *(
                        []
                        if deployment_privacy == "configured"
                        else [f"deployment_privacy:{deployment_privacy}"]
                    ),
                    *([] if domain_review == "accepted" else ["domain_review:pending"]),
                    *[
                        f"signoff:{role}"
                        for role in sorted(REQUIRED_ROLES)
                        if statuses.get(role) != "accepted"
                    ],
                ],
            }
        )

    return {
        "systems": systems,
        "summary": {
            "system_count": len(systems),
            "technical_complete": sum(item["technical_complete"] for item in systems),
            "release_ready": sum(item["release_ready"] for item in systems),
            "project_license_status": project_license,
            "deployment_privacy_status": deployment_privacy,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path("."))
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--require-technical", action="store_true")
    mode.add_argument("--require-ready", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = audit_readiness(args.root)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.require_ready:
        passed = report["summary"]["release_ready"] == report["summary"]["system_count"]
    elif args.require_technical:
        passed = report["summary"]["technical_complete"] == report["summary"]["system_count"]
    else:
        passed = True
    if not passed:
        print("Readiness requirement failed.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
