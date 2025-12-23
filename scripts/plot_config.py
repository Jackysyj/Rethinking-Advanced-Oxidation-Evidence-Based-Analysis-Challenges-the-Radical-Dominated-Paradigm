#!/usr/bin/env python3
"""
Unified Plot Configuration Module
Standard settings for all figures in the LLM Benchmark experiment.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# =============================================================================
# Color Palette
# =============================================================================

COLORS_PRIMARY = ['#F09395', '#6AB7A1', '#8F97C9', '#30B3BB', '#FBB070']
COLORS_EXTENDED = ['#E8B4B8', '#A8D5BA', '#B8C5E2', '#7DCFCF', '#FFD4A3']

# Model-specific colors
MODEL_COLORS = {
    'claude': '#F09395',      # Coral pink
    'sonnet': '#E8B4B8',      # Light rose
    'gpt4o': '#8F97C9',       # Lavender purple
    'gemini': '#6AB7A1',      # Mint green
    'qwen': '#FBB070',        # Apricot orange
    'deepseek': '#30B3BB',    # Cyan blue
}

MODEL_LABELS = {
    'claude': 'Claude Opus 4.1',
    'sonnet': 'Claude Sonnet 4.5',
    'gpt4o': 'GPT-4o',
    'gemini': 'Gemini 3.0 Pro',
    'qwen': 'Qwen3-MAX',
    'deepseek': 'DeepSeek-R1',
}

# =============================================================================
# Figure Size (4:3 aspect ratio)
# =============================================================================

FIGURE_SIZE_LARGE = (12, 9)    # Default for most plots
FIGURE_SIZE_MEDIUM = (10, 7.5)  # Medium size
FIGURE_SIZE_SMALL = (8, 6)      # Single column
DPI = 300

# =============================================================================
# Font Sizes
# =============================================================================

FONT_SIZES = {
    'title': 26,
    'axis_label': 24,
    'tick_label': 20,
    'legend_title': 18,
    'legend': 16,
    'annotation': 16,
    'significance': 18,
}

# =============================================================================
# Line Widths
# =============================================================================

LINE_WIDTHS = {
    'main': 2.0,
    'secondary': 1.5,
    'grid': 0.5,
    'spine': 1.5,
    'box': 1.5,
    'whisker': 1.5,
    'bracket': 1.2,
}

# =============================================================================
# Style Functions
# =============================================================================

def apply_plot_style():
    """Apply unified plot style to matplotlib rcParams."""
    plt.rcParams.update({
        # Figure
        'figure.figsize': FIGURE_SIZE_LARGE,
        'figure.dpi': DPI,
        'figure.facecolor': 'white',

        # Font
        'font.family': 'sans-serif',
        'font.size': 14,

        # Axes
        'axes.titlesize': FONT_SIZES['title'],
        'axes.titleweight': 'bold',
        'axes.labelsize': FONT_SIZES['axis_label'],
        'axes.labelweight': 'bold',
        'axes.spines.top': False,
        'axes.spines.right': False,
        'axes.linewidth': LINE_WIDTHS['spine'],
        'axes.grid': True,
        'axes.axisbelow': True,

        # Ticks
        'xtick.labelsize': FONT_SIZES['tick_label'],
        'ytick.labelsize': FONT_SIZES['tick_label'],

        # Legend
        'legend.fontsize': FONT_SIZES['legend'],
        'legend.title_fontsize': FONT_SIZES['legend_title'],
        'legend.framealpha': 0.95,
        'legend.edgecolor': 'gray',

        # Grid
        'grid.alpha': 0.4,
        'grid.linestyle': '--',
        'grid.linewidth': LINE_WIDTHS['grid'],
    })


def create_figure(size='large'):
    """Create a new figure with standard settings.

    Args:
        size: 'large' (12x9), 'medium' (10x7.5), or 'small' (8x6)

    Returns:
        fig, ax: matplotlib figure and axes
    """
    apply_plot_style()

    if size == 'large':
        figsize = FIGURE_SIZE_LARGE
    elif size == 'medium':
        figsize = FIGURE_SIZE_MEDIUM
    else:
        figsize = FIGURE_SIZE_SMALL

    fig, ax = plt.subplots(figsize=figsize, dpi=DPI)
    return fig, ax


def add_significance_bracket(ax, x1, x2, y, p_value, h=0.02):
    """Add significance bracket between two groups.

    Args:
        ax: matplotlib axes
        x1, x2: x positions for bracket ends
        y: y position for bracket base
        p_value: p-value for significance test
        h: bracket height
    """
    # Determine significance level
    if p_value < 0.001:
        sig_text = '***'
    elif p_value < 0.01:
        sig_text = '**'
    elif p_value < 0.05:
        sig_text = '*'
    else:
        sig_text = 'ns'

    # Draw bracket
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], 'k-', lw=LINE_WIDTHS['bracket'])
    ax.text((x1+x2)/2, y+h+0.005, sig_text, ha='center', va='bottom',
            fontsize=FONT_SIZES['significance'], fontweight='bold')


def create_model_legend(ax, models=None, loc='lower left', bbox_to_anchor=None, ncol=1):
    """Create standardized legend for model comparison plots.

    Args:
        ax: matplotlib axes
        models: list of model keys, or None for all models
        loc: legend location
        bbox_to_anchor: tuple for legend position (optional)
        ncol: number of columns for legend (default 1)
    """
    if models is None:
        models = list(MODEL_COLORS.keys())

    handles = [mpatches.Patch(facecolor=MODEL_COLORS[m], edgecolor='black',
                              alpha=0.8, label=MODEL_LABELS[m])
               for m in models if m in MODEL_COLORS]

    legend_kwargs = dict(
        handles=handles,
        loc=loc,
        fontsize=FONT_SIZES['legend'],
        title='Models',
        title_fontsize=FONT_SIZES['legend_title'],
        framealpha=0.95,
        edgecolor='gray',
        ncol=ncol
    )
    if bbox_to_anchor is not None:
        legend_kwargs['bbox_to_anchor'] = bbox_to_anchor

    ax.legend(**legend_kwargs)


def save_figure(fig, filepath, dpi=None):
    """Save figure with standard settings.

    Args:
        fig: matplotlib figure
        filepath: output path (should end with .png)
        dpi: optional DPI override
    """
    if dpi is None:
        dpi = DPI
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight', facecolor='white')
    print(f"Saved: {filepath}")
