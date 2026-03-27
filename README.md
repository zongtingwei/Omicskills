<div align="center">
<img src="assets/bioclaw_logo.jpg" width="300">

# Bioclaw_Skills_Hub

### Official [Bioclaw](https://github.com/Runchuan-BU/BioClaw) Skills Library for Bioinformatics and Omics Workflows

[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

**Bioclaw_Skills_Hub** is a public collection of reusable skills for bioinformatics, omics analysis, and computational biology.

It is organized around real analysis tasks rather than isolated tools, making it easier to browse, reuse, and adapt for AI agents, workflow systems, and research assistants.

[English](README.md) | [简体中文](README.zh-CN.md)

</div>

## Contents

- [Overview](#overview)
- [What You Will Find Here](#what-you-will-find-here)
- [Repository Structure](#repository-structure)
- [Major Domains](#major-domains)
- [What Makes This Repository Useful](#what-makes-this-repository-useful)
- [Project Status](#project-status)
- [How To Use It](#how-to-use-it)
- [Design Principles](#design-principles)
- [License](#license)

## Overview

Bioinformatics workflows are often scattered across many small prompt collections, tool-specific notes, and one-off agent instructions.

**Bioclaw_Skills_Hub** brings those patterns together into a more consistent repository structure. The goal is to provide a skill library that is easier to curate, easier to route, and easier to reuse across different omics settings, including transcriptomics, single-cell analysis, epigenomics, metagenomics, proteomics, structural biology, and general bioinformatics.

## What You Will Find Here

- task-focused skills for common omics workflows
- a taxonomy that groups skills by major analysis domain
- deeper references for high-value workflows such as ChIP-seq, ATAC-seq, differential expression, metagenomics, proteomics, structural biology, and single-cell analysis
- a foundation for building smaller runtime packs for agent systems such as BioClaw

## Repository Structure

```text
Bioclaw_Skills_Hub/
├── skills/
│   ├── transcriptomics/
│   ├── single-cell-and-spatial/
│   ├── epigenomics-and-regulation/
│   ├── genomics-and-variation/
│   ├── metagenomics-and-microbiome/
│   ├── proteomics-and-metabolomics/
│   ├── multi-omics-and-systems/
│   ├── core-bioinformatics/
│   └── .../
├── catalog/
├── scripts/
└── .github/workflows/
```

## Major Domains

- Transcriptomics
- Single-cell and spatial
- Epigenomics and regulation
- Genomics and variation
- Metagenomics and microbiome
- Proteomics and metabolomics
- Multi-omics and systems biology
- Core bioinformatics

## What Makes This Repository Useful

- It reduces duplication across many small skill collections by consolidating them into a clearer omics taxonomy.
- It keeps high-level categories compact while still allowing specialized leaf skills.
- It is suitable both as a standalone public skill library and as a source repository for downstream agent packs.

## Project Status

This repository will continue to be iterated and expanded over time.

If you find it useful, consider giving the project a star.

## Acknowledgements

This repository is inspired by earlier skill collections including [claude-scientific-skills](https://github.com/K-Dense-AI/claude-scientific-skills), [OpenClaw-Medical-Skills](https://github.com/FreedomIntelligence/OpenClaw-Medical-Skills), [claude-for-life-sciences-skills](https://www.anthropic.com/news/claude-for-life-sciences) and [bioSkills](https://github.com/GPTomics/bioSkills).

The current project reorganizes and refines those ideas into a more unified omics-oriented library structure.

## How To Use It

- Browse `skills/` when you want a workflow-oriented entry point.
- Use `catalog/` when you want the compact taxonomy and source mapping.
- Reuse individual leaf skills directly, or curate a smaller subset for a production agent environment.

## Design Principles

- Group skills by user-facing analysis goals, not just package names.
- Keep leaf skills actionable and easy to route.
- Separate broad workflow guidance from deeper technical references.
- Make it easy to derive a smaller, high-signal runtime pack from a larger public library.

## License

This project is released under the [MIT License](LICENSE).
