"""Build deterministic, installable Skill zip artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

FIXED_TIME = (1980, 1, 1, 0, 0, 0)

SYSTEM_RUNTIME_DEPENDENCIES = {
    "bazi": ("bazi",),
    "iching": ("iching",),
    "lenormand": ("lenormand",),
    "liuyao": ("liuyao", "bazi", "iching"),
    "numerology": ("numerology",),
    "qimen": ("qimen", "bazi"),
    "runes": ("runes",),
    "tarot": ("tarot",),
    "western_astrology": ("western_astrology",),
    "ziwei": ("ziwei",),
}

SYSTEM_SHARED_MODULES = {
    "bazi": ("__init__.py", "rules.py", "solar_time.py", "time.py"),
    "iching": ("__init__.py",),
    "lenormand": ("__init__.py", "auditable_draw.py"),
    "liuyao": ("__init__.py", "solar_time.py", "time.py"),
    "numerology": ("__init__.py",),
    "qimen": ("__init__.py", "solar_time.py", "time.py"),
    "runes": ("__init__.py", "auditable_draw.py"),
    "tarot": ("__init__.py",),
    "western_astrology": ("__init__.py", "time.py"),
    "ziwei": ("__init__.py", "solar_time.py", "time.py"),
}

SYSTEM_EXTERNAL_REQUIREMENTS = {
    "bazi": {
        "python_packages": [
            "jsonschema[format]==4.26.0",
            "lunar_python==1.4.8",
            "tzdata==2026.3",
        ]
    },
    "iching": {"python_packages": []},
    "lenormand": {"python_packages": []},
    "liuyao": {"python_packages": ["lunar_python==1.4.8", "tzdata==2026.3"]},
    "numerology": {"python_packages": []},
    "qimen": {"python_packages": ["lunar_python==1.4.8", "tzdata==2026.3"]},
    "runes": {"python_packages": []},
    "tarot": {"python_packages": []},
    "western_astrology": {"python_packages": ["astronomy-engine==2.1.19", "tzdata==2026.3"]},
    "ziwei": {"python_packages": ["lunar_python==1.4.8", "tzdata==2026.3"]},
}

RUNTIME_EXCLUDED_DIRECTORIES = {
    "__pycache__",
    "cases",
    "evaluations",
    "examples",
    "migrations",
    "reviews",
    "skills",
    "tests",
}

RUNTIME_FILE_SUFFIXES = {".json", ".py"}

COMMON_CONTRACT_FILES = (
    "reading-session.schema.json",
    "chart-import.schema.json",
    "confidence-profile.schema.json",
    "timeline.schema.json",
    "comparison.schema.json",
    "report-profile.schema.json",
)


def _write_entry(archive: zipfile.ZipFile, name: str, payload: bytes) -> None:
    info = zipfile.ZipInfo(name, FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, payload)


def _append_content_manifest(target: Path, skill_name: str) -> None:
    with zipfile.ZipFile(target, "r") as archive:
        prefix = f"{skill_name}/"
        files = []
        for name in sorted(archive.namelist()):
            payload = archive.read(name)
            files.append(
                {
                    "path": name.removeprefix(prefix),
                    "size": len(payload),
                    "sha256": hashlib.sha256(payload).hexdigest(),
                }
            )
    manifest = {"format": "divination-skill-content-v1", "files": files}
    with zipfile.ZipFile(target, "a") as archive:
        _write_entry(
            archive,
            f"{skill_name}/CONTENT_MANIFEST.json",
            (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8"),
        )


def _third_party_notices(repo_root: Path, system: str) -> dict[str, Any]:
    return {
        "bundled": [],
        "required_but_not_bundled": SYSTEM_EXTERNAL_REQUIREMENTS[system].get("python_packages", []),
    }


def _excluded_source_manifest(path: Path) -> bool:
    if path.parent.name != "sources" or path.suffix != ".json":
        return False
    try:
        status = json.loads(path.read_text(encoding="utf-8")).get("usage_status")
    except (OSError, json.JSONDecodeError):
        return False
    return status in {"reference_only", "rejected"}


def _runtime_files(repo_root: Path, system: str) -> Iterator[tuple[Path, str]]:
    """Yield the minimal project-authored runtime needed outside the source checkout."""

    systems_init = repo_root / "systems" / "__init__.py"
    yield systems_init, "systems/__init__.py"
    for dependency in SYSTEM_RUNTIME_DEPENDENCIES[system]:
        dependency_dir = repo_root / "systems" / dependency
        for path in sorted(dependency_dir.rglob("*")):
            if not path.is_file() or path.suffix not in RUNTIME_FILE_SUFFIXES:
                continue
            relative = path.relative_to(dependency_dir)
            if RUNTIME_EXCLUDED_DIRECTORIES.intersection(relative.parts):
                continue
            if _excluded_source_manifest(path):
                continue
            yield path, f"systems/{dependency}/{relative.as_posix()}"

    tooling_package = repo_root / "tooling" / "src" / "divination_skills"
    for filename in SYSTEM_SHARED_MODULES[system]:
        yield tooling_package / filename, f"divination_skills/{filename}"
    yield tooling_package / "contracts.py", "divination_skills/contracts.py"

    for path in sorted((repo_root / "catalog" / "sources").glob("*.json")):
        if _excluded_source_manifest(path):
            continue
        yield path, f"catalog/sources/{path.name}"

    for filename in COMMON_CONTRACT_FILES:
        path = repo_root / "common" / "schemas" / filename
        yield path, f"common/schemas/{filename}"
    high_risk_policy = repo_root / "common" / "safety" / "HIGH_RISK_POLICY.md"
    yield high_risk_policy, "common/safety/HIGH_RISK_POLICY.md"


def build_skill_packages(
    repo_root: Path, output_dir: Path, system: str = "bazi"
) -> list[dict[str, Any]]:
    """Build every Skill for one system and return artifact metadata."""

    system_dir = repo_root / "systems" / system
    version = (system_dir / "VERSION").read_text(encoding="utf-8").strip()
    schema_paths = [
        system_dir / "calculator" / "output.schema.json",
        system_dir / "draw" / "output.schema.json",
    ]
    schema_path = next((path for path in schema_paths if path.exists()), None)
    schema = json.loads(schema_path.read_text(encoding="utf-8")) if schema_path else None
    schema_version = schema["properties"]["schema_version"]["const"] if schema else version
    project_license = json.loads(
        (repo_root / "common" / "licensing" / "PROJECT_LICENSE.json").read_text(encoding="utf-8")
    )
    skills_dir = system_dir / "skills"
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = []

    for skill_dir in sorted(path for path in skills_dir.iterdir() if path.is_dir()):
        manifest = {
            "artifact_format": "divination-skill-zip-v1",
            "system": system.replace("_", "-"),
            "skill": skill_dir.name,
            "package_version": version,
            "chart_schema_version": schema_version,
            "runtime": {
                "python_version": ">=3.11",
                "project_systems": list(SYSTEM_RUNTIME_DEPENDENCIES[system]),
                **SYSTEM_EXTERNAL_REQUIREMENTS[system],
            },
            "third_party_notices": "THIRD_PARTY_NOTICES.json",
            "python_requirements": "requirements.txt",
            "project_license_status": project_license["status"],
            "project_license_document": "LICENSE",
            "project_license_notice": "LICENSE_STATUS.md",
            "content_manifest": "CONTENT_MANIFEST.json",
        }
        target = output_dir / f"{skill_dir.name}-{version}.zip"
        with zipfile.ZipFile(target, "w") as archive:
            for path in sorted(skill_dir.rglob("*")):
                if not path.is_file() or "__pycache__" in path.parts:
                    continue
                relative = path.relative_to(skill_dir).as_posix()
                _write_entry(archive, f"{skill_dir.name}/{relative}", path.read_bytes())
            for path, relative in _runtime_files(repo_root, system):
                _write_entry(
                    archive,
                    f"{skill_dir.name}/scripts/{relative}",
                    path.read_bytes(),
                )
            _write_entry(
                archive,
                f"{skill_dir.name}/scripts/verify_package.py",
                (repo_root / "tooling" / "assets" / "verify_package.py").read_bytes(),
            )
            _write_entry(
                archive,
                f"{skill_dir.name}/RUNTIME_REQUIREMENTS.json",
                (json.dumps(manifest["runtime"], indent=2, sort_keys=True) + "\n").encode("utf-8"),
            )
            _write_entry(
                archive,
                f"{skill_dir.name}/requirements.txt",
                (
                    "\n".join(manifest["runtime"]["python_packages"])
                    + ("\n" if manifest["runtime"]["python_packages"] else "")
                ).encode("utf-8"),
            )
            _write_entry(
                archive,
                f"{skill_dir.name}/LICENSE",
                (repo_root / "LICENSE").read_bytes(),
            )
            _write_entry(
                archive,
                f"{skill_dir.name}/LICENSE_STATUS.md",
                (repo_root / "LICENSE_STATUS.md").read_bytes(),
            )
            _write_entry(
                archive,
                f"{skill_dir.name}/PROJECT_LICENSE.json",
                (json.dumps(project_license, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            )
            _write_entry(
                archive,
                f"{skill_dir.name}/THIRD_PARTY_NOTICES.json",
                (
                    json.dumps(_third_party_notices(repo_root, system), indent=2, sort_keys=True)
                    + "\n"
                ).encode("utf-8"),
            )
            _write_entry(
                archive,
                f"{skill_dir.name}/PACKAGE_MANIFEST.json",
                (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode("utf-8"),
            )
        _append_content_manifest(target, skill_dir.name)
        digest = hashlib.sha256(target.read_bytes()).hexdigest()
        target.with_suffix(".zip.sha256").write_text(f"{digest}  {target.name}\n", encoding="ascii")
        artifacts.append({**manifest, "path": str(target), "sha256": digest})
    return artifacts


def build_all_skill_packages(repo_root: Path, output_dir: Path) -> list[dict[str, Any]]:
    """Build every system that contains a Skill source directory."""

    artifacts = []
    systems_dir = repo_root / "systems"
    for system_dir in sorted(path for path in systems_dir.iterdir() if path.is_dir()):
        if (system_dir / "skills").is_dir() and (system_dir / "VERSION").is_file():
            artifacts.extend(build_skill_packages(repo_root, output_dir, system=system_dir.name))
    return artifacts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", default=".", type=Path)
    parser.add_argument("--system", default="bazi")
    parser.add_argument("--output", default=Path("dist"), type=Path)
    parser.add_argument(
        "--release",
        action="store_true",
        help="refuse to build unless every license, review, and sign-off gate is accepted",
    )
    args = parser.parse_args(argv)
    if args.release:
        from divination_skills.readiness import audit_readiness

        readiness = audit_readiness(args.repo.resolve())
        summary = readiness["summary"]
        if summary["release_ready"] != summary["system_count"]:
            print(
                json.dumps(
                    {
                        "error": "release_not_ready",
                        "summary": summary,
                        "systems": [
                            {
                                "system": item["system"],
                                "blocking_reasons": item["blocking_reasons"],
                            }
                            for item in readiness["systems"]
                            if not item["release_ready"]
                        ],
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                file=sys.stderr,
            )
            return 2
    if args.system == "all":
        artifacts = build_all_skill_packages(args.repo.resolve(), args.output.resolve())
    else:
        artifacts = build_skill_packages(args.repo.resolve(), args.output.resolve(), args.system)
    print(json.dumps(artifacts, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
