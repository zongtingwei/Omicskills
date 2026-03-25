# Contributing

## Scope

This repository collects reusable omics and computational biology skills.

Good contributions:

- improve an existing leaf skill
- add a missing workflow inside an existing top-level group
- refine package references or validation rules
- merge overlapping subskills into a clearer unit

Avoid:

- adding many new top-level groups
- creating package-only top-level categories
- importing large source libraries without curation
- writing skills that depend on local filesystem layouts outside this repository

## Standard Skill Format

Every leaf skill directory should follow one consistent structure:

```text
skills/<group>/<skill-name>/
├── README.md
├── SKILL.md
└── references/
    └── ...
```

Notes:

- `README.md` is the short human-facing summary.
- `SKILL.md` is the main executable skill instruction file for agents.
- `references/` is optional, but recommended for deeper technical notes, commands, thresholds, datasets, or tool-specific details.
- Nested collections are allowed when needed, but every leaf directory that contains a `SKILL.md` must also contain a `README.md`.

## Writing Guidelines

- prefer workflow-oriented names
- keep instructions portable
- record assumptions and validation steps
- separate core workflow guidance from optional tool references
- keep frontmatter in every `SKILL.md`, including at least `name` and `description`
- write skills so they still make sense outside your own laptop, cloud account, or conda setup

## How To Create A New Skill

1. Choose the most appropriate existing top-level group under `skills/`.
2. Add or update a leaf skill directory instead of creating a new top-level domain unless there is a clear taxonomy gap.
3. Create the leaf directory with this minimum structure:

```text
skills/<group>/<skill-name>/
├── README.md
└── SKILL.md
```

4. Add `references/` only when the workflow needs extra commands, thresholds, API notes, or troubleshooting material.
5. In `README.md`, provide a short summary using the standard sections: `Scope`, `Typical Inputs`, `Typical Outputs`, `Conceptual Seeds`, `Optional Supplements`, and `Main Skill File`.
6. In `SKILL.md`, include frontmatter with at least `name` and `description`, then give portable, step-by-step instructions.
7. Keep relative paths repository-local. Do not reference your own desktop paths, local conda envs, or sibling repos.
8. If the skill depends on external tools, models, APIs, or datasets, state those runtime assumptions clearly in `SKILL.md` or `references/`.

## How To Update An Existing Skill

- preserve the current directory location whenever possible
- improve clarity before adding more depth
- keep repeated tool details in `references/` instead of duplicating them in many skills
- if you rename or split a skill, explain the taxonomy reason in the PR

## Local Validation

Run local validation before opening a PR:

```bash
python3 scripts/validate_skills.py
```

This check verifies that every leaf skill directory has:

- a `SKILL.md`
- a sibling `README.md`
- minimal frontmatter in `SKILL.md`

## Pull Request Expectations

- explain what workflow or gap the contribution covers
- mention which group and leaf skill directories were added or updated
- avoid mixing unrelated restructures with a new skill contribution
- keep the repository readable; if a contribution adds many new skills, include a rationale for the taxonomy change
- if a PR adds a new skill family, describe how it differs from existing nearby skills
