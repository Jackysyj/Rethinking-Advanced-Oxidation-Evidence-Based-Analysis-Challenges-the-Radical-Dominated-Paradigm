# Stage 3: ROS Identification & Mechanism (Schema v3.0)

## ANTI-HALLUCINATION RULES (READ FIRST)

**YOU MUST NEVER FABRICATE DATA.** Follow these rules strictly:

- **If EPR/ESR analysis was NOT performed, set `EPR_analysis.performed: false`**
- **If quenching experiments were NOT described, set `quenching_experiments.performed: false`**
- **Do NOT assume inhibition percentages** if not explicitly reported - use `null`
- **`radical_pathway` and `non_radical_pathway` MUST be boolean or null**, NOT strings
- **If uncertain, use `null`** - Wrong data is worse than missing data

---

## Task

Based on Stage 1-2 results, extract ROS identification data and catalytic mechanism details.

## CRITICAL: Cumulative Extraction

- **KEEP all values from Stage 1-2** - Do NOT delete any existing data
- **ADD new values** to the fields below
- This stage focuses on the MOST IMPORTANT data for the research paper

## STRICT TYPE REQUIREMENTS

| Field | Type | Valid Examples | INVALID Examples |
|-------|------|----------------|------------------|
| `radical_pathway` | boolean or null | `true`, `false`, `null` | `"free radical"`, `"yes"` |
| `non_radical_pathway` | boolean or null | `true`, `false`, `null` | `"electron transfer"` |
| `quenching_experiments.results` | array of objects | See format below | Array of strings |
| `inhibition_percent` | number or null | `70`, `null` | `"70%"`, `"significant"` |

## STRICT RULES

1. Output the COMPLETE JSON structure with all previous data preserved
2. Pay SPECIAL ATTENTION to quenching experiments - extract EACH scavenger individually
3. For EPR analysis, note the spin trap and ALL detected signals
4. **ONLY extract inhibition_percent if EXPLICITLY stated as a number in the paper**

## Fields to Focus on in Stage 3

### reactive_species (CRITICAL - Core Data)

#### identified_species
Array of ROS mentioned: `["SO4•−", "•OH", "1O2", "O2•−"]`
- Use standard notation: SO4•−, •OH, 1O2, O2•−, h+, e-

#### dominant_species
The main contributing ROS stated by authors (e.g., "SO4•−" or "1O2")

#### identification_methods
Array: `["EPR", "quenching experiments", "probe compounds"]`

#### quenching_experiments (VERY IMPORTANT)

**REQUIRED FORMAT:**
```json
{
  "performed": true,
  "scavengers_used": ["methanol", "TBA", "FFA", "p-BQ"],
  "results": [
    {
      "scavenger": "methanol",
      "target_ROS": "•OH + SO4•−",
      "inhibition_percent": 65,
      "effect": "significant inhibition"
    },
    {
      "scavenger": "TBA",
      "target_ROS": "•OH",
      "inhibition_percent": null,
      "effect": "slight inhibition"
    }
  ]
}
```

**CRITICAL:**
- `inhibition_percent` should be `null` if not explicitly stated as a number
- Do NOT estimate or calculate inhibition percentages

**Common Scavenger-ROS Mapping:**
- methanol/EtOH → •OH + SO4•−
- TBA (tert-butanol) → •OH
- FFA (furfuryl alcohol) → 1O2
- L-histidine → 1O2
- p-BQ (p-benzoquinone) → O2•−
- TEMPOL → O2•−
- NaN3 → 1O2

#### EPR_analysis

**CRITICAL: If NO EPR/ESR data in paper, use:**
```json
{
  "performed": false,
  "spin_trap": null,
  "detected_signals": []
}
```

**If EPR was performed:**
```json
{
  "performed": true,
  "spin_trap": "DMPO",
  "detected_signals": ["DMPO-OH", "DMPO-SO4"]
}
```

- DMPO → detects •OH (DMPO-OH) and SO4•− (DMPO-SO4)
- TEMP → detects 1O2 (TEMPO or TEMP-1O2)

### catalytic_mechanism

- `radical_pathway`: `true` if radical pathway is involved, `false` if not, `null` if not discussed
- `non_radical_pathway`: `true` if non-radical pathway is involved, `false` if not, `null` if not discussed
- `dominant_mechanism`: One of `"radical"`, `"non-radical"`, `"both"`, or `null`
- `key_active_sites`: Array like `["Fe2+/Fe3+", "oxygen vacancies", "pyridinic N"]`
- `mechanism_description`: Brief description of the proposed mechanism

### degradation_pathway

- `pathway_proposed`: `true` if paper proposes degradation pathway, `false` otherwise
- `identification_method`: e.g., "LC-MS", "GC-MS", "HPLC-QTOF"
- `num_intermediates`: Number of intermediates identified (integer or null)
- `main_attack_sites`: Array like `["amino group", "benzene ring", "β-lactam ring"]`
- `reaction_types`: Array like `["hydroxylation", "deamination", "ring opening"]`
- `final_products`: Array like `["CO2", "H2O", "NH4+", "SO42-"]`

**Output the COMPLETE JSON with all Stage 1-2 data preserved and Stage 3 fields added.**
