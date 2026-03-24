<p align="center">
  <img src="assets/hero_animation.svg" width="560" alt="Protein Design Skills">
</p>

<p align="center">
  <strong>21 agent skills for computational protein design</strong>
</p>

<p align="center">
  <a href="docs/getting-started.md">Getting started</a> •
  <a href="docs/skills.md">Skills</a> •
  <a href="docs/standard-pipeline.md">Pipeline</a>
</p>

---

## Install

```
/plugin marketplace add <your-repo-or-local-path>
/plugin install <your-plugin-namespace>
```

---

## Setup (first time)

<p align="center">
  <img src="assets/setup_steps.svg" width="600" alt="Setup steps">
</p>

→ [Getting started](docs/getting-started.md)

---

## Skills

<p align="center">
  <img src="assets/skill_categories.svg" width="550" alt="Skill categories">
</p>

→ [View all 21 skills](docs/skills.md)

---

## Pipeline

<p align="center">
  <img src="assets/pipeline_flow.svg" width="550" alt="Pipeline flow">
</p>

→ [Standard pipeline](docs/standard-pipeline.md)

---

## Quick start

> "Design a binder for PDB 1ALU"

Claude will automatically use the right skills (BoltzGen → Chai → QC).

## Templates and Demo

- [Minimal binder campaign demo](examples/minimal-binder-campaign/README.md)
- [Reusable templates](templates/)
- [Executable QC scorer](scripts/protein_qc_score.py)

---

## Links

- [Getting started](docs/getting-started.md)
- [Skills](docs/skills.md)
- [Standard pipeline](docs/standard-pipeline.md)
- [Compute setup](docs/compute-setup.md)
- [Contributing](CONTRIBUTING.md)

## Credits

This repository builds on ideas and original materials from
[`adaptyvbio/protein-design-skills`](https://github.com/adaptyvbio/protein-design-skills/tree/main).

The current version is intended for downstream BioClaw-oriented reuse and has
been substantially extended, renamed, reorganized, and supplemented with
additional templates, examples, scripts, and documentation.

This repository should be understood as a derived and expanded skill pack, not
as a direct mirror of the upstream source.

---

## Contributing

### Creating a new skill

The easiest way to create a new skill is with Claude Code:

```
/skill skill-creator
```

This uses [Anthropic's skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) to guide you through the process.

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Downstream reuse

If you package or publish this repository inside another skill hub, keep the
credit section intact and update repository metadata, installation instructions,
and namespace details for the downstream target.

---

## License

MIT

## References

- [biomodals](https://github.com/hgbrian/biomodals) - Modal execution wrappers
- [Anthropic Skills](https://github.com/anthropics/skills) - Skills specification
