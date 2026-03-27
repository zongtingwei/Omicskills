#!/usr/bin/env python3
"""
Bioclaw_Skills_Hub Internal Test Pipeline

Minimal test runner that:
1. Counts skills by category
2. Validates file completeness
3. Generates a test report

Reuses existing scripts/validate_skills.py for validation.
"""

from __future__ import annotations

import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
TEST_ROOT = ROOT / "_bioclaw_test"
VALIDATE_SCRIPT = ROOT / "scripts" / "validate_skills.py"
TAXONOMY_PATH = ROOT / "catalog" / "taxonomy.yaml"
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def skill_dirs() -> list[Path]:
    """Return all skill directories that contain a SKILL.md file."""
    return sorted({path.parent for path in SKILLS_ROOT.rglob("SKILL.md")})


def count_skills() -> dict[str, int]:
    """Count SKILL.md files by category."""
    categories = {}
    for category_dir in sorted(SKILLS_ROOT.iterdir()):
        if not category_dir.is_dir():
            continue
        count = len(list(category_dir.rglob("SKILL.md")))
        if count > 0:
            categories[category_dir.name] = count
    return categories


def actual_taxonomy() -> dict[str, list[str]]:
    """Build taxonomy from the current repository structure."""
    groups: dict[str, list[str]] = {}

    for group_dir in sorted(path for path in SKILLS_ROOT.iterdir() if path.is_dir()):
        if group_dir.name == "protein-design":
            nested_root = group_dir / "skills"
            leaves = sorted(
                skill.parent.name
                for skill in nested_root.rglob("SKILL.md")
                if skill.parent.name != "_shared"
            )
        elif (group_dir / "SKILL.md").is_file():
            leaves = [group_dir.name]
        else:
            leaves = sorted(skill.parent.name for skill in group_dir.rglob("SKILL.md"))

        if leaves:
            groups[group_dir.name] = leaves

    return groups


def parse_taxonomy_yaml() -> dict[str, list[str]]:
    """Parse the simple taxonomy YAML structure without external dependencies."""
    groups: dict[str, list[str]] = {}
    current_group: str | None = None
    in_subskills = False

    for raw_line in TAXONOMY_PATH.read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped == "groups:":
            continue

        if line.startswith("  ") and not line.startswith("    ") and line.endswith(":"):
            current_group = stripped[:-1]
            groups[current_group] = []
            in_subskills = False
            continue

        if current_group is None:
            continue

        if stripped == "subskills:":
            in_subskills = True
            continue

        if in_subskills and stripped.startswith("- "):
            groups[current_group].append(stripped[2:])
            continue

        if line.startswith("    description:"):
            in_subskills = False

    return groups


def check_taxonomy_consistency() -> list[str]:
    """Check that taxonomy.yaml matches the current skill layout."""
    expected = parse_taxonomy_yaml()
    actual = actual_taxonomy()
    problems: list[str] = []

    for group, subskills in actual.items():
        if group not in expected:
            problems.append(f"Missing taxonomy group: {group}")
            continue
        if sorted(expected[group]) != sorted(subskills):
            problems.append(
                f"Subskill mismatch in {group}: taxonomy={sorted(expected[group])} actual={sorted(subskills)}"
            )

    for group in expected:
        if group not in actual:
            problems.append(f"Extra taxonomy group not present in skills/: {group}")

    return problems


def normalize_link_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    if " " in target and not target.startswith(("http://", "https://")):
        target = target.split(" ", 1)[0]
    return target


