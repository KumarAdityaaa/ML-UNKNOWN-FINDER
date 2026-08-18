# AI Unknown Finder

> **An LLM-Powered Scientific Knowledge Discovery System for Identifying Research Gaps, Contradictions, and Testable Hypotheses from Scientific Literature.**

## Project Status

**Phase:** Project bootstrap  
**Status:** Initial repository setup  
**Primary branch:** `main`

## Vision

AI Unknown Finder is a research-oriented machine learning system designed to move beyond literature retrieval and summarization toward **evidence-backed discovery of potential unknowns in scientific literature**.

Given a defined corpus of scientific papers, the system will extract claims, methods, datasets, results, assumptions, limitations, and evidence; construct a research knowledge graph; identify contradictions and underexplored relationships; and generate candidate research hypotheses with explicit evidence traces.

The system will **not claim that a generated hypothesis is scientifically novel merely because an LLM produced it**. Novelty will be treated as an estimate over a defined literature corpus and validated through explicit search boundaries and human evaluation.

## Research Questions

1. Can AI identify evidence-backed potential knowledge gaps from scientific literature?
2. Can AI detect meaningful contradictions between independent scientific claims?
3. Can AI identify underexplored combinations of methods, datasets, concepts, and experimental conditions?
4. Can AI generate scientifically testable hypotheses from structured literature evidence?
5. Can every generated hypothesis be traced back to supporting or conflicting evidence?
6. How accurately can the system rank candidate gaps and hypotheses compared with human researchers?

## Planned Pipeline

```text
Scientific Literature
        ↓
Literature Collection
        ↓
PDF / Document Parsing
        ↓
Scientific Information Extraction
        ↓
Claim + Evidence Representation
        ↓
Research Knowledge Graph
        ↓
Contradiction Detection
        ↓
Research Gap Detection
        ↓
Candidate Hypothesis Generation
        ↓
Evidence Tracing
        ↓
Novelty / Feasibility / Impact Estimation
        ↓
Human Evaluation
        ↓
Interactive Research Dashboard
```

## Core Modules

| Module | Purpose | Status |
|---|---|---|
| Literature ingestion | Collect and register scientific papers | Planned |
| Document parsing | Extract structured content from papers | Planned |
| Scientific extraction | Extract concepts, claims, methods, datasets, results, limitations and evidence | Planned |
| Knowledge graph | Represent relationships between scientific entities and claims | Planned |
| Contradiction detection | Identify and classify conflicting claims | Planned |
| Gap detection | Find missing evaluations, disconnected concepts and underexplored combinations | Planned |
| Hypothesis generation | Produce candidate, testable research hypotheses | Planned |
| Evidence tracing | Link every result to source papers and reasoning paths | Planned |
| Novelty estimation | Estimate originality within the defined corpus | Planned |
| Evaluation | Measure system quality against human judgments and baselines | Planned |
| Dashboard | Explore graphs, gaps, contradictions and hypotheses | Planned |

## Research Integrity Principles

- **Evidence before generation:** hypotheses must be grounded in extracted literature evidence.
- **Corpus-bounded claims:** absence from the indexed corpus must not be presented as proof that nobody has studied a topic.
- **Traceability:** generated outputs must link back to source papers, claims, and graph paths.
- **Reproducibility:** datasets, configurations, experiments, and evaluation procedures will be versioned where legally and technically possible.
- **Modularity:** every major component will be independently testable.
- **Human validation:** scientific novelty and significance will ultimately require human assessment and, where applicable, experimental validation.

## Development Philosophy

This repository is being developed as a collaborative research project. Each implementation stage will include:

1. a defined research or engineering objective;
2. a reproducible implementation;
3. tests or validation criteria;
4. documentation updates;
5. a focused Git commit or pull request.

Large dependencies and advanced models will be introduced only when they are required by a validated stage of the pipeline.

## Repository Structure

The repository structure will evolve with the implementation. The intended architecture is:

```text
ML-UNKNOWN-FINDER/
├── configs/                 # Reproducible configuration files
├── data/                    # Local datasets and derived artifacts (ignored when appropriate)
├── docs/                    # Architecture, research decisions, experiments and methodology
├── models/                  # Locally downloaded/model artifacts (ignored when appropriate)
├── notebooks/              # Exploratory research notebooks
├── scripts/                # Reproducible utility and pipeline scripts
├── src/                    # Production Python package
│   └── unknown_finder/
│       ├── ingestion/
│       ├── parsing/
│       ├── extraction/
│       ├── knowledge_graph/
│       ├── contradiction/
│       ├── gaps/
│       ├── hypothesis/
│       ├── evidence/
│       ├── novelty/
│       └── evaluation/
├── tests/                  # Automated tests
├── dashboard/              # Interactive research interface
├── .gitignore
├── CONTRIBUTING.md
├── environment.yml
├── requirements.txt
└── README.md
```

## Development Environment

The primary development environment will use **Conda with Python 3.11**. Exact package versions will be recorded as the implementation progresses so that collaborators can reproduce the environment.

## Current Milestone

### Milestone 0 — Repository Bootstrap

- [x] Create GitHub repository
- [x] Establish project vision and research principles
- [ ] Add reproducible Conda environment
- [ ] Add Python package structure
- [ ] Add testing infrastructure
- [ ] Add CI validation
- [ ] Add contribution workflow

## Roadmap

### Phase 1 — Literature Ingestion

- [x] Literature source abstraction
- [x] OpenAlex integration
- [x] Paper metadata schema
- [x] Metadata validation
- [x] Metadata storage
- [x] Automated ingestion tests
- [ ] arXiv integration
- [ ] Semantic Scholar integration
- [x] PubMed integration
- [ ] Corpus deduplication
- [ ] Paper download pipeline

### Phase 2 — Literature Ingestion

Build a source-agnostic paper registry and collectors for selected scholarly APIs.

### Phase 3 — Scientific Document Understanding

Parse papers and extract structured scientific information.

### Phase 4 — Research Knowledge Graph

Represent papers, claims, methods, datasets, experiments, metrics and relationships.

### Phase 5 — Discovery Engine

Implement contradiction detection, gap detection and underexplored relationship discovery.

### Phase 6 — Hypothesis Engine

Generate and rank candidate hypotheses with explicit evidence traces.

### Phase 7 — Evaluation

Build datasets, baselines, human evaluation protocols and ablation studies.

### Phase 8 — Research Dashboard

Provide interactive exploration of the research graph and discovery results.

## Important Limitation

The first version will operate on a **defined and documented literature corpus**. Statements such as "this has never been studied" will therefore be avoided unless supported by an explicitly defined search methodology and sufficient coverage evidence.

## License

License will be selected during the repository bootstrap phase before external redistribution.
