"""Design tokens for the light IDE theme."""
from __future__ import annotations

BG = "#F5F7FB"
SURFACE = "#FFFFFF"
SURFACE_ALT = "#FAFBFE"
BORDER = "#E5E8F1"
TEXT = "#111827"
MUTED = "#64748B"
FAINT = "#94A3B8"
PRIMARY = "#4F46E5"
PRIMARY_SOFT = "#EEF0FF"
ACCENT = "#0EA5E9"
SUCCESS = "#10B981"
WARNING = "#F59E0B"
DANGER = "#EF4444"
SHADOW = "0 1px 2px rgba(16,24,40,.04), 0 8px 24px rgba(16,24,40,.05)"

SIDEBAR_WIDTH = "268px"
FONT = "'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Consolas, monospace"

CARD = {
    "background": SURFACE,
    "border": f"1px solid {BORDER}",
    "border_radius": "14px",
    "box_shadow": SHADOW,
}

CHIP = {
    "background": SURFACE_ALT,
    "border": f"1px solid {BORDER}",
    "border_radius": "999px",
    "font_size": "12px",
    "color": MUTED,
}
