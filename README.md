# Data-Driven-Evidence-for-the-Non-radical-Paradigm-Shift-in-PMS-Based-AOPs
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18017674.svg)](https://doi.org/10.5281/zenodo.18017674)

This directory contains the data supporting the Critical Review manuscript. Raw extracted JSON files are retained for future research and not included in this release.

## 📂 Dataset Structure

The data is organized by the analytical chapters of the review. The core master dataset is `SI_literature_full.csv`.

### 1. Master Dataset
*   **`SI_literature_full.csv`**: The complete, row-level dataset containing all extracted fields for every paper analyzed.
    *   **Key Columns**: `paper_id`, `year`, `catalyst_type`, `pollutant_category`, `mechanism_category` (Radical/Non-radical/Both), `dominant_species`, `removal_efficiency`, `active_sites`, etc.
*   **`SI_literature_list.csv`**: A simplified list of all diverse literature sources included in the review.

### 2. Descriptive Statistics (Chapter 3)
Files related to the general landscape of the field (pollutants, catalysts, and publication volume).
*   `SI_Ch3_basic_statistics.csv`: Summary counts (total papers, missing data rates).
*   `SI_Ch3_catalyst_distribution.csv`: Distribution of catalyst types (e.g., MOF-derived, SACs, Metal Oxides).
*   `SI_Ch3_pollutant_distribution.csv`: Breakdown of target pollutants (Antibiotics, Phenolics, etc.).

### 3. Mechanism & Paradigm Shift (Chapter 4)
Files tracking the temporal evolution of activation mechanisms and reactive species.
*   **`SI_Ch4_mechanism_by_year.csv`**: Annual counts of Radical vs. Non-radical vs. Dual mechanisms (Evidence of the paradigm shift).
*   **`SI_Ch4_species_by_period.csv`**: Frequency of dominant reactive species (¹O₂, HVM, •OH, etc.) over time.
*   **`SI_Ch4_mechanism_species_flow.csv`**: Data for Sankey diagrams linking mechanism categories to specific reactive species.

### 4. Catalyst-Mechanism Correlations (Chapter 5)
Detailed matrices linking material properties to mechanistic outcomes.
*   `SI_Ch5_catalyst_mechanism_matrix.csv`: Correlation matrix showing which catalysts favor which mechanisms.
*   `SI_Ch5_sac_active_sites.csv`: Analysis specific to Single-Atom Catalysts (SACs) and their coordination environments (e.g., Fe-N4, Co-N4).
*   `SI_Ch5_defect_mechanism.csv`: Impact of defects (general) on mechanism selection.
*   `SI_Ch5_n_doping_mechanism.csv`: Specific analysis of Nitrogen doping types (Graphitic, Pyridinic, Pyrrolic).
*   `SI_Ch5_hvm_by_catalyst.csv`: Which catalysts are most likely to generate High-Valent Metal (HVM) species.

### 5. Design Framework & Environmental Factors (Chapter 6)
Data supporting the rational design guidelines.
*   `SI_Ch6_design_framework_summary.csv`: Summary data for the hierarchical decision tree (Catalyst -> Active Site -> Species).
*   `SI_Ch6_environmental_effects.csv`: Aggregated data on the effects of water matrix parameters (pH, anions).
*   `SI_Ch6_n_doping_theory_experiment.csv`: Data contrasting theoretical predictions vs. experimental realities of N-doping.

### 6. Evaluation Metrics
*   `SI_Ch2_evaluation_detailed.json` & `SI_Ch2_per_paper_metrics.json`: Validation metrics for the LLM extraction pipeline (Precision/Recall/F1 scores compared to human ground truth).

---
