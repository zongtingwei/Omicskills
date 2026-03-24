#!/usr/bin/env python3
"""Add standardized interface sections to protein design skills."""

from __future__ import annotations

from pathlib import Path


REPO_ROOT = Path("/Users/xmingyang/Desktop/BioClaw/protein-design-skills")
SKILLS_DIR = REPO_ROOT / "skills"


SECTION_MAP = {
    "alphafold2-multimer": {
        "inputs": [
            "One or more protein sequences in FASTA format, optionally grouped as a complex.",
            "Optional template structures, MSA settings, and recycle count overrides.",
            "A prediction workspace with enough disk for intermediate features and outputs.",
        ],
        "outputs": [
            "Predicted structure files such as PDB/mmCIF plus per-model confidence JSON or PKL files.",
            "Model-level confidence metrics including pLDDT, pTM, ipTM, and PAE matrices.",
            "A ranked prediction set ready for `protein-design-qc` filtering or `ipsae` ranking.",
        ],
        "next": "Run `protein-design-qc` to filter low-confidence models, then use `ipsae` when ranking binders for experiments.",
    },
    "bindcraft": {
        "inputs": [
            "A prepared target structure with confirmed chain IDs and hotspot residues.",
            "Chosen protocol settings such as binder length range, number of trajectories, and design mode.",
            "A compute environment with GPU access plus BindCraft or Modal dependencies installed.",
        ],
        "outputs": [
            "Designed binder backbones and sequences, often paired with AlphaFold validation outputs.",
            "Campaign-level metadata such as pass rates, design counts, and protocol parameters.",
            "Candidate binders ready for `ipsae` ranking and downstream `protein-design-qc` filtering.",
        ],
        "next": "Rank promising designs with `ipsae`, filter with `protein-design-qc`, and move the top set into experimental validation.",
    },
    "binder-design-tool-selection": {
        "inputs": [
            "A design objective such as de novo binder generation, ligand binding, or nanobody optimization.",
            "Target context including structure availability, hotspot knowledge, and diversity requirements.",
            "Compute and timeline constraints that affect tool choice.",
        ],
        "outputs": [
            "A recommended tool choice or tool combination for the target and campaign goal.",
            "A staged workflow covering target preparation, generation, validation, and filtering.",
            "Suggested handoffs into skills such as `pdb`, `boltzgen`, `rfdiffusion`, `chai1-structure-prediction`, and `protein-design-qc`.",
        ],
        "next": "Use `pdb` to prepare the target, then execute the chosen design path with `boltzgen`, `bindcraft`, or `rfdiffusion`.",
    },
    "spr-bli-binding-characterization": {
        "inputs": [
            "Purified binders or crude samples plus a defined target and assay format preference.",
            "Expected affinity range, kinetic questions, and any throughput constraints.",
            "Instrument context such as available SPR chips, BLI tips, and regeneration chemistry.",
        ],
        "outputs": [
            "An assay recommendation such as SPR versus BLI with a justified experimental setup.",
            "Suggested immobilization strategy, concentration series, and troubleshooting checks.",
            "Interpretation guidance for artifacts such as mass transport, rebinding, and non-specific signal.",
        ],
        "next": "Use the recommended assay plan to run validation experiments, then feed the measured binders back into campaign prioritization.",
    },
    "boltz-structure-prediction": {
        "inputs": [
            "Protein or complex sequences, optionally with ligands or cofactors depending on the prediction task.",
            "A chosen Boltz model version, runtime settings, and output directory.",
            "GPU-enabled environment or Modal configuration for prediction runs.",
        ],
        "outputs": [
            "Predicted structures and confidence artifacts for each sampled model.",
            "Confidence metrics suitable for downstream QC, including interface-aware scores on complexes.",
            "A ranked set of validation structures for design triage.",
        ],
        "next": "Filter the resulting predictions with `protein-design-qc` and compare top candidates against `chai1-structure-prediction` or `alphafold2-multimer` when needed.",
    },
    "boltzgen": {
        "inputs": [
            "A YAML design specification describing target chains, binder entities, and binding residues.",
            "Prepared input structures in PDB or mmCIF format with verified chain numbering.",
            "Sampling settings such as protocol, number of designs, and compute budget.",
        ],
        "outputs": [
            "All-atom designed structures that include backbone, sequence, and side-chain packing decisions.",
            "Run metadata describing protocol choices, design counts, and any built-in filters.",
            "Candidate structures ready for validation with `boltz-structure-prediction` or `chai1-structure-prediction` and filtering with `protein-design-qc`.",
        ],
        "next": "Validate successful designs with `chai1-structure-prediction` or `boltz-structure-prediction`, then score and filter them using `protein-design-qc`.",
    },
    "binder-design-campaign-manager": {
        "inputs": [
            "A campaign goal expressed in experimental terms such as binder count, timeline, or target class.",
            "Upstream context including target structure quality, hotspot knowledge, and compute budget.",
            "Observed campaign metrics if the design effort is already in progress.",
        ],
        "outputs": [
            "A concrete campaign plan with tool selection, design counts, and expected funnel sizes.",
            "Health checks on failure modes such as poor pLDDT, weak interfaces, or low diversity.",
            "Prioritized next actions that map into the relevant generation, validation, or QC skills.",
        ],
        "next": "Execute the planned campaign through `binder-design-tool-selection` and `end-to-end-protein-design-workflow`, then revisit this skill when pass rates drift.",
    },
    "cell-free-protein-expression": {
        "inputs": [
            "A protein construct or sequence plus the intended expression objective and desired scale.",
            "Known liabilities such as disulfides, toxicity, membrane association, or aggregation.",
            "Available CFPS system options and readouts for yield or solubility.",
        ],
        "outputs": [
            "A recommended CFPS platform, construct design guidance, and reaction optimization plan.",
            "Troubleshooting suggestions for low yield, precipitation, or inactive product.",
            "An experiment-ready checklist covering template design, additives, and controls.",
        ],
        "next": "Run the recommended expression screen, then pair high-yield constructs with `spr-bli-binding-characterization` or structural validation.",
    },
    "chai1-structure-prediction": {
        "inputs": [
            "Protein sequences or complexes in FASTA format, optionally with ligand or molecular context.",
            "Prediction parameters such as diffusion steps, seeds, and output directory.",
            "A GPU or API-backed runtime configured for Chai inference.",
        ],
        "outputs": [
            "Predicted structures and accompanying confidence metrics for each input sequence or complex.",
            "Model artifacts suitable for extracting pLDDT, ipTM, PAE, and ranking metadata.",
            "A validation set that can flow directly into `protein-design-qc` and `ipsae`.",
        ],
        "next": "Run `protein-design-qc` on the prediction outputs, then use `ipsae` if you need binder-focused ranking.",
    },
    "esm2-sequence-scoring": {
        "inputs": [
            "Protein sequences in FASTA or CSV form for scoring, embedding, or variant analysis.",
            "A selected ESM model size and any layer or batching preferences.",
            "Optional metadata linking each sequence back to a design campaign.",
        ],
        "outputs": [
            "Sequence-level embeddings, pseudo-log-likelihood scores, or mutation effect estimates.",
            "A plausibility signal that can be merged into `protein-design-qc` composite ranking.",
            "Sequence features that support clustering, deduplication, or active-learning loops.",
        ],
        "next": "Merge ESM-derived scores into `protein-design-qc`, then send surviving candidates to `chai1-structure-prediction` or `boltz-structure-prediction` for structure validation.",
    },
    "foldseek": {
        "inputs": [
            "One or more query structures in PDB or mmCIF format.",
            "A chosen database target such as PDB, AFDB, or a local structural collection.",
            "Search settings like sensitivity, output mode, and result count.",
        ],
        "outputs": [
            "Ranked structural hits with alignment statistics and hit annotations.",
            "Evidence about novelty, scaffold reuse, or remote structural homology.",
            "Candidate templates or analogs to inspect with `pdb` or follow up in design decisions.",
        ],
        "next": "Inspect the top structural hits with `pdb`, then use the results to refine scaffold choice or novelty claims.",
    },
    "ipsae": {
        "inputs": [
            "Predicted complex structures with aligned error information and chain assignments.",
            "A set of candidate binders or complexes to compare under a shared ranking rule.",
            "Optional filtering context from `protein-design-qc` to avoid ranking obvious failures.",
        ],
        "outputs": [
            "ipSAE scores and binder-oriented rankings that complement ipTM and raw PAE.",
            "A shortlist of top complex predictions for experimental follow-up.",
            "A binder-ranking table that can be merged with QC or campaign tracking sheets.",
        ],
        "next": "Take the highest-ranked designs into experimental characterization, or merge ipSAE with `protein-design-qc` scores for a combined rank.",
    },
    "ligandmpnn": {
        "inputs": [
            "A protein structure containing the ligand, cofactor, or metal context to design around.",
            "Design masks or residue constraints describing which positions may change.",
            "Sampling settings such as temperature, sequence count, and batch size.",
        ],
        "outputs": [
            "Ligand-aware designed sequences consistent with the provided backbone and pocket context.",
            "Per-design metadata that can be paired with structure validation results.",
            "Sequence candidates ready for `chai1-structure-prediction` or `boltz-structure-prediction` prediction and later `protein-design-qc` filtering.",
        ],
        "next": "Validate designed sequences structurally with `chai1-structure-prediction` or `boltz-structure-prediction`, then filter them using `protein-design-qc`.",
    },
    "pdb": {
        "inputs": [
            "A PDB ID, text query, sequence, or local structure file that needs preparation.",
            "Optional chain IDs, residue windows, or interface regions of interest.",
            "A local workspace for downloaded files and processed structures.",
        ],
        "outputs": [
            "Downloaded structure files, FASTA sequences, and metadata from RCSB.",
            "Prepared subsets such as single chains, trimmed binding regions, or interface residue lists.",
            "Design-ready structural inputs for `boltzgen`, `rfdiffusion`, `bindcraft`, or validation workflows.",
        ],
        "next": "Pass the prepared structure into `binder-design-tool-selection` for tool choice or directly into a generation skill such as `boltzgen` or `rfdiffusion`.",
    },
    "end-to-end-protein-design-workflow": {
        "inputs": [
            "A starting project goal, target structure context, and desired validation depth.",
            "Constraints on compute, turnaround time, and expected throughput.",
            "Optional prior campaign results that should shape the next iteration.",
        ],
        "outputs": [
            "An end-to-end workflow describing target prep, generation, sequence design, validation, and QC.",
            "A practical execution order across the specialized protein design skills.",
            "A shared mental model for where each tool fits in the campaign funnel.",
        ],
        "next": "Start with `pdb` for target preparation, then follow the recommended generation and validation path through the linked skills.",
    },
    "protein-design-qc": {
        "inputs": [
            "A CSV table of design metrics such as pLDDT, ipTM, PAE, scRMSD, and optional ESM or expression fields.",
            "Optional threshold overrides for stricter or more permissive filtering.",
            "A design campaign context so summary pass rates can be interpreted correctly.",
        ],
        "outputs": [
            "Per-design pass or fail annotations across structural, binding, and expression checks.",
            "A composite score and ranked output table suitable for experimental triage.",
            "A campaign summary highlighting which filter stage is removing most candidates.",
        ],
        "next": "Advance the top-ranked designs into `ipsae` or experimental testing, and use the summary to decide whether the generation stage needs adjustment.",
    },
    "proteinmpnn": {
        "inputs": [
            "One or more backbone structures in PDB format prepared for inverse folding.",
            "Optional fixed-position, tied-position, or omit-AA constraints.",
            "Sampling settings including sequence count, temperature, and chain selection.",
        ],
        "outputs": [
            "Designed protein sequences and run metadata for each backbone or chain.",
            "A sequence library ready for structural validation with `chai1-structure-prediction`, `boltz-structure-prediction`, or `alphafold2-multimer`.",
            "Intermediate campaign artifacts that can be merged into QC and ranking workflows.",
        ],
        "next": "Run structure prediction on the designed sequences, then filter the predicted results with `protein-design-qc`.",
    },
    "rfdiffusion": {
        "inputs": [
            "A prepared target structure plus contig and hotspot definitions for the design task.",
            "A clear generation objective such as binder design, motif scaffolding, or symmetry.",
            "Sampling settings such as design count, checkpoint choice, and noise scale.",
        ],
        "outputs": [
            "Generated backbone structures that satisfy the requested geometric constraints.",
            "A candidate backbone library for sequence design with `proteinmpnn` or `solublempnn`.",
            "Run metadata needed to reproduce successful generation settings.",
        ],
        "next": "Hand the generated backbones to `proteinmpnn` for sequence design, then validate with structure prediction and `protein-design-qc`.",
    },
    "setup": {
        "inputs": [
            "A fresh environment or a failing runtime with missing dependencies and unclear tooling state.",
            "The tool the user wants to run first, such as BoltzGen, RFdiffusion, or Chai.",
            "Information about whether execution will happen locally or through Modal.",
        ],
        "outputs": [
            "A validated environment checklist covering Modal, biomodals, credentials, and test commands.",
            "A list of missing dependencies or broken paths that must be fixed before design work starts.",
            "A known-good starting point for the rest of the skill library.",
        ],
        "next": "After setup passes, move into `pdb` for target preparation or directly into the first design skill you plan to run.",
    },
    "solublempnn": {
        "inputs": [
            "Backbone structures that need sequence design with a stronger solubility bias.",
            "Optional residue constraints and the desired number of redesigned sequences.",
            "Sampling settings and hardware context for batch inference.",
        ],
        "outputs": [
            "Solubility-optimized designed sequences for each provided backbone.",
            "Sequence libraries suitable for structure validation and expression-focused triage.",
            "Candidates that can be compared against standard ProteinMPNN outputs in downstream QC.",
        ],
        "next": "Validate the sequences structurally and compare them against standard `proteinmpnn` outputs using `protein-design-qc` and expression screens.",
    },
    "uniprot": {
        "inputs": [
            "A UniProt accession, gene symbol, organism filter, or annotation query.",
            "Optional fields such as sequence, domains, variants, or cross-references to retrieve.",
            "A workspace for storing FASTA files, JSON results, or curated notes.",
        ],
        "outputs": [
            "Protein sequences, annotations, domain boundaries, and linked database identifiers.",
            "Cross-references that help bridge between sequence records and structures in `pdb`.",
            "Target context useful for construct design, hotspot selection, and sequence analysis.",
        ],
        "next": "Use the retrieved sequence context with `pdb`, `esm2-sequence-scoring`, or downstream design skills depending on whether you need structure, scoring, or generation.",
    },
}


def make_section(info: dict[str, object]) -> str:
    lines = [
        "## Inputs",
        "",
    ]
    for item in info["inputs"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Outputs", ""])
    for item in info["outputs"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Next Step", "", info["next"], ""])
    return "\n".join(lines)


def strip_existing_interface_section(text: str) -> str:
    marker = "\n## Inputs\n"
    idx = text.find(marker)
    if idx != -1:
        return text[:idx].rstrip() + "\n"
    return text.rstrip() + "\n"


def main() -> None:
    for skill_dir in sorted(SKILLS_DIR.iterdir()):
        if not skill_dir.is_dir() or skill_dir.name.startswith("_"):
            continue
        skill_name = skill_dir.name
        skill_file = skill_dir / "SKILL.md"
        if skill_name not in SECTION_MAP or not skill_file.exists():
            continue
        original = skill_file.read_text()
        updated = strip_existing_interface_section(original) + "\n" + make_section(SECTION_MAP[skill_name])
        skill_file.write_text(updated)


if __name__ == "__main__":
    main()
