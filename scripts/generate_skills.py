from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]

MANUAL_OVERRIDE_PATHS = {
    "skills/single-cell-and-spatial/scrna-preprocessing-clustering",
    "skills/single-cell-and-spatial/cell-annotation",
    "skills/epigenomics-and-regulation/chip-seq",
    "skills/epigenomics-and-regulation/atac-seq",
    "skills/transcriptomics/differential-expression",
    "skills/proteomics-and-metabolomics/proteomics",
    "skills/metagenomics-and-microbiome/metagenomics",
    "skills/proteomics-and-metabolomics/structural-biology",
}


SKILLS = [
    {
        "path": "skills/transcriptomics/bulk-rna-expression",
        "name": "bulk-rna-expression",
        "title": "Bulk RNA Expression",
        "description": "Python-first workflow for bulk RNA-seq expression intake, normalization, sample QC, and downstream-ready matrices.",
        "when": [
            "use when the task is bulk RNA-seq expression profiling before or alongside differential analysis",
            "use when the user has count matrices, transcript abundances, or aligned RNA-seq reads and needs expression summaries",
            "use when sample-level QC, PCA, or normalized matrices are required",
        ],
        "inputs": ["count matrix", "sample metadata", "optional BAM or quantification outputs"],
        "outputs": ["normalized matrix", "sample QC plots", "PCA or clustering summaries"],
        "tools": ["pandas", "numpy", "seaborn", "matplotlib", "scanpy for matrix utilities when appropriate"],
        "steps": [
            ("Validate matrix orientation", "Confirm rows and columns, unique sample IDs, and whether counts are raw integers or already normalized."),
            ("Join metadata", "Check condition labels, replicate structure, batch columns, and missing covariates before analysis."),
            ("Compute sample QC", "Summarize library size, detected genes, missingness, outliers, and replicate similarity."),
            ("Normalize for exploration", "Apply count-aware normalization or variance stabilization appropriate to the downstream method."),
            ("Export analysis-ready data", "Save normalized matrices and QC tables for DE, enrichment, or reporting."),
        ],
        "avoid": [
            "mixing raw counts and normalized values in the same table",
            "running DE directly on TPM values unless the method explicitly supports it",
            "skipping sample metadata validation before modeling",
        ],
        "sources": ["bulk transcriptomics matrix handling patterns", "RNA quantification workflows", "bulk RNA QC and expression summarization patterns"],
        "supplements": ["pydeseq2", "pysam"],
    },
    {
        "path": "skills/transcriptomics/rna-quantification",
        "name": "rna-quantification",
        "title": "RNA Quantification",
        "description": "Workflow for gene and transcript quantification from RNA-seq reads using alignment-based or alignment-free tools.",
        "when": [
            "use when the user needs counts or transcript abundances from FASTQ files",
            "use when the task is featureCounts, salmon, kallisto, or tximport-style quantification",
            "use when quantification outputs need to be prepared for DE or expression reporting",
        ],
        "inputs": ["FASTQ files", "reference genome or transcriptome", "annotation GTF or GFF"],
        "outputs": ["gene counts", "transcript abundances", "quantification QC summaries"],
        "tools": ["salmon", "kallisto", "featureCounts", "tximport-style imports", "pandas"],
        "steps": [
            ("Choose quantification strategy", "Prefer alignment-free quantification for speed and transcript-level abundance, and alignment-based counting when genomic alignment is already available."),
            ("Verify references", "Ensure transcriptome, genome, and annotation versions are consistent before quantification."),
            ("Run quantification", "Capture both abundance tables and tool-specific mapping or assignment rates."),
            ("Aggregate to analysis level", "Convert transcript-level outputs to gene-level summaries only when the downstream task calls for it."),
            ("Prepare outputs", "Standardize sample IDs and produce a count or abundance matrix plus QC metadata."),
        ],
        "avoid": [
            "combining references from different releases",
            "dropping assignment-rate QC when quantification quality is uncertain",
            "using abundance estimates as counts without tracking the distinction",
        ],
        "sources": ["RNA quantification workflows", "alignment-derived counting patterns", "RNA-seq quantification task patterns"],
        "supplements": ["pysam"],
    },
    {
        "path": "skills/transcriptomics/differential-expression",
        "name": "differential-expression",
        "title": "Differential Expression",
        "description": "Python-first differential expression workflow for bulk transcriptomics with design validation, contrasts, result filtering, and visualization.",
        "when": [
            "use when the user asks for DE genes between conditions in bulk transcriptomics data",
            "use when counts and sample metadata are available and the design matrix must be checked",
            "use when volcano plots, ranked genes, and pathway-ready outputs are needed",
        ],
        "inputs": ["raw count matrix", "sample metadata with condition and covariates", "contrast definition"],
        "outputs": ["DE result table", "volcano or MA plots", "ranked genes for enrichment"],
        "tools": ["pydeseq2", "pandas", "numpy", "matplotlib", "seaborn"],
        "steps": [
            ("Validate design", "Check replicate counts, confounded covariates, factor levels, and contrast direction before fitting."),
            ("Fit count-aware model", "Use a method intended for raw counts and include relevant batch or pairing terms."),
            ("Filter and rank results", "Apply effect-size and adjusted-p-value thresholds suited to the biological question."),
            ("Visualize findings", "Generate MA plots, volcano plots, and heatmaps for top genes or pathways."),
            ("Export downstream artifacts", "Save a complete results table plus a ranked gene list for enrichment analysis."),
        ],
        "avoid": [
            "running DE on log-normalized expression instead of raw counts for count-based models",
            "ignoring confounded batches or paired designs",
            "reporting top genes without effect sizes and adjusted p-values",
        ],
        "sources": ["bulk differential expression workflows", "Python count-modeling patterns", "differential-expression task patterns"],
        "supplements": ["pydeseq2"],
    },
    {
        "path": "skills/transcriptomics/alternative-splicing",
        "name": "alternative-splicing",
        "title": "Alternative Splicing",
        "description": "Workflow for event-level and isoform-level splicing analysis with sashimi-ready outputs and splice QC.",
        "when": [
            "use when the task is differential splicing, isoform switching, or splice-aware QC",
            "use when aligned RNA-seq reads and transcript annotations are available",
            "use when the user needs event summaries, PSI-like metrics, or sashimi-style visualization",
        ],
        "inputs": ["aligned RNA-seq reads", "splice junction summaries", "transcript annotation"],
        "outputs": ["event tables", "isoform usage summaries", "sashimi or splice plots"],
        "tools": ["splice-aware quantification tools", "pandas", "matplotlib", "genome track plotting utilities"],
        "steps": [
            ("Confirm splice-aware inputs", "Verify junction extraction, transcript annotation, and sample group definitions."),
            ("Choose analysis level", "Use event-level methods for exon or junction usage and isoform-level methods for transcript switching."),
            ("Quantify splicing changes", "Compute condition-specific splice usage and test for differential splicing."),
            ("Inspect representative loci", "Plot junction-supported events to verify that statistical hits reflect visible changes."),
            ("Export interpretable results", "Save event IDs, effect estimates, significance values, and plot-ready loci."),
        ],
        "avoid": [
            "interpreting isoform changes without read support at informative junctions",
            "mixing event- and transcript-level interpretations without stating which was used",
            "skipping locus-level review of top hits",
        ],
        "sources": ["alternative splicing workflows"],
        "supplements": ["pysam"],
    },
    {
        "path": "skills/transcriptomics/small-rna-seq",
        "name": "small-rna-seq",
        "title": "Small RNA Seq",
        "description": "Workflow for small RNA and miRNA preprocessing, quantification, differential analysis, and target-oriented interpretation.",
        "when": [
            "use when the user has miRNA or other small RNA sequencing data",
            "use when adapter-heavy preprocessing and short-read-specific QC are required",
            "use when the goal is differential miRNA analysis or target prediction follow-up",
        ],
        "inputs": ["small RNA FASTQ files", "adapter sequences", "reference miRNA annotations"],
        "outputs": ["small RNA count matrix", "differential miRNA tables", "target candidate summaries"],
        "tools": ["miRge3", "miRDeep2-style workflows", "pandas", "seaborn"],
        "steps": [
            ("Handle short inserts carefully", "Trim adapters and confirm read-length distributions before quantification."),
            ("Quantify annotated species", "Map or assign reads to miRNAs and other small RNA classes with class-aware counting."),
            ("Perform count-aware comparisons", "Use replicate-aware statistics for differential abundance."),
            ("Review library composition", "Inspect proportions of miRNA, tRNA fragments, rRNA fragments, and other classes."),
            ("Prepare interpretation outputs", "Export mature miRNA results and optional target-prediction inputs."),
        ],
        "avoid": [
            "treating adapter-trimmed and untrimmed samples as comparable",
            "ignoring multi-mapping behavior for short RNAs",
            "reporting targets without clarifying they are predictions",
        ],
        "sources": ["small RNA sequencing workflows", "miRNA-focused analysis patterns"],
        "supplements": [],
    },
    {
        "path": "skills/transcriptomics/ribo-seq",
        "name": "ribo-seq",
        "title": "Ribo Seq",
        "description": "Workflow for ribosome profiling, P-site aware preprocessing, periodicity checks, ORF detection, and translation efficiency analysis.",
        "when": [
            "use when the task is ribosome profiling or translation efficiency analysis",
            "use when matched RNA-seq is available for translation-vs-expression comparisons",
            "use when periodicity and P-site validation are necessary before biological claims",
        ],
        "inputs": ["ribo-seq reads", "optional matched RNA-seq", "transcript annotation"],
        "outputs": ["periodicity metrics", "ORF candidates", "translation efficiency summaries"],
        "tools": ["ribo-seq preprocessing utilities", "pandas", "matplotlib"],
        "steps": [
            ("Validate read quality and offsets", "Establish read-length distributions and P-site offsets before counting footprints."),
            ("Check periodicity", "Confirm expected triplet periodicity and frame enrichment."),
            ("Quantify translation signal", "Compute footprint abundance at transcript or ORF level and compare with matched RNA when available."),
            ("Identify translated features", "Report canonical or novel ORFs with explicit evidence criteria."),
            ("Export clear diagnostics", "Save periodicity plots, TE tables, and prioritized translated features."),
        ],
        "avoid": [
            "making translation claims without periodicity evidence",
            "comparing unmatched RNA and ribo data as if they were paired",
            "ignoring read-length-specific behavior",
        ],
        "sources": ["ribosome profiling workflows"],
        "supplements": [],
    },
    {
        "path": "skills/single-cell-and-spatial/scrna-preprocessing-clustering",
        "name": "scrna-preprocessing-clustering",
        "title": "scRNA Preprocessing And Clustering",
        "description": "Python-first single-cell RNA workflow for QC, normalization, dimensionality reduction, neighborhood graph construction, and clustering.",
        "when": [
            "use when the task is exploratory scRNA-seq preprocessing and clustering",
            "use when the user has AnnData, 10X outputs, or a count matrix and needs UMAP or clusters",
            "use when later annotation or trajectory analysis depends on a well-prepared single-cell object",
        ],
        "inputs": ["AnnData object or count matrix", "cell metadata", "gene annotations"],
        "outputs": ["filtered single-cell object", "UMAP or PCA embeddings", "cluster assignments"],
        "tools": ["scanpy", "anndata", "seaborn", "matplotlib"],
        "steps": [
            ("Assess cell and gene QC", "Filter low-quality cells, low-detection genes, and obvious outliers using dataset-appropriate thresholds."),
            ("Normalize and select features", "Apply normalization, log transform when appropriate, and identify highly variable genes."),
            ("Build neighborhoods and embeddings", "Compute PCA, neighbor graphs, and 2D embeddings such as UMAP."),
            ("Cluster iteratively", "Try a small grid of clustering resolutions and compare cluster stability against marker expression."),
            ("Persist the processed object", "Save embeddings, cluster labels, and QC metrics for downstream annotation or integration."),
        ],
        "avoid": [
            "using a single fixed QC threshold without checking the data distribution",
            "interpreting UMAP structure before verifying batch effects and QC artifacts",
            "discarding raw counts needed for downstream modeling",
        ],
        "sources": ["single-cell preprocessing workflows", "single-cell clustering workflows", "scanpy-style analysis patterns"],
        "supplements": ["anndata", "scanpy"],
    },
    {
        "path": "skills/single-cell-and-spatial/cell-annotation",
        "name": "cell-annotation",
        "title": "Cell Annotation",
        "description": "Workflow for single-cell cell type annotation using marker review, reference mapping, and classifier-based labeling with confidence checks.",
        "when": [
            "use when the user asks to assign cell types to single-cell clusters or cells",
            "use when marker genes, references, or transfer-learning annotations are available",
            "use when automated labels need to be reconciled with manual biology checks",
        ],
        "inputs": ["clustered single-cell object", "marker gene sets", "optional reference atlas"],
        "outputs": ["cell type labels", "cluster marker summaries", "confidence or ambiguity flags"],
        "tools": ["scanpy", "celltypist", "scvi-tools when needed for mapping", "pandas"],
        "steps": [
            ("Review cluster markers first", "Do not rely on automated labels before inspecting marker expression and cluster coherence."),
            ("Choose annotation path", "Use marker-based rules, reference mapping, or classifier-based labeling depending on the dataset and available references."),
            ("Assign confidence-aware labels", "Store confidence scores or ambiguity tags rather than forcing every cell into a label."),
            ("Check consistency", "Compare labels across clusters, conditions, and known marker panels to catch overcalling."),
            ("Export interpretable labels", "Save both raw method outputs and a curated final label column."),
        ],
        "avoid": [
            "accepting transferred labels without checking markers",
            "over-interpreting low-confidence reference matches",
            "erasing uncertainty from ambiguous clusters",
        ],
        "sources": ["single-cell annotation workflows", "reference-based cell labeling patterns", "scanpy-centered single-cell interpretation patterns"],
        "supplements": ["scanpy", "scvi-tools"],
    },
    {
        "path": "skills/single-cell-and-spatial/cell-communication",
        "name": "cell-communication",
        "title": "Cell Communication",
        "description": "Workflow for ligand-receptor communication inference in single-cell or spatial data with sender-receiver summaries and cautious interpretation.",
        "when": [
            "use when the task is cell-cell communication or ligand-receptor analysis",
            "use when the dataset already has reasonable cell type annotations or spatial neighborhoods",
            "use when the user needs network, heatmap, or pathway-style communication outputs",
        ],
        "inputs": ["annotated single-cell or spatial object", "ligand-receptor resource", "group or condition metadata"],
        "outputs": ["interaction tables", "sender-receiver summaries", "communication visualizations"],
        "tools": ["pandas", "networkx", "seaborn", "matplotlib"],
        "steps": [
            ("Confirm annotation quality", "Communication analysis depends on robust cell labels or spatial domains."),
            ("Define comparison units", "Choose whether to infer communication across clusters, cell types, neighborhoods, or conditions."),
            ("Run interaction scoring", "Compute ligand-receptor evidence and apply filtering for expression support and redundancy."),
            ("Aggregate to interpretable views", "Summarize signals by sender, receiver, pathway, or condition."),
            ("Report caveats", "State clearly that inferred communication is hypothesis-generating unless validated experimentally."),
        ],
        "avoid": [
            "running communication analysis on unstable or weak annotations",
            "equating expression correlation with validated signaling",
            "reporting dense uninterpretable networks without summarization",
        ],
        "sources": ["single-cell communication workflows", "spatial communication workflows"],
        "supplements": ["string-database"],
    },
    {
        "path": "skills/single-cell-and-spatial/trajectory-lineage",
        "name": "trajectory-lineage",
        "title": "Trajectory And Lineage",
        "description": "Workflow for pseudotime, lineage branching, and state-transition analysis in single-cell data.",
        "when": [
            "use when the user asks for pseudotime, lineage branching, or developmental progression",
            "use when the single-cell object already has a coherent embedding and annotations",
            "use when dynamic gene programs or branch-specific markers are needed",
        ],
        "inputs": ["processed single-cell object", "cluster labels", "optional time or perturbation metadata"],
        "outputs": ["pseudotime assignments", "branch or lineage states", "dynamic gene programs"],
        "tools": ["scanpy", "scvelo where velocity is available", "matplotlib"],
        "steps": [
            ("Check topology assumptions", "Ensure the embedding and cluster relationships support a trajectory-style interpretation."),
            ("Pick roots and branches carefully", "Use prior biology or metadata to justify start states and branch structure."),
            ("Infer trajectories", "Compute pseudotime or lineage paths and verify they align with marker trends."),
            ("Identify dynamic features", "Report genes or modules that vary along pseudotime or across branches."),
            ("Visualize with context", "Overlay trajectories on embeddings and summarize branch-specific biology."),
        ],
        "avoid": [
            "forcing linear trajectories on clearly disconnected states",
            "setting roots arbitrarily without stating the assumption",
            "claiming lineage causality from static data alone",
        ],
        "sources": ["single-cell trajectory inference workflows", "temporal genomics trajectory modeling", "RNA velocity-style trajectory patterns"],
        "supplements": ["scvelo"],
    },
    {
        "path": "skills/single-cell-and-spatial/multiome-scatac",
        "name": "multiome-scatac",
        "title": "Multiome And scATAC",
        "description": "Workflow for paired or integrated single-cell RNA and ATAC analysis with multimodal latent spaces and regulatory interpretation.",
        "when": [
            "use when the task is scATAC, multiome RNA-ATAC, or multimodal single-cell integration",
            "use when gene activity, motif activity, or regulatory linkage is required",
            "use when the user needs a joint view across modalities rather than separate analyses",
        ],
        "inputs": ["multiome object or paired modalities", "ATAC fragments or peak matrix", "cell metadata"],
        "outputs": ["integrated embeddings", "modality-aware clusters", "motif or regulatory summaries"],
        "tools": ["scanpy", "anndata", "scvi-tools where appropriate", "motif-analysis utilities"],
        "steps": [
            ("QC both modalities", "Evaluate RNA and ATAC quality independently before joint integration."),
            ("Create harmonized features", "Build peak, gene, or gene activity representations consistent across cells."),
            ("Integrate modalities", "Use an approach suited to paired or unpaired multimodal data."),
            ("Interpret regulatory signals", "Relate motif accessibility, gene activity, and expression patterns cautiously."),
            ("Export multimodal state summaries", "Save joint embeddings, modality-specific QC, and regulatory annotations."),
        ],
        "avoid": [
            "treating weak gene activity estimates as direct expression measurements",
            "integrating low-quality modalities without modality-specific QC",
            "reporting regulatory links without stating the evidence type",
        ],
        "sources": ["single-cell multimodal integration workflows", "single-cell ATAC analysis workflows", "ATAC-seq interpretation patterns"],
        "supplements": ["scvi-tools", "anndata"],
    },
    {
        "path": "skills/single-cell-and-spatial/spatial-transcriptomics",
        "name": "spatial-transcriptomics",
        "title": "Spatial Transcriptomics",
        "description": "Workflow for spatial transcriptomics preprocessing, domain detection, deconvolution, neighborhood analysis, and publication-ready maps.",
        "when": [
            "use when the task is spatial transcriptomics analysis or spatially aware visualization",
            "use when coordinates, images, or spot-level expression are part of the dataset",
            "use when the user needs domains, deconvolution, or neighborhood summaries",
        ],
        "inputs": ["spatial expression data", "coordinates or histology images", "optional single-cell reference"],
        "outputs": ["spatial domains", "deconvolution tables", "spatial maps and neighborhood results"],
        "tools": ["scanpy-like spatial tooling", "image analysis utilities", "matplotlib", "seaborn"],
        "steps": [
            ("Validate spatial assets", "Confirm coordinate systems, image registration, and barcode alignment where applicable."),
            ("Preprocess expression and spatial structure", "Normalize expression while preserving spatial coordinates and neighborhood information."),
            ("Choose a task path", "Run domain detection, deconvolution, communication, or neighborhood analysis according to the question."),
            ("Visualize spatial biology", "Generate maps that preserve physical context, legends, and scale."),
            ("Export interpretable artifacts", "Save spatial labels, coordinates, and figure-ready outputs."),
        ],
        "avoid": [
            "dropping coordinate integrity during preprocessing",
            "treating deconvolution outputs as ground truth cell counts",
            "using overcrowded spatial plots without readable legends",
        ],
        "sources": ["spatial transcriptomics workflows", "spatial omics task patterns"],
        "supplements": ["scanpy"],
    },
    {
        "path": "skills/epigenomics-and-regulation/atac-seq",
        "name": "atac-seq",
        "title": "ATAC Seq",
        "description": "Workflow for ATAC-seq QC, peak calling, accessibility summaries, motif deviation, footprinting, and differential accessibility.",
        "when": [
            "use when the task is bulk ATAC-seq or accessibility-focused chromatin profiling",
            "use when fragment-level QC, peak calling, or differential accessibility is required",
            "use when motif activity or footprinting is part of the interpretation",
        ],
        "inputs": ["ATAC-seq reads or fragments", "reference genome", "optional group metadata"],
        "outputs": ["peak sets", "QC metrics", "differential accessibility and motif summaries"],
        "tools": ["peak-calling tools", "deepTools-style summaries", "pandas", "matplotlib"],
        "steps": [
            ("Check assay quality", "Review fragment length periodicity, TSS enrichment, mapping quality, and duplication."),
            ("Call and consolidate peaks", "Generate peak sets and a consensus representation suitable for counting."),
            ("Quantify accessibility", "Build peak-by-sample matrices and test condition effects where appropriate."),
            ("Interpret motifs and footprints", "Use motif activity and footprint analyses only after confirming high-quality accessible peaks."),
            ("Export assay-ready outputs", "Save peak calls, count matrices, QC tables, and visualization assets."),
        ],
        "avoid": [
            "performing footprinting on low-quality or sparse peaks",
            "skipping TSS enrichment and fragment-size QC",
            "mixing peak sets from incompatible reference builds",
        ],
        "sources": ["ATAC-seq workflows", "chromatin accessibility task patterns", "signal track and coverage visualization patterns"],
        "supplements": ["deeptools", "pysam"],
    },
    {
        "path": "skills/epigenomics-and-regulation/chip-seq",
        "name": "chip-seq",
        "title": "ChIP Seq",
        "description": "Workflow for ChIP-seq QC, peak calling, annotation, motif analysis, differential binding, and track visualization.",
        "when": [
            "use when the task is TF or histone-mark ChIP-seq analysis",
            "use when the user needs peak calls, motif analysis, or differential binding",
            "use when signal tracks or genome-browser-ready outputs are part of the deliverable",
        ],
        "inputs": ["aligned treatment and control reads", "reference genome", "annotations"],
        "outputs": ["peak files", "annotated regions", "motif and differential binding summaries"],
        "tools": ["MACS2-style peak calling", "deepTools-style plotting", "pandas", "matplotlib"],
        "steps": [
            ("Check replicate and control structure", "Confirm whether the assay has input or control samples and whether replicates support robust calling."),
            ("Run peak calling", "Use assay-appropriate settings for narrow or broad marks."),
            ("Annotate and compare peaks", "Link peaks to genomic features and test differences across conditions when replicates permit."),
            ("Inspect motifs and tracks", "Use motif analysis and genome-browser views to verify major findings."),
            ("Export final artifacts", "Save peaks, counts, annotations, and track files for downstream review."),
        ],
        "avoid": [
            "calling broad and narrow marks with the same assumptions",
            "ignoring replicate consistency",
            "interpreting motif hits without checking peak quality and genomic context",
        ],
        "sources": ["ChIP-seq workflows", "peak-centric chromatin binding patterns", "signal track and coverage visualization patterns"],
        "supplements": ["deeptools", "pysam"],
    },
    {
        "path": "skills/epigenomics-and-regulation/methylation-analysis",
        "name": "methylation-analysis",
        "title": "Methylation Analysis",
        "description": "Workflow for methylation alignment or calling, DMR analysis, methylation QC, and locus-level interpretation.",
        "when": [
            "use when the task is DNA methylation calling or differential methylation",
            "use when bisulfite or long-read methylation data must be summarized at loci or regions",
            "use when methylation QC and DMR export are required",
        ],
        "inputs": ["methylation-aware sequencing reads", "reference genome", "sample metadata"],
        "outputs": ["methylation calls", "DMR tables", "sample and locus QC plots"],
        "tools": ["Bismark-like workflows", "pandas", "matplotlib", "seaborn"],
        "steps": [
            ("Check assay-specific preprocessing", "Use the correct alignment or calling path for bisulfite versus direct methylation detection."),
            ("Summarize methylation levels", "Aggregate calls at CpG, region, or feature level appropriate to the study question."),
            ("Run differential analysis", "Test differences using replicate-aware region-based methods when possible."),
            ("Inspect biological context", "Annotate DMRs to promoters, enhancers, or other regions before interpretation."),
            ("Export report-ready outputs", "Save calls, DMR tables, and locus-level example plots."),
        ],
        "avoid": [
            "mixing assay types without documenting the calling method",
            "reporting regional changes without effect direction and coverage context",
            "ignoring low-coverage loci during interpretation",
        ],
        "sources": ["DNA methylation analysis workflows"],
        "supplements": [],
    },
    {
        "path": "skills/epigenomics-and-regulation/epitranscriptomics",
        "name": "epitranscriptomics",
        "title": "Epitranscriptomics",
        "description": "Workflow for RNA modification analysis such as m6A peak calling, differential modification, and transcript-level visualization.",
        "when": [
            "use when the task is MeRIP-seq, direct RNA modification analysis, or differential RNA modification",
            "use when enriched IP and input comparisons need to be modeled carefully",
            "use when the user needs modification-aware plots and transcript-level context",
        ],
        "inputs": ["modification-enriched reads", "input reads", "transcript annotations"],
        "outputs": ["modification peaks", "differential modification results", "transcript-level plots"],
        "tools": ["peak-calling tools", "pandas", "matplotlib"],
        "steps": [
            ("Validate assay design", "Confirm IP and input matching, replicate availability, and transcript annotation consistency."),
            ("Call modification features", "Detect modification-enriched regions with assay-aware models."),
            ("Compare conditions", "Test differential modification while separating abundance changes from modification-specific changes where possible."),
            ("Visualize representative transcripts", "Plot peaks or signal tracks over transcripts to support interpretation."),
            ("Export clearly labeled outputs", "Separate modification results from standard expression results in all tables and plots."),
        ],
        "avoid": [
            "equating expression shifts with modification shifts",
            "calling differential modification without matched inputs or replicates where possible",
            "overstating transcript-level resolution when the assay is region-based",
        ],
        "sources": ["RNA modification workflows"],
        "supplements": [],
    },
    {
        "path": "skills/epigenomics-and-regulation/hi-c-3d-genomics",
        "name": "hi-c-3d-genomics",
        "title": "Hi-C And 3D Genomics",
        "description": "Workflow for Hi-C and related 3D genomics analyses including compartments, loops, TADs, differential contacts, and visualization.",
        "when": [
            "use when the task is Hi-C matrix analysis or 3D genome interpretation",
            "use when loops, compartments, or TADs must be called or compared",
            "use when contact-map figures or feature-level summaries are required",
        ],
        "inputs": ["Hi-C contact pairs or matrices", "genome bins", "condition metadata"],
        "outputs": ["compartments", "loops and TADs", "contact maps and differential summaries"],
        "tools": ["Hi-C processing utilities", "numpy", "pandas", "matplotlib"],
        "steps": [
            ("Validate matrix resolution", "Choose a resolution supported by coverage and the biological question."),
            ("Normalize contact structure", "Apply appropriate normalization before calling global or local features."),
            ("Call 3D features", "Infer compartments, TADs, or loops with methods matched to the resolution and assay."),
            ("Compare conditions carefully", "Quantify differences only where coverage and normalization support fair comparison."),
            ("Produce readable maps", "Export heatmaps and feature tables with clear genome coordinates and labels."),
        ],
        "avoid": [
            "interpreting noisy low-coverage matrices at overly fine resolution",
            "comparing raw contacts without normalization",
            "mixing feature scales without stating the resolution",
        ],
        "sources": ["3D genomics and Hi-C workflows"],
        "supplements": [],
    },
    {
        "path": "skills/epigenomics-and-regulation/gene-regulatory-networks",
        "name": "gene-regulatory-networks",
        "title": "Gene Regulatory Networks",
        "description": "Workflow for regulatory network inference, regulon scoring, perturbation-aware comparison, and network visualization.",
        "when": [
            "use when the task is GRN inference or regulon-level interpretation",
            "use when the data include expression matrices and optionally chromatin features or TF priors",
            "use when the user needs network-level summaries rather than only gene lists",
        ],
        "inputs": ["expression matrix", "optional accessibility data", "TF prior resources"],
        "outputs": ["inferred networks", "regulon activity tables", "network visualizations"],
        "tools": ["arboreto-like GRN utilities", "networkx", "pandas", "seaborn"],
        "steps": [
            ("Choose the evidence model", "Clarify whether inference is coexpression-based, prior-constrained, or multimodal."),
            ("Infer or score networks", "Run network inference or regulon-scoring methods appropriate to the data type."),
            ("Compare across states", "Summarize regulators and network changes across conditions, perturbations, or branches."),
            ("Visualize selectively", "Plot subnetworks or regulator-centric views rather than full unreadable graphs."),
            ("Export confidence-aware outputs", "Store edge weights, regulator scores, and evidence annotations."),
        ],
        "avoid": [
            "presenting inferred networks as validated causal circuitry",
            "plotting whole dense networks without summarization",
            "mixing inference evidence types without labeling them",
        ],
        "sources": ["gene regulatory network workflows", "tree- or regression-based GRN inference patterns"],
        "supplements": ["arboreto"],
    },
    {
        "path": "skills/genomics-and-variation/variant-calling",
        "name": "variant-calling",
        "title": "Variant Calling",
        "description": "Workflow for small-variant and structural-variant discovery, filtering, annotation, and interpretation from sequencing data.",
        "when": [
            "use when the user asks for germline, somatic, or structural variant calling",
            "use when BAM or CRAM files and a reference genome are available",
            "use when VCF generation, filtering, annotation, or interpretation is needed",
        ],
        "inputs": ["aligned reads", "reference genome", "optional truth set or panel resources"],
        "outputs": ["VCF files", "filtered variant tables", "annotation summaries"],
        "tools": ["GATK-style workflows", "DeepVariant-style workflows", "bcftools", "pandas"],
        "steps": [
            ("Define the variant task", "Separate germline, somatic, and structural variant paths early because assumptions differ."),
            ("Check alignment quality", "Review coverage, duplicate rates, contamination indicators, and reference compatibility before calling."),
            ("Call and filter variants", "Use caller-appropriate best practices and keep raw versus filtered outputs distinct."),
            ("Annotate and prioritize", "Attach gene, consequence, frequency, and clinical context before interpretation."),
            ("Export reproducible artifacts", "Save VCFs, filter criteria, annotation tables, and QC summaries."),
        ],
        "avoid": [
            "mixing germline and somatic assumptions",
            "interpreting unfiltered calls as final findings",
            "forgetting to record the reference build and caller version",
        ],
        "sources": ["variant-calling workflows", "clinical and research variant interpretation patterns", "alignment and VCF handling patterns"],
        "supplements": ["pysam", "tiledbvcf"],
    },
    {
        "path": "skills/genomics-and-variation/copy-number",
        "name": "copy-number",
        "title": "Copy Number",
        "description": "Workflow for copy-number estimation, segmentation, annotation, and visualization in sequencing-based assays.",
        "when": [
            "use when the task is CNV calling or copy-number visualization",
            "use when coverage-based segment inference is needed for tumor or cohort samples",
            "use when the user needs gene-level CNV summaries or segment plots",
        ],
        "inputs": ["coverage or ratio data", "target bins or intervals", "sample metadata"],
        "outputs": ["CNV segments", "gene-level CNV tables", "CNV plots"],
        "tools": ["CNVkit-style workflows", "GATK CNV-style workflows", "pandas", "matplotlib"],
        "steps": [
            ("Confirm assay context", "Clarify tumor-normal versus tumor-only design and target capture versus genome-wide coverage."),
            ("Generate or import coverage summaries", "Build bin- or target-level signals suitable for segmentation."),
            ("Call segments", "Infer copy-number segments and classify gains, losses, or focal events."),
            ("Annotate to genes and loci", "Map segments to biologically relevant genes and recurrent regions."),
            ("Report with visualization", "Produce chromosome-level plots and gene-centric summaries."),
        ],
        "avoid": [
            "treating noisy ratio shifts as confident focal events without segmentation support",
            "ignoring tumor purity or ploidy context when it matters",
            "reporting copy-number calls without genome build and binning details",
        ],
        "sources": ["copy-number workflows", "coverage- and segmentation-based CNV patterns"],
        "supplements": [],
    },
    {
        "path": "skills/genomics-and-variation/long-read-genomics",
        "name": "long-read-genomics",
        "title": "Long-Read Genomics",
        "description": "Workflow for nanopore or PacBio long-read QC, alignment, polishing, methylation-aware analysis, and structural variant discovery.",
        "when": [
            "use when the dataset is nanopore or PacBio long-read sequencing",
            "use when structural variants, phasing, polishing, or long-read methylation are part of the task",
            "use when long-read-specific QC and alignment assumptions must be respected",
        ],
        "inputs": ["long-read FASTQ or raw data", "reference genome", "sample metadata"],
        "outputs": ["aligned long-read files", "polished consensus or assembly updates", "long-read variant summaries"],
        "tools": ["long-read aligners", "Clair3-like SV or small-variant tools", "medaka-like polishing tools", "pandas"],
        "steps": [
            ("Assess long-read quality", "Check read length, quality distributions, and platform-specific artifacts."),
            ("Choose a long-read path", "Separate reference alignment, de novo assembly, and methylation-aware analyses as needed."),
            ("Run long-read-aware calling or polishing", "Use tools designed for long-read error profiles."),
            ("Interpret platform-specific outputs", "Report read-support and confidence metrics appropriate to long-read data."),
            ("Export standard artifacts", "Save BAM or CRAM, polished sequences, and variant or methylation summaries."),
        ],
        "avoid": [
            "using short-read assumptions for long-read error profiles",
            "skipping platform-specific QC",
            "mixing nanopore and PacBio outputs without documenting differences",
        ],
        "sources": ["long-read sequencing workflows"],
        "supplements": ["pysam"],
    },
    {
        "path": "skills/genomics-and-variation/genome-assembly",
        "name": "genome-assembly",
        "title": "Genome Assembly",
        "description": "Workflow for de novo assembly, scaffolding, polishing, contamination review, and assembly QC.",
        "when": [
            "use when the user needs a genome assembly from short, long, or hybrid reads",
            "use when the task includes scaffolding, polishing, or completeness evaluation",
            "use when final assembly statistics and contamination summaries are required",
        ],
        "inputs": ["short reads, long reads, or both", "optional reference or related genome", "sample context"],
        "outputs": ["assembled contigs or scaffolds", "assembly QC metrics", "contamination summaries"],
        "tools": ["assembly toolchains", "polishing tools", "QUAST-like QC", "pandas"],
        "steps": [
            ("Select assembly strategy", "Choose short-read, long-read, hybrid, or metagenome assembly based on the data and target organism."),
            ("Assemble and polish", "Run the appropriate assembler and follow with polishing suited to the sequencing platform."),
            ("Check contamination and completeness", "Evaluate assembly size, contiguity, contamination, and expected completeness."),
            ("Annotate assembly context", "Record strain, organism, ploidy, and sequencing assumptions that affect interpretation."),
            ("Export validated deliverables", "Save FASTA outputs plus QC tables and summary figures."),
        ],
        "avoid": [
            "using an assembler mismatched to the data type",
            "treating N50 as the only QC metric",
            "skipping contamination screening",
        ],
        "sources": ["genome assembly workflows"],
        "supplements": [],
    },
    {
        "path": "skills/genomics-and-variation/comparative-genomics",
        "name": "comparative-genomics",
        "title": "Comparative Genomics",
        "description": "Workflow for orthology, synteny, ancestral reconstruction, and evolutionary comparison across genomes.",
        "when": [
            "use when the task is cross-genome comparison or evolutionary inference",
            "use when assembled genomes and annotations are available for multiple taxa or strains",
            "use when the user needs orthologs, synteny blocks, or positive-selection style summaries",
        ],
        "inputs": ["assemblies", "gene annotations", "optional phylogenetic context"],
        "outputs": ["ortholog tables", "synteny outputs", "evolutionary comparison summaries"],
        "tools": ["orthology tools", "alignment and phylogeny utilities", "pandas"],
        "steps": [
            ("Define comparison scale", "Clarify whether the task is gene-level, synteny-level, or phylogenomic."),
            ("Standardize annotations", "Use consistent naming, feature models, and assemblies before comparing genomes."),
            ("Infer shared and divergent elements", "Run orthology, synteny, or evolutionary analyses appropriate to the question."),
            ("Interpret in biological context", "Separate technical annotation differences from genuine biological divergence."),
            ("Export concise comparison artifacts", "Save tables and figures that highlight conserved versus lineage-specific patterns."),
        ],
        "avoid": [
            "comparing genomes with incompatible annotation quality without caveats",
            "overstating adaptive evolution from weak evidence",
            "mixing orthology and homology claims carelessly",
        ],
        "sources": ["comparative genomics workflows"],
        "supplements": [],
    },
    {
        "path": "skills/genomics-and-variation/phasing-imputation",
        "name": "phasing-imputation",
        "title": "Phasing And Imputation",
        "description": "Workflow for haplotype phasing, genotype imputation, reference-panel matching, and imputation QC.",
        "when": [
            "use when the task is genotype phasing or imputation from array or sequence-derived variant data",
            "use when the study requires haplotypes, imputed markers, or downstream association-ready genotypes",
            "use when reference panel choice and QC are central to the analysis",
        ],
        "inputs": ["VCF genotype data", "sample metadata", "reference panel"],
        "outputs": ["phased genotypes", "imputed genotype set", "imputation QC metrics"],
        "tools": ["phasing tools", "imputation tools", "bcftools", "pandas"],
        "steps": [
            ("Validate cohort and reference compatibility", "Choose a reference panel matched to ancestry and build."),
            ("Phase genotypes", "Produce haplotype-aware inputs appropriate for the imputation engine."),
            ("Impute variants", "Run imputation and retain quality metrics such as INFO or dosage confidence."),
            ("Filter post-imputation", "Apply frequency and quality thresholds aligned with the downstream use case."),
            ("Export association-ready outputs", "Save phased or imputed VCFs and QC summaries."),
        ],
        "avoid": [
            "using a poorly matched reference panel without documenting the limitation",
            "keeping low-confidence imputed sites as if they were observed genotypes",
            "forgetting genome build harmonization",
        ],
        "sources": ["phasing and imputation workflows"],
        "supplements": [],
    },
    {
        "path": "skills/metagenomics-and-microbiome/metagenomics",
        "name": "metagenomics",
        "title": "Metagenomics",
        "description": "Workflow for shotgun metagenomics including abundance profiling, functional profiling, AMR detection, and strain tracking.",
        "when": [
            "use when the task is shotgun metagenomic taxonomic or functional analysis",
            "use when host depletion, abundance estimation, or AMR detection is part of the workflow",
            "use when the user needs community composition plus function or strain-level follow-up",
        ],
        "inputs": ["metagenomic FASTQ files", "sample metadata", "reference databases"],
        "outputs": ["taxonomic abundance tables", "functional profiles", "AMR or strain summaries"],
        "tools": ["Kraken-style classifiers", "MetaPhlAn-style profilers", "AMR resources", "pandas"],
        "steps": [
            ("Clean and classify reads", "Perform read QC and, where necessary, host depletion before taxonomic profiling."),
            ("Choose taxonomic strategy", "Use marker-based or k-mer-based methods depending on the question and resource limits."),
            ("Add function or AMR", "Profile functional pathways or resistance features when they are relevant to the task."),
            ("Compare samples and conditions", "Aggregate relative abundance and function across groups carefully."),
            ("Export reproducible community outputs", "Save abundance matrices, metadata joins, and summary plots."),
        ],
        "avoid": [
            "mixing taxonomic profiles from incompatible databases without stating it",
            "over-interpreting very low-abundance taxa",
            "ignoring host contamination in host-associated samples",
        ],
        "sources": ["shotgun metagenomics workflows", "community profiling and AMR task patterns"],
        "supplements": ["scikit-bio"],
    },
    {
        "path": "skills/metagenomics-and-microbiome/microbiome-amplicon",
        "name": "microbiome-amplicon",
        "title": "Microbiome Amplicon",
        "description": "Workflow for amplicon microbiome analysis including denoising, taxonomy assignment, diversity analysis, and differential abundance.",
        "when": [
            "use when the task is 16S, ITS, or other amplicon-based microbiome profiling",
            "use when denoising, taxonomy assignment, and diversity metrics are required",
            "use when the user needs cohort-level differential abundance or community structure summaries",
        ],
        "inputs": ["amplicon FASTQ files", "sample metadata", "taxonomy database"],
        "outputs": ["ASV or OTU tables", "taxonomy assignments", "diversity and differential abundance summaries"],
        "tools": ["QIIME2-style workflows", "pandas", "scikit-bio", "seaborn"],
        "steps": [
            ("Preprocess reads", "Trim primers or adapters and denoise reads into ASVs or OTUs."),
            ("Assign taxonomy", "Use a suitable taxonomy model or reference database for the marker type."),
            ("Compute diversity", "Calculate alpha and beta diversity with metadata-aware comparisons."),
            ("Compare groups", "Run differential abundance with methods matched to compositional data constraints."),
            ("Export community reports", "Save tables, ordinations, and taxonomy summaries."),
        ],
        "avoid": [
            "treating relative abundance changes as absolute shifts without context",
            "using a taxonomy database mismatched to the marker region",
            "running differential abundance without accounting for compositional effects",
        ],
        "sources": ["amplicon microbiome workflows", "community diversity and differential abundance patterns"],
        "supplements": ["scikit-bio"],
    },
    {
        "path": "skills/metagenomics-and-microbiome/pathogen-epi-genomics",
        "name": "pathogen-epi-genomics",
        "title": "Pathogen Epidemiological Genomics",
        "description": "Workflow for outbreak-style pathogen genomics, surveillance, lineage assignment, and transmission-oriented comparative analysis.",
        "when": [
            "use when the task is pathogen surveillance, lineage assignment, or outbreak genomics",
            "use when sample metadata include time, geography, or host context",
            "use when genomic comparison must be linked to epidemiological interpretation",
        ],
        "inputs": ["pathogen genomes or read sets", "collection metadata", "reference resources"],
        "outputs": ["lineage assignments", "cluster or outbreak summaries", "surveillance-ready tables or figures"],
        "tools": ["phylogenetics utilities", "variant and lineage-calling tools", "pandas"],
        "steps": [
            ("Standardize metadata", "Ensure time, location, and sample identifiers are consistent before analysis."),
            ("Generate comparable genomic summaries", "Call variants or consensus sequences in a way that supports cross-sample comparison."),
            ("Assign lineages or clusters", "Use pathogen-appropriate nomenclature and clustering logic."),
            ("Link genomics to epidemiology", "Summarize genomic findings with explicit metadata context and caution around transmission claims."),
            ("Export surveillance outputs", "Save lineage tables, phylogenies, and cluster summaries."),
        ],
        "avoid": [
            "claiming direct transmission from genomics alone",
            "mixing consensus builds or lineage schemes without stating it",
            "ignoring metadata QC in outbreak analyses",
        ],
        "sources": ["pathogen surveillance and epidemiological genomics workflows"],
        "supplements": ["phylogenetics"],
    },
    {
        "path": "skills/metagenomics-and-microbiome/phylogenetics",
        "name": "phylogenetics",
        "title": "Phylogenetics",
        "description": "Workflow for multiple sequence alignment, tree inference, annotated tree visualization, and distance-based evolutionary comparison.",
        "when": [
            "use when the task is tree building or evolutionary relationship analysis",
            "use when aligned sequences or genomes must be compared in phylogenetic context",
            "use when the user needs annotated trees or support metrics",
        ],
        "inputs": ["aligned sequences", "optional metadata", "model assumptions"],
        "outputs": ["phylogenetic trees", "annotated tree figures", "distance or support summaries"],
        "tools": ["alignment tools", "tree inference tools", "ete toolkit-style plotting", "matplotlib"],
        "steps": [
            ("Prepare alignment", "Trim or mask poorly aligned regions and confirm sequence comparability."),
            ("Choose an inference strategy", "Pick distance, maximum likelihood, or other tree approaches matched to the problem."),
            ("Assess support", "Include bootstrap or comparable support metrics where relevant."),
            ("Annotate with metadata", "Overlay sample metadata on trees for interpretation."),
            ("Export publishable trees", "Save tree files plus readable static figures."),
        ],
        "avoid": [
            "building trees from poor-quality or incompatible alignments",
            "omitting support metrics on uncertain topologies",
            "over-interpreting branch differences without scale context",
        ],
        "sources": ["phylogenetics workflows", "tree inference and visualization patterns"],
        "supplements": ["etetoolkit"],
    },
    {
        "path": "skills/proteomics-and-metabolomics/proteomics",
        "name": "proteomics",
        "title": "Proteomics",
        "description": "Workflow for mass spectrometry proteomics including identification, inference, quantification, QC, differential abundance, and PTM follow-up.",
        "when": [
            "use when the task is MS-based proteomics analysis",
            "use when peptide or protein quantification, DIA, PTM analysis, or QC is required",
            "use when the user needs cohort-level protein abundance comparisons and figures",
        ],
        "inputs": ["raw MS files or converted spectra", "sample metadata", "sequence database"],
        "outputs": ["peptide or protein tables", "QC summaries", "differential abundance results"],
        "tools": ["pyopenms", "pandas", "numpy", "seaborn", "matplotlib"],
        "steps": [
            ("Clarify assay type", "Separate DDA, DIA, PTM-enriched, and targeted analyses because downstream assumptions differ."),
            ("Check QC first", "Inspect identification rates, missingness, replicate behavior, and batch structure before interpretation."),
            ("Quantify consistently", "Keep peptide-level and protein-level outputs distinct and document normalization choices."),
            ("Perform comparative analysis", "Model differential abundance with replicate- and batch-aware methods."),
            ("Export interpretable deliverables", "Save protein tables, QC plots, and result figures with clear identifiers."),
        ],
        "avoid": [
            "mixing peptide and protein abundance levels in one result table",
            "ignoring missingness patterns before differential analysis",
            "treating low-confidence identifications as stable findings",
        ],
        "sources": ["proteomics workflows", "protein quantification and QC patterns", "Python mass spectrometry tooling patterns"],
        "supplements": ["pyopenms"],
    },
    {
        "path": "skills/proteomics-and-metabolomics/metabolomics",
        "name": "metabolomics",
        "title": "Metabolomics",
        "description": "Workflow for untargeted or targeted metabolomics including preprocessing, normalization, annotation, statistics, and pathway mapping.",
        "when": [
            "use when the task is LC-MS or GC-MS metabolomics",
            "use when the user needs feature tables, annotation, differential analysis, or pathway mapping",
            "use when targeted and untargeted workflows must be kept conceptually separate",
        ],
        "inputs": ["metabolomics raw files", "sample metadata", "annotation databases"],
        "outputs": ["feature tables", "annotated metabolites", "statistical and pathway summaries"],
        "tools": ["XCMS-like preprocessing", "MS-DIAL-style workflows", "pandas", "seaborn"],
        "steps": [
            ("Choose targeted or untargeted path", "Treat identification certainty, normalization, and comparisons differently by assay type."),
            ("Preprocess raw signals", "Perform peak detection, alignment, feature grouping, and QC filtering."),
            ("Normalize and annotate", "Apply batch-aware normalization and attach annotation confidence levels."),
            ("Run statistics and interpretation", "Test condition effects and map metabolites to pathways when biologically justified."),
            ("Export layered results", "Keep raw features, annotated metabolites, and pathway outputs in separate tables."),
        ],
        "avoid": [
            "overstating metabolite identity when annotation confidence is weak",
            "mixing targeted concentrations with untargeted relative abundances without stating it",
            "skipping QC samples and batch review",
        ],
        "sources": ["metabolomics workflows", "feature processing and annotation patterns", "metabolomics database lookup patterns"],
        "supplements": ["metabolomics-workbench-database"],
    },
    {
        "path": "skills/proteomics-and-metabolomics/imaging-mass-cytometry",
        "name": "imaging-mass-cytometry",
        "title": "Imaging Mass Cytometry",
        "description": "Workflow for multiplexed imaging or IMC segmentation, phenotyping, and spatial summarization.",
        "when": [
            "use when the task is imaging mass cytometry or related multiplexed tissue imaging",
            "use when segmentation, cell phenotyping, and spatial summaries are needed",
            "use when the deliverable includes cell-level features plus tissue-level maps",
        ],
        "inputs": ["marker images", "panel metadata", "segmentation masks or raw images"],
        "outputs": ["cell-level feature tables", "phenotype assignments", "spatial plots"],
        "tools": ["image analysis utilities", "pandas", "numpy", "matplotlib"],
        "steps": [
            ("Validate panel and images", "Confirm marker-channel mapping, image integrity, and segmentation assets."),
            ("Segment and quantify cells", "Produce cell-level intensities and morphological features."),
            ("Phenotype cells", "Assign cell states using marker panels and thresholding or clustering logic."),
            ("Summarize spatial organization", "Compute neighborhood or region-level patterns when the question requires them."),
            ("Export image-linked outputs", "Save cell tables, masks, and visualization overlays."),
        ],
        "avoid": [
            "using poorly validated segmentation as if it were exact",
            "hiding threshold assumptions in phenotype calls",
            "reporting only heatmaps without spatial context",
        ],
        "sources": ["imaging mass cytometry workflows"],
        "supplements": [],
    },
    {
        "path": "skills/proteomics-and-metabolomics/structural-biology",
        "name": "structural-biology",
        "title": "Structural Biology",
        "description": "Workflow for structure retrieval, prediction, inspection, modification, and geometry-aware biological interpretation.",
        "when": [
            "use when the task is protein or macromolecular structure analysis",
            "use when the user needs AlphaFold-style retrieval, structure IO, or geometry-based measurements",
            "use when sequence-level findings need structural context",
        ],
        "inputs": ["protein sequences", "structure files", "optional ligand or residue annotations"],
        "outputs": ["predicted or curated structures", "structural measurements", "annotated structure summaries"],
        "tools": ["alphafold-database", "biopython", "visualization or geometry utilities"],
        "steps": [
            ("Pick structure source", "Use experimental structures when available and predictions when appropriate."),
            ("Validate structural context", "Check chain mapping, residue numbering, and confidence metrics."),
            ("Measure or annotate", "Compute distances, sites, interfaces, or structural changes needed for the question."),
            ("Interpret cautiously", "Separate high-confidence structural observations from low-confidence predicted regions."),
            ("Export reusable outputs", "Save coordinates, annotation tables, and summary figures."),
        ],
        "avoid": [
            "treating low-confidence predicted regions as resolved structure",
            "mixing residue numbering systems without mapping them",
            "making mechanistic claims without structural evidence quality notes",
        ],
        "sources": ["structural biology workflows", "structure retrieval and prediction patterns"],
        "supplements": ["alphafold-database"],
    },
    {
        "path": "skills/multi-omics-and-systems/multi-omics-integration",
        "name": "multi-omics-integration",
        "title": "Multi-Omics Integration",
        "description": "Workflow for integrating matched or partially matched omics layers into shared latent structure and cross-modal interpretation.",
        "when": [
            "use when the task is multi-omics factor discovery or integrated cohort analysis",
            "use when the user has two or more omics modalities that should be related jointly",
            "use when cross-modal factors or harmonized sample structure are needed",
        ],
        "inputs": ["multiple omics matrices", "sample metadata", "feature mapping resources"],
        "outputs": ["integrated latent factors", "cross-modal associations", "integrated visualizations"],
        "tools": ["MOFA+-style approaches", "mixOmics-style approaches", "pandas", "numpy"],
        "steps": [
            ("Check sample and feature alignment", "Confirm which samples are shared and how features relate across modalities."),
            ("Normalize per modality", "Handle each omics layer according to its data-generating properties before integration."),
            ("Choose integration model", "Use a factor-based or correlation-based method matched to the question and data structure."),
            ("Interpret latent factors", "Link integrated components back to biology, covariates, and modality-specific loadings."),
            ("Export separated artifacts", "Save factors, loadings, and modality-aware summaries."),
        ],
        "avoid": [
            "forcing direct feature comparability across unrelated omics types",
            "ignoring modality-specific QC before integration",
            "reporting latent factors without biological interpretation or covariate review",
        ],
        "sources": ["multi-omics integration workflows", "cross-modal latent factor patterns"],
        "supplements": ["reactome-database", "string-database"],
    },
    {
        "path": "skills/multi-omics-and-systems/pathway-analysis",
        "name": "pathway-analysis",
        "title": "Pathway Analysis",
        "description": "Workflow for enrichment testing, ranked-gene analysis, pathway scoring, and pathway-focused visualization across omics outputs.",
        "when": [
            "use when the task is pathway enrichment or gene set interpretation",
            "use when the user has gene lists, ranked statistics, or pathway-scored samples",
            "use when Reactome, KEGG, GO, or similar resources are part of the deliverable",
        ],
        "inputs": ["gene lists or ranked statistics", "pathway databases", "optional sample-level matrices"],
        "outputs": ["enriched pathway tables", "pathway plots", "pathway interpretation summaries"],
        "tools": ["Reactome and STRING resources", "pandas", "matplotlib", "seaborn"],
        "steps": [
            ("Choose enrichment mode", "Use over-representation for filtered gene lists and ranked methods for full signed statistics."),
            ("Match identifiers", "Standardize gene IDs to the pathway database before testing."),
            ("Run enrichment and summarize", "Report effect direction, significance, and pathway sizes."),
            ("Visualize selectively", "Use dot plots, bar plots, or network summaries without overwhelming the reader."),
            ("Export pathway-ready tables", "Save standardized pathway identifiers, scores, and member genes."),
        ],
        "avoid": [
            "mixing identifier systems without conversion",
            "treating pathway databases as interchangeable without stating the source",
            "showing only p-values without effect direction or gene overlap context",
        ],
        "sources": ["pathway analysis workflows", "pathway database querying patterns", "interaction-network enrichment patterns"],
        "supplements": ["reactome-database", "string-database"],
    },
    {
        "path": "skills/multi-omics-and-systems/systems-biology",
        "name": "systems-biology",
        "title": "Systems Biology",
        "description": "Workflow for constraint-based metabolic modeling, context-specific models, gene essentiality, and systems-level interpretation.",
        "when": [
            "use when the task is flux balance analysis, metabolic reconstruction, or model-based systems biology",
            "use when transcriptomic or metabolomic data must be folded into pathway or network models",
            "use when the user needs model-derived pathway behavior rather than only enrichment analysis",
        ],
        "inputs": ["metabolic model", "omics-derived constraints", "reaction and metabolite annotations"],
        "outputs": ["flux solutions", "context-specific models", "pathway or essentiality summaries"],
        "tools": ["cobrapy", "pandas", "network utilities"],
        "steps": [
            ("Validate the model", "Check model format, reaction constraints, and biomass assumptions before analysis."),
            ("Integrate context", "Incorporate condition- or tissue-specific evidence when the task calls for it."),
            ("Run systems analysis", "Perform flux analysis, essentiality testing, or pathway-level model interrogation."),
            ("Interpret model outputs", "Relate flux shifts or essential reactions back to the biological question."),
            ("Export model-derived summaries", "Save flux tables, condition comparisons, and pathway views."),
        ],
        "avoid": [
            "treating model predictions as direct measurements",
            "skipping feasibility checks before comparing conditions",
            "mixing curated and auto-generated models without documenting it",
        ],
        "sources": ["systems biology workflows", "constraint-based modeling patterns"],
        "supplements": ["cobrapy"],
    },
    {
        "path": "skills/multi-omics-and-systems/causal-genomics",
        "name": "causal-genomics",
        "title": "Causal Genomics",
        "description": "Workflow for fine-mapping, colocalization, mediation, pleiotropy analysis, and Mendelian randomization.",
        "when": [
            "use when the task is causal variant, trait-to-gene, or mediation-style genomic inference",
            "use when GWAS and QTL summary data must be integrated",
            "use when the user needs statistical evidence about shared signals or directionality assumptions",
        ],
        "inputs": ["GWAS summary statistics", "QTL or molecular trait summary statistics", "LD reference"],
        "outputs": ["colocalization results", "credible sets", "causal evidence summaries"],
        "tools": ["summary-statistics workflows", "pandas", "numpy"],
        "steps": [
            ("Harmonize summary statistics", "Align alleles, genome builds, and variant IDs before combining datasets."),
            ("Pick the causal framework", "Use fine-mapping, colocalization, mediation, or MR according to the question."),
            ("Test and compare signals", "Quantify shared or potentially causal effects with the required assumptions stated clearly."),
            ("Review sensitivity", "Inspect heterogeneity, pleiotropy, and LD-related caveats before interpretation."),
            ("Export assumption-aware results", "Save summary tables with methods, assumptions, and confidence measures."),
        ],
        "avoid": [
            "treating statistical colocalization as definitive causal proof",
            "ignoring allele harmonization issues",
            "running MR without checking instrument quality and pleiotropy",
        ],
        "sources": ["causal genomics workflows"],
        "supplements": [],
    },
    {
        "path": "skills/multi-omics-and-systems/machine-learning-for-omics",
        "name": "machine-learning-for-omics",
        "title": "Machine Learning For Omics",
        "description": "Workflow for predictive modeling, biomarker discovery, survival modeling, and explainability over omics-derived features.",
        "when": [
            "use when the task is supervised learning on omics features",
            "use when the user needs a model, validation metrics, and interpretable feature importance",
            "use when the modeling objective is biomarker discovery, classification, regression, or survival prediction",
        ],
        "inputs": ["feature matrix", "labels or outcomes", "split or validation design"],
        "outputs": ["trained model", "validation metrics", "feature importance or explanation summaries"],
        "tools": ["scikit-learn", "statsmodels", "survival tooling where needed", "shap when appropriate"],
        "steps": [
            ("Define the prediction task", "Clarify outcome type, class balance, leakage risks, and validation plan."),
            ("Build a reproducible split", "Use train-validation-test or cross-validation schemes that respect cohort structure."),
            ("Train parsimonious models first", "Start with robust baseline models before complex architectures."),
            ("Evaluate honestly", "Report calibration, held-out performance, and failure modes instead of only one metric."),
            ("Explain cautiously", "Use importance or explanation methods as interpretation aids, not proof of causality."),
        ],
        "avoid": [
            "leakage across train and test sets",
            "high-dimensional modeling without strong regularization or validation",
            "presenting feature importance as mechanistic causality",
        ],
        "sources": ["omics machine-learning workflows", "scientific modeling and explainability patterns"],
        "supplements": ["scikit-learn", "statsmodels"],
    },
    {
        "path": "skills/core-bioinformatics/sequence-and-format-io",
        "name": "sequence-and-format-io",
        "title": "Sequence And Format IO",
        "description": "Workflow for foundational sequence parsing, conversion, compression handling, and interval-aware file validation.",
        "when": [
            "use when the task is file parsing, sequence manipulation, or format conversion",
            "use when FASTA, FASTQ, BED, GTF, BAM, or related files need validation or transformation",
            "use when a downstream omics workflow is blocked on messy input files",
        ],
        "inputs": ["sequence or annotation files", "format specifications", "optional metadata"],
        "outputs": ["validated or converted files", "summary statistics", "format sanity-check reports"],
        "tools": ["biopython", "pysam", "pandas", "basic shell utilities"],
        "steps": [
            ("Identify file semantics", "Do not assume a file is clean just because the extension looks right."),
            ("Validate core structure", "Check headers, coordinates, indexing, compression, and identifier consistency."),
            ("Convert safely", "Preserve metadata and line ordering where downstream tools depend on it."),
            ("Summarize content", "Produce quick counts and sanity-check metrics after transformation."),
            ("Hand off clean artifacts", "Save validated outputs with explicit naming and build context."),
        ],
        "avoid": [
            "silently converting between 0-based and 1-based coordinate systems",
            "rewriting compressed indexed files without regenerating indexes",
            "dropping metadata columns during format conversion",
        ],
        "sources": ["sequence I/O workflows", "genome interval handling patterns", "bioinformatics file utility patterns"],
        "supplements": ["pysam", "biopython"],
    },
    {
        "path": "skills/core-bioinformatics/alignment-and-mapping",
        "name": "alignment-and-mapping",
        "title": "Alignment And Mapping",
        "description": "Workflow for read alignment, sorting, indexing, mapping statistics, and downstream-ready alignment artifacts.",
        "when": [
            "use when the task is sequence alignment or alignment file preparation",
            "use when FASTQ files must be mapped to a genome or transcriptome",
            "use when BAM or CRAM files and mapping metrics are the expected outputs",
        ],
        "inputs": ["FASTQ files", "reference genome or transcriptome", "alignment indexes"],
        "outputs": ["sorted and indexed alignments", "mapping metrics", "downstream-ready BAM or CRAM files"],
        "tools": ["bwa", "bowtie2", "hisat2", "STAR", "samtools", "pysam"],
        "steps": [
            ("Choose the mapper", "Match the aligner to DNA, RNA, read length, and splice-awareness needs."),
            ("Run alignment reproducibly", "Capture all parameters that influence multi-mapping, splicing, and scoring."),
            ("Post-process alignments", "Sort, index, mark or handle duplicates as appropriate, and compute mapping summaries."),
            ("Check mapping quality", "Review alignment rate, insert sizes, and reference compatibility before downstream analysis."),
            ("Export standard artifacts", "Save BAM or CRAM plus indexes and mapping reports."),
        ],
        "avoid": [
            "using a DNA aligner for splice-aware RNA tasks without justification",
            "forgetting sort and index steps before downstream tools",
            "dropping read-group or sample metadata needed later",
        ],
        "sources": ["read alignment workflows", "pairwise and multiple alignment handling patterns", "alignment file management patterns"],
        "supplements": ["pysam"],
    },
    {
        "path": "skills/core-bioinformatics/read-qc",
        "name": "read-qc",
        "title": "Read QC",
        "description": "Workflow for sequencing read QC, trimming, contamination screening, and pre-alignment cleanup.",
        "when": [
            "use when the task is FASTQ quality assessment or cleanup before analysis",
            "use when the user needs trimming, contamination review, or read-level reports",
            "use when downstream pipelines depend on deciding whether data quality is acceptable",
        ],
        "inputs": ["raw FASTQ files", "adapter sequences", "optional sequencing metadata"],
        "outputs": ["QC reports", "filtered or trimmed reads", "contamination summaries"],
        "tools": ["fastp", "FastQC-style reports", "pandas", "matplotlib"],
        "steps": [
            ("Profile raw reads", "Inspect quality scores, adapter content, duplication, and GC behavior before trimming."),
            ("Trim or filter judiciously", "Apply adapter removal and quality filtering with settings matched to the assay."),
            ("Screen contamination", "Check for host, ribosomal, or other unwanted content if the study design calls for it."),
            ("Re-evaluate after cleanup", "Confirm that trimming improved quality without over-truncating useful reads."),
            ("Export both reports and cleaned reads", "Keep raw and cleaned QC records for reproducibility."),
        ],
        "avoid": [
            "trimming aggressively without checking length distributions afterward",
            "assuming all contamination is removable without assay-specific review",
            "running downstream analysis on reads that failed basic QC without documenting it",
        ],
        "sources": ["read quality-control workflows"],
        "supplements": [],
    },
    {
        "path": "skills/core-bioinformatics/database-access",
        "name": "database-access",
        "title": "Database Access",
        "description": "Workflow for retrieving public omics datasets, sequences, annotations, and literature-linked biological resources.",
        "when": [
            "use when the task is downloading or querying public bioinformatics databases",
            "use when accessions, identifiers, or search terms must be resolved into data assets",
            "use when external references such as GEO, SRA, UniProt, Reactome, or PubMed are needed",
        ],
        "inputs": ["accessions or identifiers", "query terms", "optional species or database constraints"],
        "outputs": ["downloaded datasets", "linked metadata tables", "query result summaries"],
        "tools": ["Entrez-style APIs", "UniProt access tools", "Reactome and PubMed resources", "pandas"],
        "steps": [
            ("Pick the right database", "Choose repositories based on whether the target is raw data, processed data, annotation, pathways, or literature."),
            ("Query reproducibly", "Record identifiers, filters, and database versions or access dates."),
            ("Normalize returned metadata", "Standardize result tables so downstream workflows can join on stable IDs."),
            ("Download only needed assets", "Avoid bulk retrieval when a narrower dataset or accession list solves the task."),
            ("Export usable references", "Save accession tables, metadata joins, and database provenance."),
        ],
        "avoid": [
            "mixing identifiers across databases without explicit mapping",
            "downloading oversized collections when a filtered subset is enough",
            "citing database content without recording provenance",
        ],
        "sources": ["bioinformatics database access workflows", "literature and pathway lookup patterns", "public dataset retrieval patterns"],
        "supplements": ["pubmed-database", "reactome-database", "string-database"],
    },
    {
        "path": "skills/core-bioinformatics/reporting-and-figure-export",
        "name": "reporting-and-figure-export",
        "title": "Reporting And Figure Export",
        "description": "Workflow for packaging analysis outputs into reproducible reports, clean tables, and publication-ready figure exports.",
        "when": [
            "use when the task is to turn analysis outputs into a clear report or deliverable",
            "use when plots and tables must be exported in publication- or presentation-ready form",
            "use when a notebook, Quarto report, or figure bundle is needed",
        ],
        "inputs": ["analysis tables", "plots", "metadata", "interpretation notes"],
        "outputs": ["QC or analysis reports", "exported figures", "deliverable-ready tables"],
        "tools": ["matplotlib", "seaborn", "Quarto-style or notebook reporting", "pandas"],
        "steps": [
            ("Separate raw outputs from presentation outputs", "Keep the analysis artifacts intact and build curated exports on top."),
            ("Standardize figure formatting", "Use consistent fonts, labels, color legends, and vector output when possible."),
            ("Assemble compact reports", "Summarize key methods, QC, main findings, and file provenance."),
            ("Export tables cleanly", "Write machine-readable and human-readable result tables with stable column names."),
            ("Preserve reproducibility", "Record how the report and figures were generated."),
        ],
        "avoid": [
            "copy-pasting plots without recording how they were made",
            "using unreadable legends, tiny fonts, or raster-only outputs when vector is possible",
            "mixing exploratory and final figures without labeling them",
        ],
        "sources": ["bioinformatics reporting workflows", "publication-quality figure and export patterns"],
        "supplements": ["seaborn", "plotly"],
    },
    {
        "path": "skills/core-bioinformatics/workflow-management",
        "name": "workflow-management",
        "title": "Workflow Management",
        "description": "Workflow for orchestrating reproducible omics pipelines with workflow engines and clear execution provenance.",
        "when": [
            "use when the task is to organize or run a reproducible omics pipeline",
            "use when Nextflow, Snakemake, CWL, or WDL style workflows are involved",
            "use when a one-off analysis should be turned into a repeatable pipeline",
        ],
        "inputs": ["pipeline definitions", "sample sheets", "environment descriptions"],
        "outputs": ["reproducible workflow runs", "execution logs", "portable pipeline assets"],
        "tools": ["Nextflow", "Snakemake", "CWL", "WDL"],
        "steps": [
            ("Define the workflow boundary", "State inputs, outputs, parameters, and expected execution environment clearly."),
            ("Choose an engine", "Use the engine already established by the project unless there is a strong reason not to."),
            ("Separate config from logic", "Keep sample sheets, resources, and environment settings outside the core task definitions."),
            ("Capture provenance", "Retain logs, software versions, and execution metadata for reruns."),
            ("Export reusable workflow assets", "Save configs, manifests, and run summaries in a stable structure."),
        ],
        "avoid": [
            "hardcoding sample-specific paths into pipeline logic",
            "mixing environment setup and workflow semantics in one opaque script",
            "running pipelines without recording versions and configs",
        ],
        "sources": ["workflow-management patterns for reproducible omics pipelines"],
        "supplements": [],
    },
]


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").title()


