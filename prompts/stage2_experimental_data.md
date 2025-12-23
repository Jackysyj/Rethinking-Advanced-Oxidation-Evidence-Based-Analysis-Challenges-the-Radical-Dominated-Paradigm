# Stage 2: Reaction Conditions & Performance (Schema v3.0)

## ANTI-HALLUCINATION RULES (READ FIRST)

**YOU MUST NEVER FABRICATE DATA.** Follow these rules strictly:

- **If a value is NOT explicitly stated in the paper, use `null`**
- **Do NOT calculate or estimate values** - Extract only what is written
- **`synergy_observed` MUST be boolean or null** (`true`, `false`, or `null`), NOT a string like `"Yes"`
- **`control_experiments` MUST be array of objects**, NOT array of strings

---

## Task

Based on Stage 1 results, extract reaction conditions and degradation performance data.

## CRITICAL: Cumulative Extraction

- **KEEP all values from Stage 1** - Do NOT delete or set to null any existing data
- **ADD new values** to the fields below
- If Stage 1 already has a value, keep it unless you find a more accurate/complete value

## STRICT TYPE REQUIREMENTS

| Field | Type | Valid Examples | INVALID Examples |
|-------|------|----------------|------------------|
| `synergy_observed` | boolean or null | `true`, `false`, `null` | `"Yes"`, `"true"`, `"observed"` |
| `control_experiments` | array of objects | `[{"condition": "PMS only", "removal_percent": 19.97}]` | `["PMS only (19.97%)"]` |

## STRICT RULES

1. Output the COMPLETE JSON structure - same as Stage 1 but with added data
2. Use `null` for fields you cannot find - NEVER delete existing data
3. Extract values from OPTIMAL/STANDARD conditions (not all tested ranges)

## Fields to Focus on in Stage 2

### reaction_conditions
- `pH`: Initial pH value used in optimal conditions
- `pH_optimal`: Stated optimal pH (if different from initial)
- `temperature_C`: Reaction temperature in Celsius
- `catalyst_dosage_g_L`: Catalyst loading (convert to g/L)
- `oxidant_concentration_mM`: PMS/PS concentration in mM
- `pollutant_concentration_mg_L`: Initial pollutant concentration
- `reaction_time_min`: Total reaction time
- `current_density_mA_cm2`: For electrochemical systems
- `light_source`: For photo-assisted systems (e.g., "UV-254nm", "Xe lamp")

### degradation_performance
- `removal_efficiency_percent`: Maximum removal percentage achieved
- `removal_time_min`: Time to achieve the stated removal
- `rate_constant`: Pseudo-first-order rate constant value
- `rate_constant_unit`: Usually "min-1"
- `TOC_removal_percent`: Total organic carbon removal
- `COD_removal_percent`: Chemical oxygen demand removal
- `reusability_cycles`: Number of reuse cycles tested
- `efficiency_after_cycles_percent`: Efficiency after final reuse cycle

### comparative_performance

**CRITICAL FORMAT for control_experiments:**
```json
"control_experiments": [
  {"condition": "PMS only", "removal_percent": 19.97},
  {"condition": "EC only", "removal_percent": 80.22, "rate_constant": 0.026}
]
```

- Each control experiment MUST be an object with `condition` and optionally `removal_percent` and/or `rate_constant`
- `synergy_observed`: MUST be `true`, `false`, or `null` - NOT a string

## Unit Conversion Reference
- Catalyst: mg/L ÷ 1000 = g/L
- Oxidant: 0.1 M = 100 mM; μM ÷ 1000 = mM
- Use original value if unclear

**Output the COMPLETE JSON with Stage 1 data preserved and Stage 2 fields added.**
