# Gold Standard Schema for PMS-AOP Literature Data Extraction

## Overview

This directory contains the JSON schema used for structured data extraction from PMS-based Advanced Oxidation Process (AOP) literature. The schema defines the standardized data structure for capturing experimental conditions, degradation performance, reactive species, and catalytic mechanisms.

## Schema Version

**Current Version**: v3.0 (2025-11-30)

Key improvements in v3.0:
- Strict type enforcement (boolean vs. string)
- Standardized `control_experiments` format (array of objects)
- Enhanced anti-hallucination guidelines
- Clear `null` handling for missing data

## Schema Structure

```
gold_standard_schema.json
├── paper_info              # Title, journal, year, DOI
├── experimental_system     # Pollutant, catalyst, oxidant, activation method
├── reaction_conditions     # pH, temperature, dosage, time, etc.
├── degradation_performance # Removal efficiency, rate constant, TOC, reusability
├── reactive_species        # Identified ROS, quenching experiments, EPR analysis
├── catalytic_mechanism     # Radical/non-radical pathways, active sites
├── degradation_pathway     # Intermediates, attack sites, final products
├── system_classification   # Heterogeneous/photo/electrochemical
└── comparative_performance # Control experiments, synergy
```

## Key Fields Explained

### experimental_system

| Field | Type | Options |
|-------|------|---------|
| `target_pollutant.category` | string | `antibiotic`, `dye`, `phenolic compound`, `pharmaceutical`, `pesticide`, `other` |
| `catalyst.type` | string | `MOF-derived`, `biochar`, `metal oxide`, `perovskite`, `SAC`, `carbon-based`, `electrode`, `other` |
| `oxidant` | string | `PMS`, `PS`, `H2O2`, or combination |
| `activation_method` | string | `heterogeneous catalysis`, `UV`, `visible light`, `electrochemical`, `thermal`, `homogeneous` |

### reactive_species

| Field | Type | Standard Notation |
|-------|------|-------------------|
| `identified_species` | array | `SO4•−`, `•OH`, `1O2`, `O2•−`, `h+`, `e-` |
| `dominant_species` | string | Main contributing ROS |
| `quenching_experiments.performed` | boolean | **Must be false if not described** |
| `EPR_analysis.performed` | boolean | **Must be false if no EPR data** |

### Common Scavenger-ROS Pairs

| Scavenger | Target ROS |
|-----------|------------|
| Methanol | •OH + SO4•− |
| TBA (tert-butanol) | •OH |
| FFA (furfuryl alcohol) | ¹O₂ |
| L-histidine | ¹O₂ |
| p-BQ (p-benzoquinone) | O2•− |
| EDTA | h+ |

### catalytic_mechanism

| Field | Type | Values |
|-------|------|--------|
| `radical_pathway` | boolean/null | `true`, `false`, or `null` |
| `non_radical_pathway` | boolean/null | `true`, `false`, or `null` |
| `dominant_mechanism` | string/null | `radical`, `non-radical`, `both`, or `null` |

### comparative_performance

**CRITICAL**: `control_experiments` must be an array of objects:

```json
{
  "control_experiments": [
    {"condition": "PMS only", "removal_percent": 19.97},
    {"condition": "catalyst only", "removal_percent": 5.2},
    {"condition": "EC only", "removal_percent": 80.22, "rate_constant": 0.033}
  ],
  "synergy_observed": true
}
```

**NOT** an array of strings like `["PMS only (19.97%)", "EC only (80.22%)"]`.

## Type Requirements

| Field | Correct Type | Incorrect Examples |
|-------|--------------|-------------------|
| `year` | integer | `"2022"` (string) |
| `synergy_observed` | boolean/null | `"Yes"`, `"true"` |
| `radical_pathway` | boolean/null | `"free radical"` |
| `inhibition_percent` | number/null | `"70%"`, `"significant"` |

## Usage with LLMs

When using this schema with LLMs:

1. **Always provide the schema** in the system prompt
2. **Enforce JSON output** using `response_format={"type": "json_object"}`
3. **Validate types** after extraction
4. **Use null** for any unreported values

```python
import json

def validate_extraction(data):
    """Basic validation for extracted data."""
    errors = []

    # Check year is integer
    if data.get('paper_info', {}).get('year'):
        if not isinstance(data['paper_info']['year'], int):
            errors.append("year must be integer")

    # Check boolean fields
    for field in ['synergy_observed', 'radical_pathway', 'non_radical_pathway']:
        # ... validation logic

    # Check control_experiments format
    ctrl = data.get('comparative_performance', {}).get('control_experiments', [])
    if ctrl and isinstance(ctrl[0], str):
        errors.append("control_experiments must be array of objects")

    return errors
```

## License

This schema is released under CC BY 4.0. Please cite the associated manuscript when using this schema.

## Citation

```bibtex
@article{pms_aops_critical_review_2025,
  title={Rethinking Advanced Oxidation: Evidence-Based Analysis Challenges the Radical-Dominated Paradigm},
  journal={Environmental Science \& Technology},
  year={2025},
  doi={10.5281/zenodo.18017674}
}
```