def infer_primary_tool(entry: dict) -> str:
    overrides = {
        "cell-annotation": "CellTypist",
        "scrna-preprocessing-clustering": "scanpy",
        "differential-expression": "PyDESeq2",
        "atac-seq": "MACS3",
        "chip-seq": "MACS3",
        "proteomics": "pyopenms",
        "metabolomics": "MS-DIAL/XCMS",
        "structural-biology": "AlphaFold DB",
        "database-access": "requests",
        "workflow-management": "Nextflow",
        "alignment-and-mapping": "samtools",
        "rna-quantification": "salmon",
        "phylogenetics": "IQ-TREE",
        "systems-biology": "cobrapy",
    }
    if entry["name"] in overrides:
        return overrides[entry["name"]]
    first = entry["tools"][0]
    return first.split(",")[0].split(" ")[0]


def infer_tool_type(entry: dict) -> str:
    text = " ".join(entry["tools"]).lower()
    if any(x in text for x in ["nextflow", "snakemake", "cwl", "wdl", "bwa", "bowtie2", "hisat2", "star", "salmon", "kallisto", "featurecounts"]):
        return "mixed"
    if any(x in text for x in ["peak-calling", "macs", "workflow", "aligner", "gsutil"]):
        return "mixed"
    return "python"


def render_version_compatibility(entry: dict) -> str:
    primary = infer_primary_tool(entry)
    return dedent(
        f"""\
Reference examples assume recent stable releases of the preferred tools, especially `{primary}` and the other tools listed below.

Before using code or command patterns, verify installed versions match the environment:

- Python: `python -c "import <module>; print(<module>.__version__)"`
- CLI: `<tool> --version`
- If signatures differ, inspect the installed help or API and adapt the pattern instead of retrying unchanged.
"""
    )


