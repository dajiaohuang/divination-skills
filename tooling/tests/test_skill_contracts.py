from __future__ import annotations

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SKILLS = sorted((ROOT / "systems").glob("*/skills/*/SKILL.md"))
RULE_IDS = {
    json.loads(path.read_text(encoding="utf-8"))["rule_id"]
    for path in (ROOT / "systems").glob("*/rules/*.json")
}
RULE_PATTERN = re.compile(
    r"(?<!SRC-)(?<!DSP-)(?<!CASE-)\b(?:BAZI|WESTERN|ZIWEI|VEDIC|TAROT|"
    r"ICHING|LIUYAO|QIMEN|"
    r"LENORMAND|RUNES|NUMEROLOGY|MULTI)(?:-[A-Z0-9]+)+-\d{3}\b"
)
SOURCE_PATTERN = re.compile(r"\bSRC-[A-Z0-9-]+\b")
SOURCE_IDS = {
    json.loads(path.read_text(encoding="utf-8"))["source_id"]
    for path in [
        *(ROOT / "catalog" / "sources").glob("*.json"),
        *(ROOT / "systems").glob("*/sources/*.json"),
    ]
}


def _frontmatter(text: str) -> dict:
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    assert match is not None
    value = yaml.safe_load(match.group(1))
    assert isinstance(value, dict)
    return value


def _documented_flags(text: str) -> set[str]:
    return set(re.findall(r"(?<![\w])(--[a-z][a-z0-9-]*)", text))


def _parser_flags(skill_dir: Path) -> set[str]:
    flags: set[str] = set()
    for script in (skill_dir / "scripts").glob("*.py"):
        tree = ast.parse(script.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "add_argument"
            ):
                flags.update(
                    argument.value
                    for argument in node.args
                    if isinstance(argument, ast.Constant)
                    and isinstance(argument.value, str)
                    and argument.value.startswith("--")
                )
    return flags


def test_all_skill_metadata_references_rules_and_commands_are_consistent() -> None:
    assert len(SKILLS) == 35
    skill_names = {path.parent.name for path in SKILLS}
    for path in SKILLS:
        skill_dir = path.parent
        text = path.read_text(encoding="utf-8")
        metadata = _frontmatter(text)
        assert metadata["name"] == skill_dir.name
        assert isinstance(metadata["description"], str) and "Use " in metadata["description"]
        assert len(metadata["description"]) <= 1024

        agent_path = skill_dir / "agents" / "openai.yaml"
        agent = yaml.safe_load(agent_path.read_text(encoding="utf-8"))
        assert f"${metadata['name']}" in agent["interface"]["default_prompt"]

        for relative in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            if "://" not in relative:
                assert (skill_dir / relative).is_file(), (path, relative)
        for referenced_skill in re.findall(r"\$([a-z0-9-]+)", text):
            assert referenced_skill in skill_names, (path, referenced_skill)
        for rule_id in RULE_PATTERN.findall(text):
            assert rule_id in RULE_IDS, (path, rule_id)
        assert _documented_flags(text) <= _parser_flags(skill_dir), path


def test_every_skill_script_supports_help_without_input_or_side_effects() -> None:
    scripts = sorted((ROOT / "systems").glob("*/skills/*/scripts/*.py"))
    assert len(scripts) == 35
    environment = os.environ.copy()
    environment["PYTHONPATH"] = os.pathsep.join(
        [str(ROOT), str(ROOT / "tooling" / "src")]
    )
    for script in scripts:
        result = subprocess.run(
            [sys.executable, str(script), "--help"],
            cwd=ROOT,
            env=environment,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
        assert result.returncode == 0, (
            script,
            result.stdout,
            result.stderr,
        )


def test_iching_skill_declares_the_runtime_policy_version() -> None:
    text = (
        ROOT / "systems" / "iching" / "skills" / "iching-core" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "zhu-xi-count-routing-v0.3" in text
    assert "zhu-xi-count-routing-v0.2" not in text


def test_runtime_source_and_rule_ids_resolve_to_manifests() -> None:
    runtime_files = [
        path
        for root in (ROOT / "systems", ROOT / "common")
        for path in root.rglob("*.py")
        if "tests" not in path.parts and "__pycache__" not in path.parts
    ]
    for path in runtime_files:
        text = path.read_text(encoding="utf-8")
        assert set(SOURCE_PATTERN.findall(text)) <= SOURCE_IDS, path
        assert set(RULE_PATTERN.findall(text)) <= RULE_IDS, path
