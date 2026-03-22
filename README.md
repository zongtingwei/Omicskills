# Omics Skills

This repository is a curated skill library for omics and computational biology workflows.

It is designed to be portable:

- no local absolute paths
- no dependence on sibling source repositories
- no assumption that upstream source collections are present at runtime

## Structure

```text
omics-skills/
├── skills/
│   ├── transcriptomics/
│   ├── single-cell-and-spatial/
│   ├── epigenomics-and-regulation/
│   ├── genomics-and-variation/
│   ├── metagenomics-and-microbiome/
│   ├── proteomics-and-metabolomics/
│   ├── multi-omics-and-systems/
│   └── core-bioinformatics/
├── catalog/
├── scripts/
└── .github/workflows/
```

## Positioning

This repo is best described as:

> A curated omics skill library for AI coding agents and computational biology workflows.

## Design Rules

- keep top-level categories small and legible
- group by user-facing workflow, not by every package name
- keep leaf skills actionable and environment-agnostic
- treat package- or database-specific details as optional supplements

## Recommended Usage

- Use the `skills/` tree as the main public skill library.
- Use `catalog/` as the compact map for curation and routing.
- If integrating into BioClaw, expose only a smaller runtime subset rather than every leaf skill.
