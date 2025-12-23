# PMS-AOP Literature Data Extraction (Schema v3.0)

## CRITICAL RULES - READ CAREFULLY

### 1. ANTI-HALLUCINATION RULES (MOST IMPORTANT)

**YOU MUST NEVER FABRICATE DATA.** Follow these rules strictly:

- **If a value is NOT explicitly stated in the paper, use `null`**
- **If EPR/ESR analysis was NOT performed, set `EPR_analysis.performed: false`**
- **If quenching experiments were NOT described, set `quenching_experiments.performed: false`**
- **Do NOT calculate or estimate values** - Extract only what is written
- **Do NOT assume inhibition percentages** if not explicitly reported
- **If uncertain, use `null`** - Wrong data is worse than missing data

### 2. STRICT TYPE REQUIREMENTS

These fields MUST use the exact types specified:

| Field | Type | Valid Examples | INVALID Examples |
|-------|------|----------------|------------------|
| `year` | integer | `2022` | `"2022"` |
| `synergy_observed` | boolean or null | `true`, `false`, `null` | `"Yes"`, `"true"` |
| `radical_pathway` | boolean or null | `true`, `false`, `null` | `"free radical"` |
| `non_radical_pathway` | boolean or null | `true`, `false`, `null` | `"electron transfer"` |
| `control_experiments` | array of objects | `[{"condition": "PMS only", "removal_percent": 19.97}]` | `["PMS only (19.97%)"]` |

### 3. OUTPUT FORMAT

- **Output ONLY valid JSON** - No markdown code blocks (no ```json)
- **No explanations or comments** before or after the JSON
- **Keep exact field names** - Do not rename any field
- **Keep exact structure** - Do not add or remove fields

---

## JSON TEMPLATE

```json
{
  "paper_info": {
    "title": null,
    "journal": null,
    "year": null,
    "doi": null
  },
  "experimental_system": {
    "target_pollutant": {
      "name": null,
      "abbreviation": null,
      "category": null
    },
    "catalyst": {
      "name": null,
      "type": null,
      "synthesis_method": null
    },
    "oxidant": null,
    "activation_method": null,
    "system_type": null
  },
  "reaction_conditions": {
    "pH": null,
    "pH_optimal": null,
    "temperature_C": null,
    "catalyst_dosage_g_L": null,
    "oxidant_concentration_mM": null,
    "pollutant_concentration_mg_L": null,
    "reaction_time_min": null,
    "current_density_mA_cm2": null,
    "light_source": null
  },
  "degradation_performance": {
    "removal_efficiency_percent": null,
    "removal_time_min": null,
    "rate_constant": null,
    "rate_constant_unit": "min-1",
    "TOC_removal_percent": null,
    "COD_removal_percent": null,
    "reusability_cycles": null,
    "efficiency_after_cycles_percent": null
  },
  "reactive_species": {
    "identified_species": [],
    "dominant_species": null,
    "identification_methods": [],
    "quenching_experiments": {
      "performed": false,
      "scavengers_used": [],
      "results": []
    },
    "EPR_analysis": {
      "performed": false,
      "spin_trap": null,
      "detected_signals": []
    }
  },
  "catalytic_mechanism": {
    "radical_pathway": null,
    "non_radical_pathway": null,
    "dominant_mechanism": null,
    "key_active_sites": [],
    "mechanism_description": null
  },
  "degradation_pathway": {
    "pathway_proposed": false,
    "identification_method": null,
    "num_intermediates": null,
    "main_attack_sites": [],
    "reaction_types": [],
    "final_products": []
  },
  "system_classification": {
    "is_heterogeneous_catalysis": false,
    "is_photo_assisted": false,
    "is_electrochemical": false,
    "primary_classification": null
  },
  "comparative_performance": {
    "control_experiments": [],
    "synergy_observed": null
  }
}
```

---

## FIELD DEFINITIONS

### experimental_system
- `target_pollutant.category`: One of `"antibiotic"`, `"dye"`, `"phenolic compound"`, `"pharmaceutical"`, `"pesticide"`, `"other"`
- `catalyst.type`: One of `"MOF-derived"`, `"biochar"`, `"metal oxide"`, `"perovskite"`, `"SAC"`, `"carbon-based"`, `"electrode"`, `"other"`
- `oxidant`: One of `"PMS"`, `"PS"`, `"H2O2"`, or combination
- `activation_method`: One of `"heterogeneous catalysis"`, `"UV"`, `"visible light"`, `"electrochemical"`, `"thermal"`, `"homogeneous"`
- `system_type`: Format as `"catalyst/PMS"`, `"UV/PMS"`, `"electro/PMS"`, etc.

### reactive_species
- `identified_species`: Use standard notation: `"SO4•−"`, `"•OH"`, `"1O2"`, `"O2•−"`, `"h+"`, `"e-"`
- `quenching_experiments.results`: **MUST be array of objects with this exact format:**
  ```json
  [
    {"scavenger": "methanol", "target_ROS": "•OH + SO4•−", "inhibition_percent": 70, "effect": "significant inhibition"},
    {"scavenger": "TBA", "target_ROS": "•OH", "inhibition_percent": null, "effect": "strong inhibition"}
  ]
  ```
- Common scavenger-ROS pairs:
  - `"methanol"` → `"•OH + SO4•−"`
  - `"TBA"` or `"tert-butanol"` → `"•OH"`
  - `"FFA"` or `"furfuryl alcohol"` → `"1O2"`
  - `"p-BQ"` or `"p-benzoquinone"` → `"O2•−"`
  - `"L-histidine"` → `"1O2"`
  - `"EDTA"` → `"h+"`

### catalytic_mechanism
- `radical_pathway`: `true` if radical mechanism is involved, `false` if not, `null` if not discussed
- `non_radical_pathway`: `true` if non-radical mechanism (electron transfer, 1O2, surface complex) is involved
- `dominant_mechanism`: One of `"radical"`, `"non-radical"`, `"both"`, or `null`

### comparative_performance
- **`control_experiments` MUST be array of objects:**
  ```json
  [
    {"condition": "PMS only", "removal_percent": 19.97},
    {"condition": "EC only", "removal_percent": 80.22}
  ]
  ```
  If rate constant is reported, add it: `{"condition": "PMS only", "removal_percent": 19.97, "rate_constant": 0.0033}`

- **`synergy_observed` MUST be boolean or null:** `true`, `false`, or `null`

---

## EXTRACTION CHECKLIST

Before outputting, verify:

1. ✓ `year` is integer, not string
2. ✓ `synergy_observed` is boolean or null, not string
3. ✓ `radical_pathway` and `non_radical_pathway` are boolean or null
4. ✓ `control_experiments` is array of objects, not array of strings
5. ✓ `EPR_analysis.performed` is false if no EPR data in paper
6. ✓ All `inhibition_percent` values are from paper, not estimated
7. ✓ No fabricated data - use null for missing values

---

**Now extract data from the paper. Output ONLY the JSON object (no markdown, no explanations).**
