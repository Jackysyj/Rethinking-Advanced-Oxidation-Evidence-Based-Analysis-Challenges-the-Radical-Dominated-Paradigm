#!/usr/bin/env python3
"""
Generate Open-Source Aggregated Data Files
For PMS-AOPs Critical Review Supplementary Materials

Outputs CSV files containing only the aggregated statistics used in the paper.
Raw JSON files are NOT included in open-source release.

Author: PMS-AOPs Critical Review Team
Date: 2025-12-18
"""

import json
import os
import csv
from pathlib import Path
from collections import defaultdict, Counter

# =============================================================================
# Configuration
# =============================================================================

# NOTE: Adjust these paths based on your project structure
# JSON_DIR should point to your extracted JSON data directory
# OUTPUT_DIR is where the aggregated CSV files will be saved

BASE_DIR = Path(__file__).parent.parent
JSON_DIR = BASE_DIR / "raw_json"  # Adjust to your JSON data location (not provided in open-source)
OUTPUT_DIR = BASE_DIR / "data"  # Output to the data directory

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# =============================================================================
# Species Normalization (same as 02_fig4_paradigm_shift.py)
# =============================================================================

def normalize_species(s):
    """Normalize species names to standard categories."""
    if not s:
        return None
    s_lower = s.lower()

    # Singlet oxygen
    if '1o2' in s_lower or 'singlet' in s_lower:
        return '1O2'

    # High-valent metal species (expanded coverage)
    elif 'fe(iv)' in s_lower or 'fe(v)' in s_lower or 'ferryl' in s_lower or 'feiv' in s_lower:
        return 'HVM'
    elif 'co(iv)' in s_lower or 'co(v)' in s_lower or 'co=' in s_lower or 'co4+' in s_lower:
        return 'HVM'
    elif 'cu(iii)' in s_lower or 'cu3+' in s_lower or 'cu(ii)' in s_lower:
        return 'HVM'
    elif 'mn(iv)' in s_lower or 'mn(v)' in s_lower or 'mn(iii)' in s_lower:
        return 'HVM'
    elif 'ni(iii)' in s_lower or 'ni(iv)' in s_lower:
        return 'HVM'
    elif 'high-valent' in s_lower or 'hvm' in s_lower:
        return 'HVM'
    elif 'miv(o)' in s_lower or 'mv(o)' in s_lower or 'm(iv)' in s_lower:
        return 'HVM'

    # Mixed radicals -> Other
    elif 'so4' in s_lower and ('oh' in s_lower or '•oh' in s_lower):
        return 'Other'
    elif 'so4' in s_lower and '1o2' in s_lower:
        return 'Other'
    elif 'oh' in s_lower and '1o2' in s_lower:
        return 'Other'

    # Sulfate radical
    elif 'so4' in s_lower:
        return 'SO4'

    # Hydroxyl radical
    elif 'oh' in s_lower:
        return 'OH'

    # Superoxide radical
    elif 'o2•' in s_lower or 'superoxide' in s_lower or 'o2.-' in s_lower:
        return 'O2'

    else:
        return 'Other'


def normalize_catalyst_type(cat_type):
    """Normalize catalyst type names."""
    if not cat_type:
        return None
    cat_type = cat_type.strip()
    if 'MOF' in cat_type.upper() or 'metal-organic' in cat_type.lower():
        return 'MOF-derived'
    elif 'SAC' in cat_type.upper() or 'single atom' in cat_type.lower() or 'single-atom' in cat_type.lower():
        return 'SAC'
    elif 'biochar' in cat_type.lower():
        return 'Biochar'
    elif 'oxide' in cat_type.lower() or 'metal oxide' in cat_type.lower():
        return 'Metal oxide'
    elif 'carbon' in cat_type.lower() and 'biochar' not in cat_type.lower():
        return 'Carbon-based'
    elif 'perovskite' in cat_type.lower():
        return 'Perovskite'
    return 'Other'


