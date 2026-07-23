"""Build the repository-wide source, rule, case, and Skill traceability report."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

from divination_skills.validation import validate_repository


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain one JSON object")
    return value


def nested_ids(value: Any, key: str) -> set[str]:
    found: set[str] = set()
    if isinstance(value, dict):
        for current_key, nested in value.items():
            if current_key == key and isinstance(nested, list):
                found.update(item for item in nested if isinstance(item, str))
            else:
                found.update(nested_ids(nested, key))
    elif isinstance(value, list):
        for nested in value:
            found.update(nested_ids(nested, key))
    return found


def all_manifests(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    paths = [
        *root.glob("catalog/sources/*.json"),
        *root.glob("systems/*/sources/*.json"),
    ]
    return [(path, load_json(path)) for path in sorted(paths)]


def all_rules(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    return [
        (path, load_json(path))
        for path in sorted(root.glob("systems/*/rules/*.json"))
    ]


def all_cases(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    cases: list[tuple[Path, dict[str, Any]]] = []
    for path in sorted(root.glob("systems/*/tests/**/*.json")):
        document = load_json(path)
        if isinstance(document.get("case_id"), str):
            cases.append((path, document))
    return cases


def build_report(root: Path) -> str:
    issues = validate_repository(root, include_examples=False)
    if issues:
        rendered = "\n".join(str(issue) for issue in issues[:20])
        raise RuntimeError(f"repository validation failed:\n{rendered}")

    systems = sorted(
        path
        for path in (root / "systems").iterdir()
        if path.is_dir() and (path / "skills").is_dir()
    )
    sources = all_manifests(root)
    rules = all_rules(root)
    cases = all_cases(root)
    rules_by_system: dict[str, list[dict[str, Any]]] = defaultdict(list)
    cases_by_system: dict[str, list[dict[str, Any]]] = defaultdict(list)
    source_by_id = {source["source_id"]: source for _, source in sources}
    for _, rule in rules:
        rules_by_system[rule["system"]].append(rule)
    for path, case in cases:
        cases_by_system[path.parts[path.parts.index("systems") + 1].replace("_", "-")].append(case)

    all_case_rule_ids: set[str] = set()
    all_case_source_ids: set[str] = set()
    for _, case in cases:
        all_case_rule_ids.update(case.get("must_match_rules", []))
        all_case_rule_ids.update(nested_ids(case, "rule_ids"))
        all_case_source_ids.update(nested_ids(case, "source_ids"))

    rows = []
    project_only_total = 0
    independent_total = 0
    for system_path in systems:
        system = system_path.name.replace("_", "-")
        system_rules = rules_by_system[system]
        system_sources = [
            source for _, source in sources if system in source.get("systems", [])
        ]
        independent = [
            source
            for source in system_sources
            if source.get("quality", {}).get("independence") == "independent"
        ]
        project_only = 0
        for rule in system_rules:
            referenced = [
                source_by_id[reference["source_id"]]
                for reference in rule.get("sources", [])
            ]
            if referenced and all(
                source.get("quality", {}).get("independence") != "independent"
                for source in referenced
            ):
                project_only += 1
        project_only_total += project_only
        independent_total += len(independent)
        case_rules = {
            rule_id
            for case in cases_by_system[system]
            for rule_id in case.get("must_match_rules", [])
        }
        skills = sum(
            1
            for skill in (system_path / "skills").iterdir()
            if skill.is_dir() and (skill / "SKILL.md").is_file()
        )
        version = (system_path / "VERSION").read_text(encoding="utf-8").strip()
        rows.append(
            "| "
            + " | ".join(
                [
                    system,
                    version,
                    str(len(system_sources)),
                    str(len(independent)),
                    str(len(system_rules)),
                    f"{len(case_rules)}/{len(system_rules)}",
                    str(len(cases_by_system[system])),
                    str(skills),
                    str(project_only),
                ]
            )
            + " |"
        )

    retained = sum(
        source.get("local_snapshot", {}).get("retained") is True
        for _, source in sources
    )
    accepted_rights = sum(
        source.get("rights_review", {}).get("status") == "accepted"
        for _, source in sources
    )
    production_sources = sum(
        source.get("usage_status") == "production" for _, source in sources
    )
    tested_rules = sum(
        rule.get("status") in {"tested", "production"}
        and bool(rule.get("tests"))
        and bool(rule.get("sources"))
        for _, rule in rules
    )
    skill_total = sum(int(row.rsplit("|", 3)[1].strip()) for row in rows)

    return "\n".join(
        [
            "# 全仓资料与规则追溯审计",
            "",
            "> 本报告由 `tooling/scripts/build_traceability_report.py` 从仓库当前状态生成。",
            "> “通过”只表示工程链路完整，不表示占卜主张获得科学验证或专家验收。",
            "",
            "## 审计结论",
            "",
            f"- 体系：{len(systems)}",
            f"- Skill：{skill_total}",
            f"- 已登记来源：{len(sources)}；Markdown 快照：{retained}/{len(sources)}",
            (
                f"- 已完成权利审查：{accepted_rights}/{len(sources)}；"
                f"生产可用来源：{production_sources}"
            ),
            (
                f"- 结构化规则：{len(rules)}；具备来源与测试的 tested/production 规则："
                f"{tested_rules}/{len(rules)}"
            ),
            f"- 全部案例记录：{len(cases)}；案例中可解析的规则 ID：{len(all_case_rule_ids)}",
            f"- 案例输出中可解析的来源 ID：{len(all_case_source_ids)}",
            "- 交叉引用、来源体系范围、快照 SHA-256、Rule→Case 声明与输出 trace ID：通过",
            "",
            "## 分体系盘点",
            "",
            (
                "| 体系 | 版本 | 来源 | 独立来源 | 规则 | 案例覆盖规则 | "
                "案例记录 | Skill | 仅项目来源规则 |"
            ),
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
            *rows,
            "",
            "“独立来源”按来源清单中的 `quality.independence=independent` 计数；",
            "“仅项目来源规则”通常是确定性随机流、报告结构、安全边界或尚待专家校订的项目策略，",
            "不能被描述成古典共识。",
            "",
            "## 审计门槛",
            "",
            "当前自动门槛同时要求：",
            "",
            "1. 每个来源有登记清单、权利状态、可跟踪 Markdown 快照和 SHA-256；",
            "2. 每条规则只引用已登记且声明适用该体系的来源；",
            "3. 每条规则声明测试案例；案例另行声明主执行路径必须命中的 `must_match_rules`；",
            "4. 案例计算结果中的 `rule_ids` 与 `source_ids` 全部存在且体系范围匹配；",
            "5. 所有体系提供相同的范围、流派、数据契约、争议、限制、版本和 Skill 包表面。",
            "",
            "## 尚未由自动化解决的风险",
            "",
            (
                f"- 仍有 {project_only_total} 条规则只有项目派生来源；"
                "这些规则必须继续明确标注为项目策略。"
            ),
            (
                f"- 独立来源按体系重复计数为 {independent_total}；"
                "“独立”不等于“权威一致”，流派差异仍应隔离。"
            ),
            "- 历史文本的版本校勘、术语语义和实践接受度仍需具名领域审阅者签署。",
            "- 自动差分只能证明与指定参考实现一致，不能证明参考实现本身没有错误。",
            "- 确定性测试证明可复现与契约稳定，不证明占卜结果具有经验预测效度。",
            "",
            "## 重建",
            "",
            "```powershell",
            ".venv\\Scripts\\python.exe tooling/scripts/build_reference_library.py --check",
            ".venv\\Scripts\\python.exe tooling/scripts/build_traceability_report.py . --check",
            ".venv\\Scripts\\python.exe -m divination_skills.validation . --no-examples",
            "```",
            "",
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", default=".", type=Path)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/AUDIT_REPORT.md"),
    )
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    output = args.output if args.output.is_absolute() else root / args.output
    rendered = build_report(root)
    if args.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != rendered:
            print(f"{output.relative_to(root).as_posix()} is stale.")
            return 1
        print("Traceability report is current.")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(f"Wrote {output.relative_to(root).as_posix()}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
