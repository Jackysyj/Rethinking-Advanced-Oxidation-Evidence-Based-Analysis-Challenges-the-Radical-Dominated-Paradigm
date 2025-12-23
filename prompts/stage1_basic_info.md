# Stage 1: Paper Info & System Classification (Schema v3.0)

## ANTI-HALLUCINATION RULES (READ FIRST)

**YOU MUST NEVER FABRICATE DATA.** Follow these rules strictly:

- **If a value is NOT explicitly stated in the paper, use `null`**
- **Do NOT guess or infer values** - Extract only what is written
- **`year` MUST be an integer** (e.g., `2022`), NOT a string (e.g., `"2022"`)
- **If uncertain, use `null`** - Wrong data is worse than missing data

---

## Task

Extract basic paper information and classify the experimental system.

## STRICT RULES

1. Output ONLY the JSON structure below - NO additional fields
2. Use `null` for missing data - NEVER leave empty or omit fields
3. Extract ONLY explicitly stated information
4. **`year` must be integer type**, not string

## Output JSON (Fill in values, keep ALL fields)

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
  "system_classification": {
    "is_heterogeneous_catalysis": false,
    "is_photo_assisted": false,
    "is_electrochemical": false,
    "primary_classification": null
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
  "comparative_performance": {
    "control_experiments": [],
    "synergy_observed": null
  }
}
```

## Field Guidelines for Stage 1

Focus on extracting:
- **paper_info**: Title, journal, year (as integer!), DOI from the paper header
- **experimental_system**: Pollutant name/category, catalyst name/type, oxidant, activation method
- **system_classification**: Determine if heterogeneous/photo/electrochemical based on the system description

**Category options for target_pollutant**: `"antibiotic"`, `"dye"`, `"phenolic compound"`, `"pharmaceutical"`, `"pesticide"`, `"other"`

**Type options for catalyst**: `"MOF-derived"`, `"biochar"`, `"metal oxide"`, `"perovskite"`, `"SAC"`, `"carbon-based"`, `"electrode"`, `"other"`

Leave other sections with `null` or empty arrays - they will be filled in later stages.

**Output ONLY the JSON object (no markdown code blocks, no explanations).**
