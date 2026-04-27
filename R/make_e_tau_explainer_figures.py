"""
Generate the E comparison and tau comparison explainer figures
for gccm_steps.md with consistent styling.
"""

from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parent.parent
FIG_DIR = PROJECT_ROOT / "figures"

FIGSIZE = (14, 6)
DPI = 200


def draw_rings(ax, ring_distances, title, subtitle, grid_size):
    """
    Draw concentric square rings on a pixel grid.

    Parameters
    ----------
    ax : matplotlib.axes.Axes
    ring_distances : list of int
        Distance of each ring from center in pixels.
    title : str
        Panel title (bold).
    subtitle : str
        Italic caption below panel.
    grid_size : int
        Number of pixels per side in the grid.
    """
    center = grid_size // 2
    ax.set_xlim(-0.5, grid_size - 0.5)
    ax.set_ylim(-0.5, grid_size - 0.5)
    ax.set_aspect("equal")
    ax.set_title(title, fontsize=16, fontweight="bold", pad=10)
    ax.set_xlabel(subtitle, fontsize=12, style="italic")

    # Soft grid
    for i in range(grid_size + 1):
        ax.axhline(i - 0.5, color="0.88", lw=0.3)
        ax.axvline(i - 0.5, color="0.88", lw=0.3)

    # Center pixel
    ax.add_patch(patches.Rectangle(
        (center - 0.5, center - 0.5), 1, 1,
        facecolor="red", edgecolor="red", alpha=0.8,
    ))

    # Rings (dark to light blue, with alpha gradient)
    n = len(ring_distances)
    for i, d in enumerate(ring_distances):
        frac = i / max(n - 1, 1)
        alpha = 0.9 - 0.5 * frac
        lw = 2.5 - 1.0 * frac
        color = plt.cm.Blues(0.8 - 0.4 * frac)
        ax.add_patch(patches.Rectangle(
            (center - d - 0.5, center - d - 0.5),
            2 * d + 1, 2 * d + 1,
            facecolor="none", edgecolor=color, lw=lw, alpha=alpha,
        ))

    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(True)
        spine.set_color("0.3")


# -- E comparison (tau=1 fixed, varying E) ------------------------------------

fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)

E_GRID = 21
draw_rings(
    axes[0],
    ring_distances=[1, 2, 3],
    title="E = 3  (3 rings)",
    subtitle="Small local neighborhood",
    grid_size=E_GRID,
)
draw_rings(
    axes[1],
    ring_distances=[1, 2, 3, 4, 5, 6, 7, 8, 9],
    title="E = 9  (9 rings)",
    subtitle="Captures a huge chunk of the city",
    grid_size=E_GRID,
)

fig.suptitle(
    "E controls how many rings describe each pixel's neighborhood",
    fontsize=17, fontweight="bold", y=0.98,
)
plt.tight_layout(rect=[0, 0, 1, 0.93])
out_e = FIG_DIR / "gccm_explainer_e_comparison.png"
plt.savefig(out_e, dpi=DPI, bbox_inches="tight", facecolor="white")
print(f"Saved: {out_e}")
plt.close()


# -- Tau comparison (E=3 fixed, varying tau) ----------------------------------

fig, axes = plt.subplots(1, 2, figsize=FIGSIZE)

TAU_GRID = 35
draw_rings(
    axes[0],
    ring_distances=[1, 2, 3],
    title="tau = 1\n(rings 1 pixel apart)",
    subtitle="Rings overlap heavily,\nsimilar values in each",
    grid_size=TAU_GRID,
)
draw_rings(
    axes[1],
    ring_distances=[5, 10, 15],
    title="tau = 5\n(rings 5 pixels apart)",
    subtitle="Rings sample different distances,\neach carries different information",
    grid_size=TAU_GRID,
)

fig.suptitle(
    "Tau controls the spacing between rings (both use E = 3)",
    fontsize=17, fontweight="bold", y=0.98,
)
plt.tight_layout(rect=[0, 0, 1, 0.93])
out_tau = FIG_DIR / "gccm_explainer_tau_comparison.png"
plt.savefig(out_tau, dpi=DPI, bbox_inches="tight", facecolor="white")
print(f"Saved: {out_tau}")
plt.close()
