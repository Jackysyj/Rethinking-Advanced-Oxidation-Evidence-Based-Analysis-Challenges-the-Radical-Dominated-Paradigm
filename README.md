# Open-Source Materials for PMS-AOP Critical Review

## Rethinking Advanced Oxidation: Evidence-Based Analysis Challenges the Radical-Dominated Paradigm

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18017674.svg)](https://doi.org/10.5281/zenodo.18017674)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

## Overview

This repository contains the open-source materials accompanying our critical review on peroxymonosulfate (PMS)-based advanced oxidation processes (AOPs). The review analyzes **531 peer-reviewed publications (2019-2025)** using a validated LLM-assisted data extraction framework.

### Key Findings

- **Paradigm Shift**: Non-radical pathways increased from 35.0% to 46.0%, achieving majority status (51.0%) by 2025 (p = 0.017)
- **Singlet Oxygen Dominance**: ¹O₂ emerged as the dominant reactive species, rising from 55% to 67% prevalence
- **Catalyst-Mechanism Correlation**: Single-atom catalysts achieve 71.1% non-radical selectivity via M-N₄ sites
- **Data Gap**: 41.4% of studies lack TOC data, revealing a 40-percentage-point gap between pollutant removal (96%) and mineralization (56%)

## Repository Structure

```
open_source/
├── README.md                 # This file
├── data/                     # Aggregated datasets (CSV/JSON)
│   ├── README.md             # Data documentation
│   ├── SI_literature_full.csv         # Master dataset (531 papers)
│   ├── SI_Ch3_*.csv          # Chapter 3: Descriptive statistics
│   ├── SI_Ch4_*.csv          # Chapter 4: Mechanism trends
│   ├── SI_Ch5_*.csv          # Chapter 5: Catalyst-mechanism correlations
│   ├── SI_Ch6_*.csv          # Chapter 6: Design framework data
│   └── SI_Ch2_*.json         # Chapter 2: LLM validation metrics
├── prompts/                  # LLM extraction prompts
│   ├── README.md             # Prompt documentation
│   ├── direct_prompt.md      # Single-call extraction
│   └── stage[1-4]_*.md       # Multi-stage extraction
├── schemas/                  # Data extraction schema
│   ├── README.md             # Schema documentation
│   └── gold_standard_schema.json  # v3.0 schema
└── scripts/                  # Utility scripts
    ├── README.md             # Script documentation
    ├── generate_si_data.py   # Data aggregation script
    └── plot_config.py        # Plotting configuration
```

## Quick Start

### Load and Explore the Data

```python
import pandas as pd

# Load the master dataset
df = pd.read_csv('data/SI_literature_full.csv')

# View paradigm shift over time
trends = df.groupby(['year', 'mechanism_category']).size().unstack().fillna(0)
print(trends)

# Analyze SAC selectivity
sac = df[df['catalyst_type'] == 'SAC']
print(sac['dominant_mechanism'].value_counts(normalize=True))
```

### Use the Extraction Prompts

```python
import json

# Load the schema
with open('schemas/gold_standard_schema.json', 'r') as f:
    schema = json.load(f)

# Load the direct extraction prompt
with open('prompts/direct_prompt.md', 'r') as f:
    prompt = f.read()

# Use with your preferred LLM API
# response = llm.complete(system_prompt=prompt, user_prompt=paper_content)
```

## LLM Extraction Performance

Our multi-stage extraction pipeline achieved:

| Metric | F1 Score |
|--------|----------|
| Core fields (title, journal, year) | 0.892 |
| Mechanism classification | 0.847 |
| Reactive species identification | 0.823 |
| **Overall weighted average** | **0.856** |

## What's NOT Included

For copyright and practical reasons, the following are **not** included:

- Raw PDF files of the 531 papers
- OCR-converted markdown files
- Intermediate extraction results
- Word document generation scripts

## Citation



## License

This repository is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose

Under the following terms:
- **Attribution** — You must give appropriate credit and indicate if changes were made

## Contact

For questions or collaborations, please open an issue in this repository or contact the corresponding author.

---

*This work demonstrates the potential of LLM-assisted systematic reviews in environmental science research.*