def render_quick_route(entry: dict) -> str:
    return dedent(
        f"""\
- If the input is raw or minimally processed data, start with validation and QC before any modeling.
- If the input is already processed, skip directly to the first workflow step that matches the user goal.
- If the user asks for a biological conclusion, always produce at least one QC or confidence artifact alongside the final result.
"""
    )


def render_reference_hint(entry: dict) -> str:
    return dedent(
        """\
- Read `references/technical_reference.md` when you need deeper tool-selection rules, environment adaptation notes, or extra validation guidance.
- Keep `SKILL.md` as the main execution path and load the reference file only when the task or failure mode needs the extra detail.
"""
    )


def render_starter_pattern(entry: dict) -> str:
    name = entry["name"]
    primary = infer_primary_tool(entry)

    if name == "cell-annotation":
        return dedent(
            """```python
import scanpy as sc
import celltypist

adata = sc.read_h5ad("input.h5ad")
pred = celltypist.annotate(adata, model="Immune_All_Low.pkl", majority_voting=True)
adata = pred.to_adata()
adata.write("results/annotated.h5ad")
```"""
        )
    if name == "scrna-preprocessing-clustering":
        return dedent(
            """```python
import scanpy as sc

adata = sc.read_h5ad("input.h5ad")
sc.pp.calculate_qc_metrics(adata, inplace=True)
sc.pp.normalize_total(adata, target_sum=1e4)
sc.pp.log1p(adata)
sc.pp.highly_variable_genes(adata, n_top_genes=2000)
sc.tl.pca(adata)
sc.pp.neighbors(adata)
sc.tl.umap(adata)
sc.tl.leiden(adata)
adata.write("results/processed.h5ad")
```"""
        )
    if name == "differential-expression":
        return dedent(
            """```python
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats

dds = DeseqDataSet(counts=counts_df, metadata=metadata_df, design_factors="condition")
dds.deseq2()
stats = DeseqStats(dds, contrast=("condition", "treated", "control"))
stats.summary()
results_df = stats.results_df
```"""
        )
    if name in {"atac-seq", "chip-seq"}:
        return dedent(
            """```bash
# Replace placeholders with assay-specific files and parameters
peak_caller callpeak \\
  -t treatment.bam \\
  -c control.bam \\
  -f BAM \\
  -g hs \\
  -n sample \\
  --outdir peaks/
```"""
        )
    if name == "alignment-and-mapping":
        return dedent(
            """```bash
bwa mem ref.fa sample_R1.fastq.gz sample_R2.fastq.gz | samtools sort -o sample.bam
samtools index sample.bam
samtools flagstat sample.bam > sample.flagstat.txt
```"""
        )
    if name == "rna-quantification":
        return dedent(
            """```bash
salmon quant \\
  -i transcriptome_index \\
  -l A \\
  -1 sample_R1.fastq.gz \\
  -2 sample_R2.fastq.gz \\
  -o quant/sample
```"""
        )
    if name == "database-access":
        return dedent(
            """```python
import requests

resp = requests.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi", params={
    "db": "gds",
    "term": "single cell liver",
    "retmode": "json",
})
print(resp.text[:500])
```"""
        )
    if name == "proteomics":
        return dedent(
            """```python
import pandas as pd

protein_df = pd.read_csv("protein_groups.tsv", sep="\\t")
sample_cols = [c for c in protein_df.columns if c.startswith("LFQ intensity")]
intensity_matrix = protein_df[sample_cols].replace(0, pd.NA)
qc_summary = intensity_matrix.notna().sum().sort_values()
```"""
        )
    if name == "metabolomics":
        return dedent(
            """```python
import pandas as pd

feature_df = pd.read_csv("feature_table.csv")
sample_cols = [c for c in feature_df.columns if c.startswith("sample_")]
matrix = feature_df[sample_cols]
```"""
        )
    if name == "structural-biology":
        return dedent(
            """```python
from Bio.PDB import alphafold_db

prediction = next(alphafold_db.get_predictions("P00520"))
cif_path = alphafold_db.download_cif_for(prediction, directory="structures")
print(cif_path)
```"""
        )
    if name == "workflow-management":
        return dedent(
            """```bash
nextflow run main.nf \\
  --input samplesheet.csv \\
  --outdir results/
```"""
        )
    if name == "systems-biology":
        return dedent(
            """```python
import cobra

model = cobra.io.read_sbml_model("model.xml")
solution = model.optimize()
print(solution.objective_value)
```"""
        )
    if name == "phylogenetics":
        return dedent(
            """```bash
mafft --auto input.fasta > aligned.fasta
iqtree2 -s aligned.fasta -m MFP -B 1000
```"""
        )
    return dedent(
        f"""```text
Preferred starting point: {primary}
Inputs: {", ".join(entry["inputs"])}
Outputs: {", ".join(entry["outputs"])}
```"""
    )