def normalize_pollutant_category(category):
    """Normalize pollutant category names."""
    if not category:
        return None
    category = category.strip()
    if 'antibiotic' in category.lower():
        return 'Antibiotic'
    elif 'phenol' in category.lower():
        return 'Phenolic compound'
    elif 'dye' in category.lower():
        return 'Dye'
    elif 'pharmac' in category.lower():
        return 'Pharmaceutical'
    elif 'pestic' in category.lower():
        return 'Pesticide'
    return 'Other'


# =============================================================================
# Data Loading
# =============================================================================

def load_all_data():
    """Load all extracted JSON files."""
    data = []
    for f in os.listdir(JSON_DIR):
        if f.endswith('.json'):
            with open(JSON_DIR / f, 'r') as file:
                try:
                    d = json.load(file)
                    if 'result' in d and d.get('success'):
                        data.append(d['result'])
                except:
                    pass
    print(f"Loaded {len(data)} papers")
    return data


# =============================================================================
# Data Generation Functions
# =============================================================================

def generate_mechanism_by_year(data):
    """Generate mechanism_by_year.csv"""
    mech_by_year = defaultdict(lambda: defaultdict(int))

    for d in data:
        year = d.get('paper_info', {}).get('year')
        mech = d.get('catalytic_mechanism', {}).get('dominant_mechanism')
        if year and mech:
            mech_by_year[year][mech] += 1

    # Write CSV
    output_path = OUTPUT_DIR / "mechanism_by_year.csv"
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['year', 'non_radical', 'both', 'radical', 'total'])

        for year in sorted(mech_by_year.keys()):
            row = [
                year,
                mech_by_year[year].get('Non-radical', 0),
                mech_by_year[year].get('Both', 0),
                mech_by_year[year].get('Radical', 0),
                sum(mech_by_year[year].values())
            ]
            writer.writerow(row)

    print(f"Saved: {output_path}")
    return mech_by_year


def generate_species_by_period(data):
    """Generate species_by_period.csv"""
    def get_period(year):
        if year <= 2021:
            return '2019-2021'
        else:
            return str(year)

    species_by_period = defaultdict(lambda: defaultdict(int))

    for d in data:
        year = d.get('paper_info', {}).get('year')
        species = d.get('reactive_species', {}).get('dominant_species')
        if year and species:
            period = get_period(year)
            norm_species = normalize_species(species)
            if norm_species:
                species_by_period[period][norm_species] += 1

    # Write CSV
    output_path = OUTPUT_DIR / "species_by_period.csv"
    periods = ['2019-2021', '2022', '2023', '2024', '2025']
    species_cols = ['1O2', 'HVM', 'SO4', 'OH', 'O2', 'Other']

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['period'] + species_cols + ['total'])

        for period in periods:
            row = [period]
            total = 0
            for sp in species_cols:
                count = species_by_period[period].get(sp, 0)
                row.append(count)
                total += count
            row.append(total)
            writer.writerow(row)

    print(f"Saved: {output_path}")
    return species_by_period


def generate_mechanism_species_flow(data):
    """Generate mechanism_species_flow.csv"""
    mech_species = defaultdict(lambda: defaultdict(int))

    for d in data:
        mech = d.get('catalytic_mechanism', {}).get('dominant_mechanism')
        species = d.get('reactive_species', {}).get('dominant_species')
        if mech and species:
            norm_species = normalize_species(species)
            if norm_species:
                mech_species[mech][norm_species] += 1

    # Calculate totals for percentages
    mech_totals = {m: sum(mech_species[m].values()) for m in mech_species}

    # Write CSV
    output_path = OUTPUT_DIR / "mechanism_species_flow.csv"
    mechanisms = ['Non-radical', 'Both', 'Radical']
    species_cols = ['1O2', 'HVM', 'SO4', 'OH', 'O2', 'Other']

    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['mechanism', 'species', 'count', 'percentage'])

        for mech in mechanisms:
            total = mech_totals.get(mech, 0)
            for sp in species_cols:
                count = mech_species[mech].get(sp, 0)
                pct = count / total * 100 if total > 0 else 0
                writer.writerow([mech, sp, count, f"{pct:.1f}"])

    print(f"Saved: {output_path}")
    return mech_species


