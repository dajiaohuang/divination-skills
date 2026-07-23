from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import zipfile
from pathlib import Path

from divination_skills.build import build_all_skill_packages, build_skill_packages, main
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
MANIFEST_SCHEMA = json.loads(
    (ROOT / "common/schemas/skill-package-manifest.schema.json").read_text(encoding="utf-8")
)
NOTICES_SCHEMA = json.loads(
    (ROOT / "common/schemas/third-party-notices.schema.json").read_text(encoding="utf-8")
)
CONTENT_SCHEMA = json.loads(
    (ROOT / "common/schemas/skill-content-manifest.schema.json").read_text(encoding="utf-8")
)


def test_bazi_skill_packages_are_complete_and_reproducible(tmp_path: Path) -> None:
    first = build_skill_packages(ROOT, tmp_path / "first")
    second = build_skill_packages(ROOT, tmp_path / "second")
    assert [item["skill"] for item in first] == [
        "bazi-calculator",
        "bazi-core",
        "bazi-validator",
    ]
    assert [item["sha256"] for item in first] == [item["sha256"] for item in second]

    for artifact in first:
        path = Path(artifact["path"])
        assert path.with_suffix(".zip.sha256").exists()
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            prefix = artifact["skill"] + "/"
            assert prefix + "SKILL.md" in names
            manifest = json.loads(archive.read(prefix + "PACKAGE_MANIFEST.json"))
            Draft202012Validator(MANIFEST_SCHEMA).validate(manifest)
            Draft202012Validator(NOTICES_SCHEMA).validate(
                json.loads(archive.read(prefix + "THIRD_PARTY_NOTICES.json"))
            )
            assert manifest["package_version"] == "0.1.0"
            assert manifest["chart_schema_version"] == "0.1.0"
            assert manifest["runtime"]["python_version"] == ">=3.11"
            assert prefix + "RUNTIME_REQUIREMENTS.json" in names
            assert prefix + "requirements.txt" in names
            assert prefix + "LICENSE" in names
            assert prefix + "LICENSE_STATUS.md" in names
            assert prefix + "PROJECT_LICENSE.json" in names
            assert prefix + "CONTENT_MANIFEST.json" in names
            assert prefix + "THIRD_PARTY_NOTICES.json" in names
            assert any(name.startswith(prefix + "scripts/systems/") for name in names)
            requirements = archive.read(prefix + "requirements.txt").decode("utf-8").splitlines()
            assert requirements == manifest["runtime"]["python_packages"]
            project_license = json.loads(archive.read(prefix + "PROJECT_LICENSE.json"))
            assert manifest["project_license_status"] == project_license["status"]
            assert project_license["distribution_allowed"] is True
            content_manifest = json.loads(archive.read(prefix + "CONTENT_MANIFEST.json"))
            Draft202012Validator(CONTENT_SCHEMA).validate(content_manifest)
            expected_names = {
                name.removeprefix(prefix)
                for name in names
                if name != prefix + "CONTENT_MANIFEST.json"
            }
            assert {item["path"] for item in content_manifest["files"]} == expected_names
            for item in content_manifest["files"]:
                payload = archive.read(prefix + item["path"])
                assert item["size"] == len(payload)
                assert item["sha256"] == hashlib.sha256(payload).hexdigest()


def test_m4_systems_build_from_the_same_packager(tmp_path: Path) -> None:
    tarot = build_skill_packages(ROOT, tmp_path / "tarot", "tarot")
    western = build_skill_packages(ROOT, tmp_path / "western", "western_astrology")
    assert [item["skill"] for item in tarot] == ["tarot-core", "tarot-draw"]
    assert [item["skill"] for item in western] == ["western-core", "western-natal"]
    assert {item["system"] for item in tarot} == {"tarot"}
    assert {item["system"] for item in western} == {"western-astrology"}


def test_all_system_skills_build_reproducibly(tmp_path: Path) -> None:
    first = build_all_skill_packages(ROOT, tmp_path / "first")
    second = build_all_skill_packages(ROOT, tmp_path / "second")
    assert len(first) == 14
    assert [item["skill"] for item in first] == [item["skill"] for item in second]
    assert [item["sha256"] for item in first] == [item["sha256"] for item in second]
    assert {item["system"] for item in first} == {
        "bazi",
        "iching",
        "lenormand",
        "liuyao",
        "numerology",
        "qimen",
        "runes",
        "tarot",
        "western-astrology",
        "ziwei",
    }
    for artifact in first:
        with zipfile.ZipFile(artifact["path"]) as archive:
            names = archive.namelist()
            assert all("references/upstream" not in name for name in names)
            assert all("/.git/" not in name and not name.endswith("/.gitmodules") for name in names)


def _run_installed(script: Path, *arguments: str) -> dict:
    completed = subprocess.run(
        [sys.executable, "-I", "-X", "utf8", str(script), *arguments],
        cwd=script.parents[2],
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=False,
        timeout=60,
    )
    assert completed.returncode == 0, completed.stderr or completed.stdout
    return json.loads(completed.stdout)


