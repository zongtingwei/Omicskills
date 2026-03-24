# BioClaw Protein Design Pack

A BioClaw protein design pack with 22 agent-readable skills for:

- binder design
- sequence design
- structure prediction
- protein design QC
- experimental follow-up planning

Key entry points:

- [Getting started](docs/getting-started.md)
- [Skills](docs/skills.md)
- [Standard pipeline](docs/standard-pipeline.md)

## Install

```
/plugin marketplace add <your-repo-or-local-path>
/plugin install <your-plugin-namespace>
```

## Setup (first time)

→ [Getting started](docs/getting-started.md)

## Skills

→ [View all 22 skills](docs/skills.md)

## Pipeline

→ [Standard pipeline](docs/standard-pipeline.md)

## Quick start

> "Design a binder for PDB 1ALU"

Claude will automatically use the right skills (BoltzGen → Chai → QC).

## Templates and Demo

- [Minimal binder campaign demo](examples/minimal-binder-campaign/README.md)
- [Reusable templates](templates/)
- [Executable QC scorer](scripts/protein_qc_score.py)

## Links

- [Getting started](docs/getting-started.md)
- [Skills](docs/skills.md)
- [Standard pipeline](docs/standard-pipeline.md)
- [Compute setup](docs/compute-setup.md)

## Credits

Built on an earlier protein-design skill foundation “adaptyvbio/protein-design-skills” and substantially revised for BioClaw with renamed skills, new templates, scripts, docs, and workflow structure.

## Contributing

To add a new skill, create a new folder under `skills/` with a `SKILL.md`
file, keep cross-skill references explicit, and add any reusable starter files
to `templates/` or `scripts/` when they improve reproducibility.

Preferred structure:

```text
skills/<skill-name>/
└── SKILL.md
```

Optional additions:

```text
skills/<skill-name>/
├── SKILL.md
├── references/
├── examples/
└── scripts/
```

Use clear names, plain-English descriptions, explicit inputs and outputs, and
direct next-step handoffs to related skills.

## License

MIT

## References

- [biomodals](https://github.com/hgbrian/biomodals) - Modal execution wrappers
- [Anthropic Skills](https://github.com/anthropics/skills) - Skills specification
