"""Shared plotting helpers for notebooks and reports."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt


def save_figure(filename: str, *, dpi: int = 200) -> Path:
    """Save the current Matplotlib figure under outputs/figures."""
    output = Path("outputs/figures") / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output, dpi=dpi, bbox_inches="tight")
    return output

