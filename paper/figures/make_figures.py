"""Redraw manuscript Figures 2-4 for IEEE Access from the values in the
revised manuscript (Tables III-V) and the five-run evidence archive.

Sizes target IEEE two-column pages: single column 3.5 in, double 7.16 in,
with text at 8 pt or larger at final print size."""
import sys
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PALETTE = {"blue_main": "#0F4D92", "blue_secondary": "#3775BA", "red_strong": "#B64342",
           "red_2": "#E9A6A1", "neutral": "#CFCECE", "teal": "#42949E", "dark": "#333333"}
plt.rcParams.update({
    "font.family": ["sans-serif"], "font.sans-serif": ["Arial", "Liberation Sans", "DejaVu Sans"], "font.size": 8,
    "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
    "axes.titlesize": 8.5, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "legend.frameon": False, "legend.fontsize": 7.5, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "pdf.fonttype": 42, "svg.fonttype": "none", "hatch.linewidth": 0.6,
})
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
OUT.mkdir(parents=True, exist_ok=True)


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(OUT / f"{name}.{ext}", dpi=600, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


# Figure 2: pooled accuracy and macro-F1 (Table III, five-run pipeline)
models = ["Multinomial NB", "Logistic regression", "Linear SVM", "Compact MLP"]
acc = [0.8493, 0.8820, 0.8804, 0.8304]
mf1 = [0.8480, 0.8816, 0.8800, 0.8302]
fig, ax = plt.subplots(figsize=(3.5, 2.3))
y = np.arange(len(models))[::-1]
h = 0.36
ax.barh(y + h / 2, acc, h, color=PALETTE["blue_main"], edgecolor="black", linewidth=0.5, label="Accuracy")
ax.barh(y - h / 2, mf1, h, color=PALETTE["neutral"], edgecolor="black", linewidth=0.5, hatch="///", label="Macro-F1")
for yy, a, m in zip(y, acc, mf1):
    ax.text(a + 0.0008, yy + h / 2, f"{a:.4f}", va="center", fontsize=7)
    ax.text(m + 0.0008, yy - h / 2, f"{m:.4f}", va="center", fontsize=7)
ax.set_yticks(y, models)
ax.set_xlim(0.80, 0.90)
ax.set_xlabel("Pooled score (axis starts at 0.80)")
ax.xaxis.grid(True, color="#E5E5E5", linewidth=0.5)
ax.set_axisbelow(True)
ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, handlelength=1.5)
save(fig, "figure2_model_performance")

# Figure 3: SC, raw-content retention, record size (Table IV)
conds = ["Decision-only", "Raw-only", "Structured-only (TRACE)", "Structured+raw"]
sc = [0.25, 0.50, 1.00, 1.00]
raw = [0, 100, 0, 100]
mean_b = [58.0, 1371.8, 319.6, 1609.4]
med_b = [57.0, 987.0, 318.0, 1224.0]
colors = [PALETTE["neutral"], PALETTE["red_2"], PALETTE["blue_main"], PALETTE["blue_secondary"]]
hatches = ["", "///", "", "///"]
fig, axes = plt.subplots(1, 3, figsize=(7.16, 2.2))
x = np.arange(4)
specs = [
    (axes[0], sc, "(a) Schema conformance (SC)", "SC", (0, 1.15), lambda v: f"{v:.2f}"),
    (axes[1], raw, "(b) Raw-content retention", "Records with email text (%)", (0, 115), lambda v: f"{v:.0f}%"),
    (axes[2], mean_b, "(c) Serialized record size", "Mean bytes per record", (0, 1900), lambda v: f"{v:,.1f}"),
]
for ax, vals, title, ylabel, ylim, fmt in specs:
    bars = ax.bar(x, vals, 0.65, color=colors, edgecolor="black", linewidth=0.5)
    for b, hch in zip(bars, hatches):
        b.set_hatch(hch)
    for xx, v in zip(x, vals):
        ax.text(xx, v + ylim[1] * 0.02, fmt(v), ha="center", va="bottom", fontsize=7)
    ax.set_xticks([])
    ax.set_ylim(*ylim)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.yaxis.grid(True, color="#E5E5E5", linewidth=0.5)
    ax.set_axisbelow(True)
axes[2].scatter(x, med_b, marker="D", s=12, color="black", zorder=3, label="Median")
axes[2].legend(loc="upper left")
from matplotlib.patches import Patch
handles = [Patch(facecolor=c, edgecolor="black", linewidth=0.5, hatch=hh, label=l)
           for c, hh, l in zip(colors, hatches, conds)]
fig.legend(handles=handles, loc="upper center", ncol=4, bbox_to_anchor=(0.5, 1.09))
fig.tight_layout(w_pad=1.2)
save(fig, "figure3_record_tradeoffs")

# Figure 4: gate stress (Table V; panel b = five-run mean with min-max range)
gates = ["Literal", "Generalized", "Context-aware"]
gcol = [PALETTE["neutral"], PALETTE["red_2"], PALETTE["blue_main"]]
ghat = ["", "///", ""]
panels = [
    ("(a) Template-only trigger rate", ["Held-out\n(n=120)", "Hard-negative\n(n=120)"],
     [[0.0, 100.0, 100.0], [0.0, 100.0, 0.0]], None),
    ("(b) Complete-email incremental trigger rate", ["Held-out\n(n=1,200)", "Hard-negative\n(n=600)"],
     [[0.0, 97.65, 89.42], [50.5, 53.6, 14.23]],
     [[(0.0, 0.0), (97.17, 98.25), (88.58, 91.0)], [(50.5, 50.5), (53.0, 54.83), (13.67, 15.0)]]),
]
fig, axes = plt.subplots(1, 2, figsize=(7.16, 2.3), sharey=True)
w = 0.26
for ax, (title, groups, vals, ranges) in zip(axes, panels):
    gx = np.arange(len(groups))
    for k in range(3):
        v = [vals[g][k] for g in range(len(groups))]
        pos = gx + (k - 1) * w
        ax.bar(pos, v, w, color=gcol[k], hatch=ghat[k], edgecolor="black", linewidth=0.5,
               label=gates[k])
        if ranges:
            lo = [v[g] - ranges[g][k][0] for g in range(len(groups))]
            hi = [ranges[g][k][1] - v[g] for g in range(len(groups))]
            ax.errorbar(pos, v, yerr=[lo, hi], fmt="none", ecolor="black", elinewidth=0.6, capsize=1.5)
        for p, vv in zip(pos, v):
            ax.text(p, vv + 3, f"{vv:.1f}", ha="center", va="bottom", fontsize=6.5)
    ax.set_xticks(gx, groups)
    ax.set_ylim(0, 112)
    ax.set_title(title)
    ax.yaxis.grid(True, color="#E5E5E5", linewidth=0.5)
    ax.set_axisbelow(True)
axes[0].set_ylabel("Trigger rate (%)")
axes[1].text(1.0, -0.30, "Error bars: min-max range across five runs.", transform=axes[1].transAxes,
             ha="right", fontsize=6.5, color="#555555")
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc="upper center", ncol=3, bbox_to_anchor=(0.5, 1.07))
fig.tight_layout()
save(fig, "figure4_gate_stress")
print("saved to", OUT)