def render_artifacts(entry: dict) -> str:
    outputs = "\n".join(f"- `{line}`" for line in entry["outputs"])
    return dedent(
        f"""\
- Recommended output layout:
  - `results/` for final tables and serialized objects
  - `figures/` for plots and static visual exports
  - `qc/` for checks that justify downstream interpretation
- Minimum expected outputs for this skill:
{outputs}
"""
    )


def render_reference_file(entry: dict) -> str:
    when = "\n".join(f"- {line}" for line in entry["when"])
    inputs = "\n".join(f"- {line}" for line in entry["inputs"])
    outputs = "\n".join(f"- {line}" for line in entry["outputs"])
    tools = "\n".join(f"- {line}" for line in entry["tools"])
    steps = "\n".join(
        f"### {i + 1}. {title}\n\n{body}\n"
        for i, (title, body) in enumerate(entry["steps"])
    )
    avoid = "\n".join(f"- {line}" for line in entry["avoid"])
    supplements = "\n".join(f"- `{line}`" for line in entry["supplements"]) if entry["supplements"] else "- None"
    sources = "\n".join(f"- {line}" for line in entry["sources"])
    return dedent(
        f"""\
# {entry["title"]} Technical Reference

## Purpose

This reference file provides deeper implementation notes for `{entry["name"]}`.

## When To Read This File

{when}

## Detailed Inputs

{inputs}

## Detailed Outputs

{outputs}

## Tooling Notes

{tools}

## Detailed Workflow Notes

{steps}
## Validation Priorities

{render_quality_checks(entry)}

## Common Failure Modes

{avoid}

## Optional Supplements

{supplements}

## Conceptual Provenance

{sources}
"""
    )


