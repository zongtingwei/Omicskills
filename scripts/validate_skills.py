from __future__ import annotations

from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"


def skill_dirs() -> list[Path]:
    return sorted({path.parent for path in SKILLS_ROOT.rglob("SKILL.md")})


def has_minimal_frontmatter(text: str) -> bool:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not match:
        return False
    block = match.group(1)
    return "name:" in block and "description:" in block


def main() -> int:
    dirs = skill_dirs()
    if not dirs:
        print("No SKILL.md files found under skills/", file=sys.stderr)
        return 1

    missing_readme: list[str] = []
    bad_frontmatter: list[str] = []

    for directory in dirs:
        skill_file = directory / "SKILL.md"
        readme_file = directory / "README.md"
        if not readme_file.is_file():
            missing_readme.append(str(directory.relative_to(ROOT)))

        if not has_minimal_frontmatter(skill_file.read_text(encoding="utf-8", errors="ignore")):
            bad_frontmatter.append(str(skill_file.relative_to(ROOT)))

    print(f"Validated {len(dirs)} skill directories.")

    if missing_readme:
        print("\nMissing README.md in the following skill directories:", file=sys.stderr)
        for item in missing_readme:
            print(f"- {item}", file=sys.stderr)

    if bad_frontmatter:
        print("\nInvalid or incomplete frontmatter in the following SKILL.md files:", file=sys.stderr)
        for item in bad_frontmatter:
            print(f"- {item}", file=sys.stderr)

    return 1 if missing_readme or bad_frontmatter else 0


if __name__ == "__main__":
    raise SystemExit(main())