def test_all_built_skill_scripts_run_outside_the_repository(tmp_path: Path) -> None:
    artifacts = build_all_skill_packages(ROOT, tmp_path / "artifacts")
    install_root = tmp_path / "installed"
    for artifact in artifacts:
        with zipfile.ZipFile(artifact["path"]) as archive:
            archive.extractall(install_root)
        if artifact["skill"] == "bazi-calculator":
            verification = _run_installed(
                install_root / artifact["skill"] / "scripts" / "verify_package.py"
            )
            assert verification == {"status": "verified", "errors": []}

    seed = "0" * 63 + "1"
    bazi_input = tmp_path / "bazi-input.json"
    bazi_input.write_text(
        json.dumps(
            {
                "local_datetime": "2000-01-01T12:00:00",
                "timezone": "UTC",
                "day_boundary": "midnight",
            }
        ),
        encoding="utf-8",
    )
    bazi_chart = _run_installed(
        install_root / "bazi-calculator/scripts/calculate.py", str(bazi_input)
    )
    chart_path = tmp_path / "bazi-chart.json"
    chart_path.write_text(json.dumps(bazi_chart), encoding="utf-8")
    bazi_report = _run_installed(install_root / "bazi-core/scripts/explain.py", str(chart_path))
    bazi_validation = _run_installed(
        install_root / "bazi-validator/scripts/validate_chart.py", str(chart_path)
    )
    assert bazi_report["narrative"]["verified_facts"]
    assert bazi_validation["status"] == "valid"

    iching = _run_installed(install_root / "iching-core/scripts/run.py", "--seed-hex", seed)
    lenormand = _run_installed(
        install_root / "lenormand-core/scripts/run.py",
        "--spread",
        "single",
        "--seed-hex",
        seed,
    )
    liuyao = _run_installed(
        install_root / "liuyao-core/scripts/run.py",
        "--local-datetime",
        "2026-01-05T08:15:00",
        "--timezone",
        "Asia/Shanghai",
        "--seed-hex",
        seed,
    )
    qimen = _run_installed(
        install_root / "qimen-hour/scripts/run.py",
        "--local-datetime",
        "2026-01-06T08:00:00",
        "--timezone",
        "Asia/Shanghai",
    )
    runes = _run_installed(
        install_root / "runes-core/scripts/run.py",
        "--spread",
        "single",
        "--seed-hex",
        seed,
    )
    for report in (iching, lenormand, liuyao, qimen, runes):
        assert report["validation"]["status"] == "valid"

    numerology_input = tmp_path / "numerology-input.json"
    numerology_input.write_text(
        json.dumps({"name": "Arden Vale", "birth_date": "1905-12-10"}),
        encoding="utf-8",
    )
    numerology = _run_installed(
        install_root / "numerology-core/scripts/calculate.py", str(numerology_input)
    )
    assert numerology["validation"]["status"] == "valid"

    tarot_input = tmp_path / "tarot-input.json"
    tarot_input.write_text(
        json.dumps(
            {
                "spread": "single",
                "allow_reversals": True,
                "question": "Synthetic package smoke test",
                "seed_hex": seed,
            }
        ),
        encoding="utf-8",
    )
    tarot_draw = _run_installed(install_root / "tarot-draw/scripts/draw.py", str(tarot_input))
    tarot_path = tmp_path / "tarot-draw.json"
    tarot_path.write_text(json.dumps(tarot_draw), encoding="utf-8")
    tarot_report = _run_installed(install_root / "tarot-core/scripts/explain.py", str(tarot_path))
    assert tarot_report["narrative"]["cards"]

    western_input = tmp_path / "western-input.json"
    western_input.write_text(
        json.dumps(
            {
                "local_datetime": "2000-01-01T12:00:00",
                "timezone": "UTC",
                "latitude": 51.4779,
                "longitude": 0.0,
            }
        ),
        encoding="utf-8",
    )
    western_chart = _run_installed(
        install_root / "western-natal/scripts/calculate.py", str(western_input)
    )
    western_path = tmp_path / "western-chart.json"
    western_path.write_text(json.dumps(western_chart), encoding="utf-8")
    western_report = _run_installed(
        install_root / "western-core/scripts/explain.py", str(western_path)
    )
    assert western_report["narrative"]["placements"]

    ziwei = _run_installed(
        install_root / "ziwei-calculator/scripts/run.py",
        "--local-datetime",
        "2000-01-01T12:00:00",
        "--timezone",
        "UTC",
        "--calculation-gender",
        "male",
    )
    assert len(ziwei["computed_facts"]["palaces"]) == 12


def test_ziwei_package_has_no_iztro_or_node_runtime_dependency(tmp_path: Path) -> None:
    [artifact] = build_skill_packages(ROOT, tmp_path, "ziwei")
    with zipfile.ZipFile(artifact["path"]) as archive:
        prefix = "ziwei-calculator/"
        notices = json.loads(archive.read(prefix + "THIRD_PARTY_NOTICES.json"))
        manifest = json.loads(archive.read(prefix + "PACKAGE_MANIFEST.json"))
        names = archive.namelist()
        assert notices["bundled"] == []
        assert all("iztro" not in name.lower() for name in names)
        assert all(not name.endswith((".mjs", "package.json")) for name in names)
        engine = archive.read(prefix + "scripts/systems/ziwei/engine.py").decode("utf-8")
        assert "import iztro" not in engine
        assert "subprocess" not in engine
        assert "executables" not in manifest["runtime"]
        assert "bundled_packages" not in manifest["runtime"]
        assert manifest["runtime"]["python_packages"] == [
            "lunar_python==1.4.8",
            "tzdata==2026.3",
        ]


def test_release_build_is_refused_while_privacy_and_reviews_are_pending(
    tmp_path: Path, capsys
) -> None:
    result = main(
        [
            str(ROOT),
            "--system",
            "bazi",
            "--output",
            str(tmp_path),
            "--release",
        ]
    )
    assert result == 2
    error = json.loads(capsys.readouterr().err)
    assert error["error"] == "release_not_ready"
    assert error["summary"]["project_license_status"] == "selected"
    assert not list(tmp_path.glob("*.zip"))