def render_quality_checks(entry: dict) -> str:
    group = Path(entry["path"]).parts[1]
    specific = {
        "structural-biology": [
            "Review residue numbering, chain identity, and confidence metrics before mapping biology onto structure.",
            "Separate high-confidence folded regions from low-confidence or disordered regions in the final interpretation.",
        ],
        "database-access": [
            "Record accession provenance, query parameters, and retrieval date or version.",
            "Verify that downloaded records map cleanly to the identifiers used downstream.",
        ],
        "workflow-management": [
            "Verify config, manifests, and sample sheets before launching a full run.",
            "Retain logs, versions, and the exact workflow entrypoint used for the run.",
        ],
        "sequence-and-format-io": [
            "Check coordinate systems, compression, and index consistency after every conversion.",
            "Run a lightweight sanity check before handing files to downstream tools.",
        ],
        "alignment-and-mapping": [
            "Confirm reference build, read-group metadata, and sort or index state before downstream analysis.",
            "Review mapping summaries before treating alignments as analysis-ready.",
        ],
        "cell-annotation": [
            "Compare transferred or classifier-derived labels against marker expression before finalizing labels.",
            "Keep uncertain cells or clusters explicitly marked rather than forcing confident labels.",
        ],
    }
    common = [
        "Confirm identifiers and metadata join correctly before modeling or summarizing.",
        "Generate at least one QC artifact before final biological interpretation.",
        "Keep raw or minimally processed inputs separate from transformed outputs.",
    ]
    group_specific = {
        "transcriptomics": [
            "Check replicate structure, outlier samples, and whether counts versus normalized values are being mixed.",
            "Export ranked or contrast-aware tables when downstream enrichment is likely.",
        ],
        "single-cell-and-spatial": [
            "Review embeddings together with QC metrics and batch structure before labeling biology.",
            "Preserve the processed object with metadata and embeddings for downstream reuse.",
        ],
        "epigenomics-and-regulation": [
            "Check assay-specific QC such as enrichment quality, coverage behavior, or replicate consistency.",
            "Verify genome build, interval coordinates, and annotation compatibility.",
        ],
        "genomics-and-variation": [
            "Record reference build, caller assumptions, and filtering rules in the final outputs.",
            "Separate raw calls from filtered or interpreted results.",
        ],
        "metagenomics-and-microbiome": [
            "Review sample contamination, depth differences, and database choice before comparing communities.",
            "State clearly whether outputs are relative abundance, counts, or derived functions.",
        ],
        "proteomics-and-metabolomics": [
            "Check missingness, batch effects, and identification or annotation confidence before differential interpretation.",
            "Keep feature-level and summarized entity-level outputs distinct.",
        ],
        "multi-omics-and-systems": [
            "Verify that modalities, samples, and model assumptions align before integration or inference.",
            "Export factors, scores, or model outputs together with interpretation context.",
        ],
        "core-bioinformatics": [
            "Validate file structure and metadata before handing outputs to downstream tools.",
            "Retain provenance for every conversion, query, or pipeline execution step.",
        ],
    }
    bullets = common + specific.get(entry["name"], group_specific.get(group, []))
    return "\n".join(f"- {line}" for line in bullets)


