# Skills

All 21 skills available in Protein Design Skills.

## Install

```
/plugin marketplace add <your-repo-or-local-path>
/plugin install <your-plugin-namespace>
```

Or install specific categories:

| Command | Skills | Description |
|---------|--------|-------------|
| `/plugin install <your-plugin-namespace>` | 21 | Everything |
| `/plugin install design-tools@<your-plugin-source>` | 10 | BoltzGen, BindCraft, RFdiffusion, ProteinMPNN, Chai, etc. |
| `/plugin install evaluation@<your-plugin-source>` | 2 | protein-design-qc, ipsae |
| `/plugin install utilities@<your-plugin-source>` | 4 | pdb, uniprot, foldseek, setup |
| `/plugin install experimental@<your-plugin-source>` | 2 | cell-free-protein-expression, spr-bli-binding-characterization |
| `/plugin install orchestration@<your-plugin-source>` | 3 | binder-design-tool-selection, end-to-end-protein-design-workflow, binder-design-campaign-manager |

---

## Design tools (10)

| Skill | Purpose |
|-------|---------|
| `boltzgen` | All-atom diffusion (recommended) |
| `bindcraft` | End-to-end binder design |
| `rfdiffusion` | Backbone generation |
| `proteinmpnn` | Inverse folding |
| `ligandmpnn` | Ligand-aware sequence design |
| `solublempnn` | Solubility-optimized design |
| `chai1-structure-prediction` | Chai-1 structure prediction for fast design validation |
| `boltz-structure-prediction` | Boltz-1 / Boltz-2 structure prediction (open-source) |
| `alphafold2-multimer` | AlphaFold2 / Multimer validation and confidence scoring |
| `esm2-sequence-scoring` | ESM2 sequence scoring and embeddings |

## Evaluation (2)

| Skill | Purpose |
|-------|---------|
| `protein-design-qc` | QC, filtering, and ranking for protein designs |
| `ipsae` | ipSAE ranking for binders |

## Utilities (4)

| Skill | Purpose |
|-------|---------|
| `pdb` | Structure retrieval |
| `uniprot` | Sequence lookup |
| `foldseek` | Structure similarity search |
| `setup` | First-time environment setup |

## Experimental (2)

| Skill | Purpose |
|-------|---------|
| `cell-free-protein-expression` | Cell-free expression planning and optimization |
| `spr-bli-binding-characterization` | SPR/BLI assay planning and kinetic troubleshooting |

## Orchestration (3)

| Skill | Purpose |
|-------|---------|
| `binder-design-tool-selection` | Tool selection for binder design workflows |
| `end-to-end-protein-design-workflow` | End-to-end protein design pipeline guide |
| `binder-design-campaign-manager` | Campaign planning, monitoring, and troubleshooting |

---

## Skill details

For detailed usage of each skill, see the individual skill documentation:

- **Design tools**: [BoltzGen](../skills/boltzgen/SKILL.md), [BindCraft](../skills/bindcraft/SKILL.md), [RFdiffusion](../skills/rfdiffusion/SKILL.md), [ProteinMPNN](../skills/proteinmpnn/SKILL.md), [LigandMPNN](../skills/ligandmpnn/SKILL.md), [SolubleMPNN](../skills/solublempnn/SKILL.md), [Chai](../skills/chai1-structure-prediction/SKILL.md), [Boltz](../skills/boltz-structure-prediction/SKILL.md), [AlphaFold](../skills/alphafold2-multimer/SKILL.md), [ESM](../skills/esm2-sequence-scoring/SKILL.md)

- **Evaluation**: [Protein QC](../skills/protein-design-qc/SKILL.md), [ipSAE](../skills/ipsae/SKILL.md)

- **Utilities**: [PDB](../skills/pdb/SKILL.md), [UniProt](../skills/uniprot/SKILL.md), [FoldSeek](../skills/foldseek/SKILL.md), [Setup](../skills/setup/SKILL.md)

- **Experimental**: [Cell-Free Expression](../skills/cell-free-protein-expression/SKILL.md), [Binding Characterization](../skills/spr-bli-binding-characterization/SKILL.md)

- **Orchestration**: [Binder Design](../skills/binder-design-tool-selection/SKILL.md), [Protein Design Workflow](../skills/end-to-end-protein-design-workflow/SKILL.md), [Campaign Manager](../skills/binder-design-campaign-manager/SKILL.md)

---

## See also

- [Getting started](getting-started.md)
- [Standard pipeline](standard-pipeline.md)
- [Compute setup](compute-setup.md)
