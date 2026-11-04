"""Helpers for turning Matplotlib / Seaborn figures into inline image URIs."""
from __future__ import annotations

import base64
import io

PALETTE = ["#4F46E5", "#0EA5E9", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"]
INK = "#1E293B"
MUTED = "#64748B"
GRID = "#E2E8F0"
SURFACE = "#FFFFFF"


def figure_to_uri(figure) -> str:
    """Return a data:image/png;base64 URI so no static asset server is needed."""
    import matplotlib.pyplot as plt

    buffer = io.BytesIO()
    figure.savefig(buffer, format="png", dpi=110, bbox_inches="tight", facecolor=SURFACE)
    plt.close(figure)
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def new_figure(width: float = 8.4, height: float = 3.8):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    figure, axes = plt.subplots(figsize=(width, height), facecolor=SURFACE)
    axes.set_facecolor(SURFACE)
    for spine in ("top", "right"):
        axes.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        axes.spines[spine].set_color(GRID)
    axes.tick_params(colors=MUTED, labelsize=9)
    axes.xaxis.label.set_color(MUTED)
    axes.yaxis.label.set_color(MUTED)
    axes.title.set_color(INK)
    axes.grid(axis="y", color=GRID, linewidth=0.8, alpha=0.9)
    axes.set_axisbelow(True)
    figure.tight_layout()
    return figure, axes