def check_links() -> tuple[list[str], list[str]]:
    """Scan markdown files under skills/ for absolute filesystem paths and broken local links."""
    absolute_path_issues: list[str] = []
    broken_link_issues: list[str] = []

    for markdown_file in sorted(SKILLS_ROOT.rglob("*.md")):
        text = markdown_file.read_text(encoding="utf-8", errors="ignore")
        for match in MARKDOWN_LINK_RE.finditer(text):
            target = normalize_link_target(match.group(1))
            if not target or target.startswith(("#", "http://", "https://", "mailto:", "data:")):
                continue

            clean_target = target.split("#", 1)[0].split("?", 1)[0]
            if not clean_target:
                continue

            if target.startswith("/"):
                absolute_path_issues.append(f"{markdown_file.relative_to(ROOT)} -> {target}")
                continue

            resolved = (markdown_file.parent / clean_target).resolve()
            if not resolved.exists():
                broken_link_issues.append(f"{markdown_file.relative_to(ROOT)} -> {target}")

    return absolute_path_issues, broken_link_issues


def check_references_completeness() -> list[str]:
    """Check that each skill directory contains the expected reference files."""
    problems: list[str] = []

    for directory in skill_dirs():
        refs_dir = directory / "references"
        technical = refs_dir / "technical_reference.md"
        commands = refs_dir / "commands_and_thresholds.md"

        if technical.is_file() and commands.is_file():
            continue

        missing: list[str] = []
        if not technical.is_file():
            missing.append("references/technical_reference.md")
        if not commands.is_file():
            missing.append("references/commands_and_thresholds.md")

        problems.append(f"{directory.relative_to(ROOT)} missing: {', '.join(missing)}")

    return problems