def render_related_skills(entry: dict) -> str:
    group_dir = Path(entry["path"]).parts[1]
    siblings = [
        other["title"]
        for other in SKILLS
        if other["path"] != entry["path"] and Path(other["path"]).parts[1] == group_dir
    ]
    related = siblings[:4]
    return "\n".join(f"- `{item}`" for item in related)


def render_skill(entry: dict) -> str:
    tool_type = infer_tool_type(entry)
    primary_tool = infer_primary_tool(entry)
    when = "\n".join(f"- {line}" for line in entry["when"])
    inputs = "\n".join(f"- {line}" for line in entry["inputs"])
    outputs = "\n".join(f"- {line}" for line in entry["outputs"])
    tools = "\n".join(f"- {line}" for line in entry["tools"])
    steps = "\n".join(
        f"### {i + 1}. {title}\n\n{body}\n"
        for i, (title, body) in enumerate(entry["steps"])
    )
    avoid = "\n".join(f"- {line}" for line in entry["avoid"])
    supplements = "\n".join(f"- `{line}`" for line in entry["supplements"]) if entry["supplements"] else "- None required for the first pass."

    return dedent(
        f"""\
---
name: {entry["name"]}
description: {entry["description"]}
tool_type: {tool_type}
primary_tool: {primary_tool}
---

# {entry["title"]}

## Version Compatibility

{render_version_compatibility(entry)}

## Overview

{entry["description"]}

## When To Use This Skill

{when}

## Quick Route

{render_quick_route(entry)}

## Progressive Disclosure

{render_reference_hint(entry)}

## Default Rules

- Prefer Python-first workflows unless the task explicitly requires something else.
- Keep intermediate and final outputs separated.
- Record software versions, reference builds, and key parameters when they affect interpretation.
- Favor reproducible tables and figures over one-off interactive-only outputs.

## Expected Inputs

{inputs}

## Expected Outputs

{outputs}

## Preferred Tools

{tools}

## Starter Pattern

{render_starter_pattern(entry)}

## Workflow

{steps}

## Output Artifacts

{render_artifacts(entry)}

## Quality Review

{render_quality_checks(entry)}

## Anti-Patterns

{avoid}

## Related Skills

{render_related_skills(entry)}

## Optional Supplements

{supplements}
"""
    )


