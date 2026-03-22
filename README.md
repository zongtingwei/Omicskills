# Omics Skills

Omics Skills is a GitHub repository of reusable skills for bioinformatics, omics analysis, and computational biology.

It is organized around real analysis tasks rather than isolated tools, so the library is easier to browse, reuse, and adapt for AI agents or human-curated workflow systems.

## What You Will Find Here

- task-focused skills for common omics workflows
- a taxonomy that groups skills by major analysis domain
- deeper references for high-value workflows such as ChIP-seq, ATAC-seq, differential expression, metagenomics, proteomics, structural biology, and single-cell analysis
- a foundation for building smaller runtime packs for agent systems such as BioClaw

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

## How To Use It

- Browse `skills/` when you want a workflow-oriented entry point.
- Use `catalog/` when you want the compact taxonomy and source mapping.
- Reuse individual leaf skills directly, or curate a smaller subset for a production agent environment.

## Design Principles

- Group skills by user-facing analysis goals, not just package names.
- Keep leaf skills actionable and easy to route.
- Separate broad workflow guidance from deeper technical references.
- Make it easy to derive a smaller, high-signal runtime pack from a larger public library.