def run_validation() -> tuple[int, str]:
    """Run the existing validate_skills.py script."""
    result = subprocess.run(
        [sys.executable, str(VALIDATE_SCRIPT)],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout + result.stderr


def format_issue_block(issues: list[str], none_message: str) -> str:
    if not issues:
        return f"- ✅ {none_message}\n"
    return "\n".join(f"- ❌ {issue}" for issue in issues) + "\n"


def generate_report(
    categories: dict[str, int],
    validation_output: str,
    validation_code: int,
    taxonomy_issues: list[str],
    absolute_path_issues: list[str],
    broken_link_issues: list[str],
    reference_issues: list[str],
) -> str:
    """Generate a test report in markdown."""
    total_skills = sum(categories.values())
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    overall_passed = not any(
        [
            validation_code != 0,
            taxonomy_issues,
            absolute_path_issues,
            broken_link_issues,
            reference_issues,
        ]
    )

    report = f"""# Bioclaw_Skills_Hub Test Report

**Generated**: {timestamp}
**Total Skills**: {total_skills}
**Overall Status**: {"✅ PASSED" if overall_passed else "❌ FAILED"}

---

## 1. Skill Count by Category

| Category | Count |
|----------|-------|
"""

    for category, count in sorted(categories.items()):
        report += f"| {category} | {count} |\n"

    report += f"""
**Total**: {total_skills} skills

---

## 2. File Validation

**Validation Status**: {"✅ PASSED" if validation_code == 0 else "❌ FAILED"}

### Validation Output

```
{validation_output.strip()}
```

---

## 3. Taxonomy Consistency

**Taxonomy Status**: {"✅ PASSED" if not taxonomy_issues else "❌ FAILED"}

{format_issue_block(taxonomy_issues, "taxonomy entries match the current skill groups and leaf skills").rstrip()}

---

## 4. Link Checks

**Link Status**: {"✅ PASSED" if not absolute_path_issues and not broken_link_issues else "❌ FAILED"}

### Repository-external absolute paths

{format_issue_block(absolute_path_issues, "no repository-external absolute paths found in markdown files under skills/").rstrip()}

### Broken local links

{format_issue_block(broken_link_issues, "no broken local markdown links found under skills/").rstrip()}

---

## 5. References Completeness

**References Status**: {"✅ PASSED" if not reference_issues else "❌ FAILED"}

{format_issue_block(reference_issues, "every skill directory contains both expected reference files").rstrip()}

---

## 6. Summary

"""

    if overall_passed:
        report += "- ✅ All skills passed validation\n"
        report += f"- ✅ {total_skills} SKILL.md files found\n"
        report += "- ✅ Taxonomy matches the current repository structure\n"
        report += "- ✅ No repository-external absolute paths or broken local links were found\n"
        report += "- ✅ All expected reference files are present\n"
    else:
        report += f"- ❌ File validation issues: {1 if validation_code != 0 else 0}\n"
        report += f"- ❌ Taxonomy issues: {len(taxonomy_issues)}\n"
        report += f"- ❌ Absolute path issues: {len(absolute_path_issues)}\n"
        report += f"- ❌ Broken link issues: {len(broken_link_issues)}\n"
        report += f"- ❌ Reference completeness issues: {len(reference_issues)}\n"

    report += f"""
---

## Test Environment

- Script: `_bioclaw_test/run_tests.py`
- Validation: `scripts/validate_skills.py`
- Root: `{ROOT}`

To re-run this test:
```bash
cd {ROOT}
python3 _bioclaw_test/run_tests.py
```
"""

    return report


def main() -> int:
    """Main test pipeline."""
    print("=" * 60)
    print("Bioclaw_Skills_Hub Internal Test Pipeline")
    print("=" * 60)
    print()

    # Step 1: Count skills
    print("Step 1: Counting skills by category...")
    categories = count_skills()
    total = sum(categories.values())
    print(f"  Found {total} skills across {len(categories)} categories")
    print()

    # Step 2: Run validation
    print("Step 2: Running file validation...")
    validation_code, validation_output = run_validation()
    if validation_code == 0:
        print("  ✅ Validation passed")
    else:
        print("  ❌ Validation failed")
    print()

    # Step 3: Check taxonomy consistency
    print("Step 3: Checking taxonomy consistency...")
    taxonomy_issues = check_taxonomy_consistency()
    if not taxonomy_issues:
        print("  ✅ Taxonomy matches current skill structure")
    else:
        print(f"  ❌ Found {len(taxonomy_issues)} taxonomy issues")
    print()

    # Step 4: Scan links
    print("Step 4: Scanning for absolute paths and broken links...")
    absolute_path_issues, broken_link_issues = check_links()
    if not absolute_path_issues and not broken_link_issues:
        print("  ✅ No absolute-path or broken-link issues found")
    else:
        print(
            "  ❌ "
            f"Found {len(absolute_path_issues)} absolute-path issues and "
            f"{len(broken_link_issues)} broken-link issues"
        )
    print()

    # Step 5: Check references completeness
    print("Step 5: Checking references completeness...")
    reference_issues = check_references_completeness()
    if not reference_issues:
        print("  ✅ All expected reference files are present")
    else:
        print(f"  ❌ Found {len(reference_issues)} reference completeness issues")
    print()

    # Step 6: Generate report
    print("Step 6: Generating test report...")
    report = generate_report(
        categories,
        validation_output,
        validation_code,
        taxonomy_issues,
        absolute_path_issues,
        broken_link_issues,
        reference_issues,
    )

    report_path = TEST_ROOT / "test_report.md"
    report_path.write_text(report, encoding="utf-8")
    print(f"  Report saved to: {report_path.relative_to(ROOT)}")
    print()

    # Summary
    overall_failed = any(
        [
            validation_code != 0,
            taxonomy_issues,
            absolute_path_issues,
            broken_link_issues,
            reference_issues,
        ]
    )
    print("=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Total skills: {total}")
    print(f"Overall: {'✅ PASSED' if not overall_failed else '❌ FAILED'}")
    print(f"File validation issues: {0 if validation_code == 0 else 1}")
    print(f"Taxonomy issues: {len(taxonomy_issues)}")
    print(f"Absolute path issues: {len(absolute_path_issues)}")
    print(f"Broken link issues: {len(broken_link_issues)}")
    print(f"Reference issues: {len(reference_issues)}")
    print(f"Report: {report_path.relative_to(ROOT)}")
    print()

    return 1 if overall_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
