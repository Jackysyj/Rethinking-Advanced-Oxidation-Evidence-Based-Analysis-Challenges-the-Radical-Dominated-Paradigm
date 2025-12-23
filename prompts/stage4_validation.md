# Stage 4: Validation & Final Compilation (Schema v3.0)

## ANTI-HALLUCINATION RULES (READ FIRST)

**BEFORE OUTPUTTING, VERIFY:**

1. ✓ `year` is integer, NOT string (e.g., `2022` not `"2022"`)
2. ✓ `synergy_observed` is boolean or null, NOT string (e.g., `true` not `"Yes"`)
3. ✓ `radical_pathway` and `non_radical_pathway` are boolean or null
4. ✓ `control_experiments` is array of objects, NOT array of strings
5. ✓ `EPR_analysis.performed` is `false` if NO EPR data in paper
6. ✓ All `inhibition_percent` values are from paper, NOT estimated
7. ✓ No fabricated data - use `null` for missing values

---

## Task

Validate all extracted data from Stages 1-3 and output the final JSON.

## CRITICAL RULES

### DO:
1. **PRESERVE all data** from previous stages - Do NOT delete any values
2. **Verify type compliance** - Fix any type errors (string → boolean, etc.)
3. **Fill gaps** if you notice obvious missing data that was mentioned earlier
4. **Ensure required booleans** have true/false values (not null)

### DO NOT:
1. **DO NOT set values to null** if they were extracted in previous stages
2. **DO NOT add new fields** not in the schema
3. **DO NOT change correctly extracted values**
4. **DO NOT fabricate data** that wasn't in the original paper

## Type Validation Checklist

| Field | Required Type | Fix If Wrong |
|-------|--------------|--------------|
| `paper_info.year` | integer | `"2022"` → `2022` |
| `synergy_observed` | boolean/null | `"Yes"` → `true`, `"No"` → `false` |
| `radical_pathway` | boolean/null | `"free radical"` → `true` |
| `non_radical_pathway` | boolean/null | `"electron transfer"` → `true` |
| `control_experiments` | array of objects | Convert strings to objects |

### control_experiments Format Fix

**WRONG:**
```json
"control_experiments": ["PMS only (19.97%)", "EC only (80.22%)"]
```

**CORRECT:**
```json
"control_experiments": [
  {"condition": "PMS only", "removal_percent": 19.97},
  {"condition": "EC only", "removal_percent": 80.22}
]
```

## Validation Checklist

### Required Fields (must not be null)
- `paper_info.title`
- `experimental_system.oxidant`
- `experimental_system.activation_method`
- `experimental_system.system_type`
- `reactive_species.identified_species` (at least one item if ROS were identified)
- `system_classification.primary_classification`

### Boolean Fields (must be true/false, not null)
- `system_classification.is_heterogeneous_catalysis`
- `system_classification.is_photo_assisted`
- `system_classification.is_electrochemical`
- `reactive_species.quenching_experiments.performed`
- `reactive_species.EPR_analysis.performed`
- `degradation_pathway.pathway_proposed`

### Numeric Sanity Checks
- `removal_efficiency_percent`: 0-100
- `rate_constant`: positive number, typically 0.001-1 for min-1
- `pH`: 1-14
- `temperature_C`: typically 20-80
- `reusability_cycles`: positive integer

## Final JSON Template

Output the complete JSON with this exact structure:

```json
{
  "paper_info": {
    "title": "...",
    "journal": "...",
    "year": 2022,
    "doi": "..."
  },
  "experimental_system": {
    "target_pollutant": {
      "name": "...",
      "abbreviation": "...",
      "category": "..."
    },
    "catalyst": {
      "name": "...",
      "type": "...",
      "synthesis_method": "..."
    },
    "oxidant": "...",
    "activation_method": "...",
    "system_type": "..."
  },
  "reaction_conditions": {
    "pH": 3,
    "pH_optimal": 3,
    "temperature_C": null,
    "catalyst_dosage_g_L": null,
    "oxidant_concentration_mM": 5,
    "pollutant_concentration_mg_L": 30,
    "reaction_time_min": 60,
    "current_density_mA_cm2": 30,
    "light_source": null
  },
  "degradation_performance": {
    "removal_efficiency_percent": 98.07,
    "removal_time_min": 60,
    "rate_constant": 0.066,
    "rate_constant_unit": "min-1",
    "TOC_removal_percent": null,
    "COD_removal_percent": 56.83,
    "reusability_cycles": 5,
    "efficiency_after_cycles_percent": 95.31
  },
  "reactive_species": {
    "identified_species": ["•OH", "SO4•−"],
    "dominant_species": "•OH",
    "identification_methods": ["quenching experiments"],
    "quenching_experiments": {
      "performed": true,
      "scavengers_used": ["methanol", "TBA"],
      "results": [
        {"scavenger": "methanol", "target_ROS": "•OH + SO4•−", "inhibition_percent": 70, "effect": "significant inhibition"},
        {"scavenger": "TBA", "target_ROS": "•OH", "inhibition_percent": null, "effect": "strong inhibition"}
      ]
    },
    "EPR_analysis": {
      "performed": false,
      "spin_trap": null,
      "detected_signals": []
    }
  },
  "catalytic_mechanism": {
    "radical_pathway": true,
    "non_radical_pathway": true,
    "dominant_mechanism": "both",
    "key_active_sites": ["PbO2 surface"],
    "mechanism_description": "..."
  },
  "degradation_pathway": {
    "pathway_proposed": true,
    "identification_method": "LC-MS",
    "num_intermediates": 9,
    "main_attack_sites": ["β-lactam ring", "amide group"],
    "reaction_types": ["hydroxylation", "ring opening"],
    "final_products": ["CO2", "H2O"]
  },
  "system_classification": {
    "is_heterogeneous_catalysis": false,
    "is_photo_assisted": false,
    "is_electrochemical": true,
    "primary_classification": "electrochemical"
  },
  "comparative_performance": {
    "control_experiments": [
      {"condition": "PMS only", "removal_percent": 19.97},
      {"condition": "EC only", "removal_percent": 80.22}
    ],
    "synergy_observed": true
  }
}
```

## Final Check

Before outputting, verify:
1. All data from Stages 1-3 is preserved
2. No extra fields added
3. All type requirements are met (integers, booleans, arrays of objects)
4. Arrays are `[]` if empty (not null)
5. No fabricated data

**Output ONLY the final validated JSON object.**
