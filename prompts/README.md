# LLM Data Extraction Prompts for PMS-AOP Literature

## Overview

This directory contains the prompt templates used for LLM-based structured data extraction from PMS-based Advanced Oxidation Process (AOP) literature. These prompts were developed and validated as part of a systematic review covering 531 peer-reviewed publications (2019-2025).

## Prompt Strategies

Two extraction strategies are provided:

### 1. Direct Extraction (Single-Call)
- **File**: `direct_prompt.md`
- **Description**: Complete extraction in one LLM call
- **Use case**: Shorter papers, well-structured content
- **Pros**: Faster, lower API cost
- **Cons**: May miss details in complex papers

### 2. Multi-Stage Extraction (4-Stage)
- **Files**: `stage1_basic_info.md` → `stage2_experimental_data.md` → `stage3_mechanism.md` → `stage4_validation.md`
- **Description**: Sequential extraction with context accumulation
- **Use case**: Complex papers, papers with multiple experiments
- **Pros**: Higher accuracy, built-in validation
- **Cons**: 4× API calls, higher cost

## Stage Descriptions

| Stage | Focus | Key Fields |
|-------|-------|------------|
| Stage 1 | Basic Info | title, journal, year, DOI, system classification |
| Stage 2 | Experimental Data | reaction conditions, degradation performance |
| Stage 3 | Mechanism | reactive species, catalytic mechanism, degradation pathway |
| Stage 4 | Validation | cross-check consistency, fill gaps |

## Key Design Principles

### Anti-Hallucination Rules
```
- Use `null` for missing data - NEVER fabricate values
- Set `performed: false` if EPR/quenching not described
- Do NOT calculate or estimate unreported values
- Prefer under-reporting over false reporting
```

### Strict Type Enforcement
```json
{
  "year": 2022,                    // integer, NOT "2022"
  "synergy_observed": true,        // boolean, NOT "Yes"
  "control_experiments": [         // array of objects
    {"condition": "PMS only", "removal_percent": 19.97}
  ]
}
```

## Usage Example

### Direct Extraction (Python)
```python
import openai

with open('direct_prompt.md', 'r') as f:
    system_prompt = f.read()

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Extract data from:\n\n{paper_content}"}
    ],
    response_format={"type": "json_object"}
)

result = json.loads(response.choices[0].message.content)
```

### Multi-Stage Extraction (Python)
```python
# Stage 1
stage1_result = extract_with_prompt('stage1_basic_info.md', paper_content)

# Stage 2 (with Stage 1 context)
stage2_result = extract_with_prompt('stage2_experimental_data.md',
                                     paper_content + "\n\nPrevious extraction:\n" + stage1_result)

# Stage 3
stage3_result = extract_with_prompt('stage3_mechanism.md',
                                     paper_content + "\n\nPrevious extraction:\n" + stage2_result)

# Stage 4 (validation)
final_result = extract_with_prompt('stage4_validation.md',
                                    paper_content + "\n\nAll previous stages:\n" + combined_results)
```

## Validation Metrics

These prompts achieved the following F1 scores on a 15-paper benchmark:

| Field Category | F1 Score |
|----------------|----------|
| Core fields (title, journal, year) | 0.892 |
| Mechanism classification | 0.847 |
| Reactive species identification | 0.823 |
| Overall weighted average | 0.856 |

## Recommended LLMs

Tested with the following models (performance may vary):
- GPT-4o / GPT-4-turbo
- Claude Opus 4.5 / Sonnet 4
- Gemini 2.0 Pro
- DeepSeek-V3
- Qwen-Max

## License

These prompts are released under CC BY 4.0. Please cite the associated manuscript when using these prompts for research.

## Citation

```bibtex
@article{pms_aops_critical_review_2025,
  title={Rethinking Advanced Oxidation: Evidence-Based Analysis Challenges the Radical-Dominated Paradigm},
  journal={Environmental Science \& Technology},
  year={2025},
  doi={10.5281/zenodo.18017674}
}
```
