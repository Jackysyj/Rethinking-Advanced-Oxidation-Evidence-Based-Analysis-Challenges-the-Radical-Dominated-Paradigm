# Utility Scripts for PMS-AOP Data Analysis

## Overview

This directory contains utility scripts for processing and visualizing PMS-AOP literature data.

## Scripts

### generate_si_data.py

Generates aggregated CSV files from extracted JSON data.

**Features:**
- Normalizes species names (e.g., `1O2`, `HVM`, `SO4`, `OH`)
- Normalizes catalyst types (e.g., `MOF-derived`, `SAC`, `Biochar`)
- Generates summary statistics by year, period, and category

**Usage:**
```bash
# Adjust paths in the script first
python generate_si_data.py
```

**Note:** This script requires raw JSON extraction data which is not included in the open-source release. The script is provided for transparency and reproducibility.

### plot_config.py

Unified plotting configuration module for consistent figure styling.

**Features:**
- Standardized color palettes (macaron style)
- Consistent figure sizes (4:3 aspect ratio)
- Publication-ready DPI (300)
- Significance bracket helpers

**Usage:**
```python
from plot_config import (
    apply_plot_style,
    create_figure,
    save_figure,
    COLORS_PRIMARY,
    MODEL_COLORS
)

# Apply consistent styling
apply_plot_style()

# Create figure with standard settings
fig, ax = create_figure(size='large')

# Use primary color palette
ax.bar(x, y, color=COLORS_PRIMARY[0])

# Save with publication quality
save_figure(fig, 'output.png')
```

**Color Palette:**
```python
COLORS_PRIMARY = ['#F09395', '#6AB7A1', '#8F97C9', '#30B3BB', '#FBB070']
# Coral pink, Mint green, Lavender purple, Cyan blue, Apricot orange
```

## Dependencies

```
matplotlib>=3.5.0
pandas>=1.4.0
```

## License

These scripts are released under CC BY 4.0.
