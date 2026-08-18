**# AI Unknown Finder**

\> **\*\*An LLM-Powered Scientific Knowledge Discovery System for Identifying Research Gaps, Contradictions, and Testable Hypotheses from Scientific Literature.\*\***

**## Project Status**

**\*\*Current Phase:\*\*** Literature Ingestion  

**\*\*Current Milestone:\*\*** Literature Ingestion Foundation  

**\*\*Status:\*\*** In active development  

**\*\*Primary branch:\*\*** \`main\`

**## Vision**

AI Unknown Finder is a research-oriented machine learning system designed to move beyond literature retrieval and summarization toward **\*\*evidence-backed discovery of potential unknowns in scientific literature\*\***.

Given a defined corpus of scientific papers, the system will extract claims, methods, datasets, results, assumptions, limitations, and evidence; construct a research knowledge graph; identify contradictions and underexplored relationships; and generate candidate research hypotheses with explicit evidence traces.

The system will **\*\*not claim that a generated hypothesis is scientifically novel merely because an LLM produced it\*\***. Novelty will be treated as an estimate over a defined literature corpus and validated through explicit search boundaries and human evaluation.

**## Research Questions**

1\. Can AI identify evidence-backed potential knowledge gaps from scientific literature?

2\. Can AI detect meaningful contradictions between independent scientific claims?

3\. Can AI identify underexplored combinations of methods, datasets, concepts, and experimental conditions?

4\. Can AI generate scientifically testable hypotheses from structured literature evidence?

5\. Can every generated hypothesis be traced back to supporting or conflicting evidence?

6\. How accurately can the system rank candidate gaps and hypotheses compared with human researchers?

**## Planned Pipeline**

\`\`\`text

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

\`\`\`

**## Core Modules**

\| Module | Purpose | Status |

\|---|---|---|

\| Literature ingestion | Collect and register scientific papers | **\*\*In progress\*\*** |

\| Document parsing | Extract structured content from papers | Planned |

\| Scientific extraction | Extract concepts, claims, methods, datasets, results, limitations and evidence | Planned |

\| Knowledge graph | Represent relationships between scientific entities and claims | Planned |

\| Contradiction detection | Identify and classify conflicting claims | Planned |

\| Gap detection | Find missing evaluations, disconnected concepts and underexplored combinations | Planned |

\| Hypothesis generation | Produce candidate, testable research hypotheses | Planned |

\| Evidence tracing | Link every result to source papers and reasoning paths | Planned |

\| Novelty estimation | Estimate originality within the defined corpus | Planned |

\| Evaluation | Measure system quality against human judgments and baselines | Planned |

\| Dashboard | Explore graphs, gaps, contradictions and hypotheses | Planned |

**## Research Integrity Principles**

\- **\*\*Evidence before generation:\*\*** hypotheses must be grounded in extracted literature evidence.

\- **\*\*Corpus-bounded claims:\*\*** absence from the indexed corpus must not be presented as proof that nobody has studied a topic.

\- **\*\*Traceability:\*\*** generated outputs must link back to source papers, claims, and graph paths.

\- **\*\*Reproducibility:\*\*** datasets, configurations, experiments, and evaluation procedures will be versioned where legally and technically possible.

\- **\*\*Modularity:\*\*** every major component will be independently testable.

\- **\*\*Human validation:\*\*** scientific novelty and significance will ultimately require human assessment and, where applicable, experimental validation.

**## Development Philosophy**

This repository is being developed as a collaborative research project.

Each implementation stage includes:

1\. a defined research or engineering objective;

2\. a reproducible implementation;

3\. automated tests or validation criteria;

4\. documentation updates;

5\. a focused Git commit;

6\. a pull request reviewed before merging into \`main\`.

Large dependencies and advanced models will be introduced only when required by a validated stage of the pipeline.

**## Repository Structure**

\`\`\`text

ML-UNKNOWN-FINDER/

├── configs/                 # Reproducible configuration files

├── data/                    # Local datasets and derived artifacts

│   ├── raw/

│   ├── processed/

│   ├── metadata/

│   └── cache/

├── docs/                    # Architecture, research decisions and experiments

├── notebooks/               # Exploratory research notebooks

├── scripts/                 # Reproducible utility and pipeline scripts

├── src/                     # Production Python package

│   └── unknown\_finder/

│       ├── config/

│       ├── ingestion/

│       ├── parsing/

│       ├── extraction/

│       ├── knowledge\_graph/

│       ├── contradiction/

│       ├── gaps/

│       ├── hypothesis/

│       ├── evidence/

│       ├── novelty/

│       └── evaluation/

├── tests/                   # Automated tests

├── dashboard/               # Interactive research interface

├── .gitignore

├── CONTRIBUTING.md

├── environment.yml

├── requirements.txt

├── pyproject.toml

└── README.md

\`\`\`

**## Development Environment**

The project uses **\*\*Conda with Python 3.11\*\***.

Create the environment with:

\`\`\`bash

conda env create -f environment.yml

\`\`\`

Activate it:

\`\`\`bash

conda activate unknown-finder

\`\`\`

Run the test suite:

\`\`\`bash

pytest

\`\`\`

The project is developed incrementally so that dependencies are introduced only when required by implemented components.

**## Current Architecture**

**### Literature Ingestion**

The current ingestion architecture normalizes different literature providers into a common \`PaperRecord\` model.

\`\`\`text

OpenAlex ───────┐

arXiv ──────────┤

PubMed ─────────┼──→ LiteratureSource

Semantic Scholar┘            ↓

                       PaperRecord

                            ↓

                     LiteratureService

                            ↓

                       Deduplication

                            ↓

                    LiteratureCorpus

                            ↓

                    Paper Metadata Storage

\`\`\`

Implemented components include:

\- \`PaperRecord\` metadata model

\- \`LiteratureSource\` abstraction

\- OpenAlex adapter

\- arXiv adapter

\- PubMed adapter

\- Semantic Scholar adapter

\- literature service

\- metadata storage

\- corpus service

\- identifier-based deduplication

\- automated tests

**## Development Workflow**

Development uses feature branches.

\`\`\`bash

git checkout main

git pull

git checkout -b feature/\<feature-name>

\`\`\`

After implementation:

\`\`\`bash

pytest

git add .

git commit -m "feat: description"

git push -u origin feature/\<feature-name>

\`\`\`

Each completed feature is submitted as a pull request and merged into \`main\` after review.

**## Current Milestone**

**### Milestone 0 — Repository Bootstrap**

\- [x] Create GitHub repository

\- [x] Establish project vision and research principles

\- [x] Add reproducible Conda environment

\- [x] Add Python package structure

\- [x] Add testing infrastructure

\- [x] Add contribution workflow

**### Milestone 1 — Literature Ingestion Foundation**

\- [x] Literature source abstraction

\- [x] OpenAlex adapter

\- [x] arXiv adapter

\- [x] PubMed adapter

\- [x] Semantic Scholar adapter

\- [x] Paper metadata schema

\- [x] Metadata storage

\- [x] Literature service

\- [x] Corpus service

\- [x] Basic deduplication

\- [x] Identifier-based deduplication

\- [x] Automated tests

**### Remaining Literature Ingestion Work**

\- [ ] Robust metadata normalization across sources

\- [ ] Corpus-level source merging

\- [ ] Paper download pipeline

\- [ ] PDF provenance tracking

\- [ ] Rate limiting and retry policies

\- [ ] Persistent corpus registry

\- [ ] Ingestion evaluation dataset

**## Roadmap**

**### Phase 2 — Scientific Document Understanding**

**Status: In Progress**

Parse papers and extract structured scientific information.

\- [ ] PDF parsing

\- [ ] Section detection

\- [ ] Figure and table extraction

\- [ ] Reference extraction

\- [ ] Equation handling

\- [ ] Scientific entity extraction

\- [ ] Claim extraction

\- [ ] Evidence extraction

\- [ ] Limitation extraction

\- [ ] Future-work extraction

**### Phase 3 — Research Knowledge Graph**

Represent papers, claims, methods, datasets, experiments, metrics and relationships.

**### Phase 4 — Discovery Engine**

Implement:

\- contradiction detection;

\- research gap detection;

\- unexplored relationship discovery;

\- missing experiment detection.

**### Phase 5 — Hypothesis Engine**

Generate and rank candidate hypotheses with explicit evidence traces.

**### Phase 6 — Evaluation**

Build:

\- evaluation datasets;

\- baselines;

\- human evaluation protocols;

\- ablation studies;

\- reproducibility experiments.

**### Phase 7 — Research Dashboard**

Provide interactive exploration of:

\- research graphs;

\- contradictions;

\- research gaps;

\- hypotheses;

\- evidence chains;

\- novelty estimates.

**## Important Limitation**

The first version will operate on a **\*\*defined and documented literature corpus\*\***.

Statements such as:

\> "This has never been studied."

will therefore be avoided unless supported by an explicitly defined search methodology and sufficient coverage evidence.

The system should instead use language such as:

\> "No relevant work was identified within the defined search corpus and methodology."

**## Research Evaluation**

The eventual system will be evaluated using measurable criteria rather than demonstration quality alone.

Planned evaluation dimensions include:

\- literature retrieval quality;

\- metadata accuracy;

\- extraction precision and recall;

\- knowledge graph quality;

\- contradiction detection accuracy;

\- research-gap precision;

\- hypothesis quality;

\- evidence traceability;

\- novelty-ranking agreement with human evaluators;

\- reproducibility.

**## License**

License will be selected before external redistribution.