def render_readme(entry: dict) -> str:
    inputs = "\n".join(f"- {line}" for line in entry["inputs"])
    outputs = "\n".join(f"- {line}" for line in entry["outputs"])
    sources = "\n".join(f"- {line}" for line in entry["sources"])
    supplements = "\n".join(f"- `{line}`" for line in entry["supplements"]) if entry["supplements"] else "- None for the minimal version."
    return dedent(
        f"""\
# {entry["title"]}

## Scope

{entry["description"]}

## Typical Inputs

{inputs}

## Typical Outputs

{outputs}

## Conceptual Seeds

{sources}

## Optional Supplements

{supplements}

## Main Skill File

- `SKILL.md`
"""
    )


def main() -> None:
    for entry in SKILLS:
        if entry["path"] in MANUAL_OVERRIDE_PATHS:
            continue
        skill_dir = ROOT / entry["path"]
        refs_dir = skill_dir / "references"
        refs_dir.mkdir(parents=True, exist_ok=True)
        skill_dir.joinpath("SKILL.md").write_text(render_skill(entry), encoding="utf-8")
        skill_dir.joinpath("README.md").write_text(render_readme(entry), encoding="utf-8")
        refs_dir.joinpath("technical_reference.md").write_text(
            render_reference_file(entry),
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