def generate_catalyst_distribution(data):
    """Generate catalyst_distribution.csv"""
    catalyst_counts = Counter()

    for d in data:
        cat_type = d.get('experimental_system', {}).get('catalyst', {}).get('type')
        if cat_type:
            norm_type = normalize_catalyst_type(cat_type)
            if norm_type:
                catalyst_counts[norm_type] += 1

    # Write CSV
    output_path = OUTPUT_DIR / "catalyst_distribution.csv"
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['catalyst_type', 'count', 'percentage'])

        total = sum(catalyst_counts.values())
        for cat_type, count in catalyst_counts.most_common():
            pct = count / total * 100 if total > 0 else 0
            writer.writerow([cat_type, count, f"{pct:.1f}"])

    print(f"Saved: {output_path}")
    return catalyst_counts


def generate_pollutant_distribution(data):
    """Generate pollutant_distribution.csv"""
    pollutant_counts = Counter()

    for d in data:
        category = d.get('experimental_system', {}).get('target_pollutant', {}).get('category')
        if category:
            norm_cat = normalize_pollutant_category(category)
            if norm_cat:
                pollutant_counts[norm_cat] += 1

    # Write CSV
    output_path = OUTPUT_DIR / "pollutant_distribution.csv"
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['pollutant_category', 'count', 'percentage'])

        total = sum(pollutant_counts.values())
        for cat, count in pollutant_counts.most_common():
            pct = count / total * 100 if total > 0 else 0
            writer.writerow([cat, count, f"{pct:.1f}"])

    print(f"Saved: {output_path}")
    return pollutant_counts


def generate_basic_statistics(data):
    """Generate basic_statistics.csv"""
    stats = {
        'total_papers': len(data),
        'papers_with_mechanism': 0,
        'papers_with_species': 0,
        'papers_with_both': 0,
        'papers_with_catalyst_type': 0,
        'papers_with_pollutant': 0,
        'year_range_start': 9999,
        'year_range_end': 0,
    }

    for d in data:
        mech = d.get('catalytic_mechanism', {}).get('dominant_mechanism')
        species = d.get('reactive_species', {}).get('dominant_species')
        cat_type = d.get('experimental_system', {}).get('catalyst', {}).get('type')
        pollutant = d.get('experimental_system', {}).get('target_pollutant', {}).get('category')
        year = d.get('paper_info', {}).get('year')

        if mech:
            stats['papers_with_mechanism'] += 1
        if species:
            stats['papers_with_species'] += 1
        if mech and species:
            stats['papers_with_both'] += 1
        if cat_type:
            stats['papers_with_catalyst_type'] += 1
        if pollutant:
            stats['papers_with_pollutant'] += 1
        if year:
            stats['year_range_start'] = min(stats['year_range_start'], year)
            stats['year_range_end'] = max(stats['year_range_end'], year)

    # Write CSV
    output_path = OUTPUT_DIR / "basic_statistics.csv"
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['statistic', 'value'])

        for key, value in stats.items():
            writer.writerow([key, value])

    print(f"Saved: {output_path}")
    return stats


# =============================================================================
# Main
# =============================================================================

def main():
    print("=" * 60)
    print("Generating Open-Source Aggregated Data Files")
    print("=" * 60)

    # Load data
    data = load_all_data()

    # Generate all CSV files
    print("\n--- Generating CSV files ---")
    generate_mechanism_by_year(data)
    generate_species_by_period(data)
    generate_mechanism_species_flow(data)
    generate_catalyst_distribution(data)
    generate_pollutant_distribution(data)
    generate_basic_statistics(data)

    print("\n" + "=" * 60)
    print("All files generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()
