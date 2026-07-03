"""
main.py
=======
End-to-end RFM Customer Segmentation Pipeline.

Run this script to:
  1. Generate / load e-commerce data
  2. Compute RFM scores
  3. Assign customer segments
  4. Save outputs (CSV files + charts)

Usage:
    python main.py
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

# Force UTF-8 output on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # non-interactive backend for saving files
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns

# ── Try squarify for treemap ────────────────────────────────────────────────
try:
    import squarify
    HAS_SQUARIFY = True
except ImportError:
    HAS_SQUARIFY = False
    print("⚠️  squarify not installed — treemap will be skipped. Run: pip install squarify")

# ── Local modules ────────────────────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))
from src.data_loader   import generate_synthetic_data, load_data
from src.rfm_engine    import compute_rfm, score_rfm, get_rfm_summary
from src.segmentation  import assign_segments, get_segment_summary, SEGMENT_META

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT        = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(ROOT, "outputs")
CHARTS_DIR  = os.path.join(OUTPUTS_DIR, "charts")
DATA_DIR    = os.path.join(ROOT, "data")
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(CHARTS_DIR,  exist_ok=True)
os.makedirs(DATA_DIR,    exist_ok=True)

# ── Style ────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  "#0F1117",
    "axes.facecolor":    "#1A1D2E",
    "axes.labelcolor":   "#E0E0E0",
    "text.color":        "#E0E0E0",
    "xtick.color":       "#A0A0A0",
    "ytick.color":       "#A0A0A0",
    "axes.edgecolor":    "#2A2D3E",
    "grid.color":        "#2A2D3E",
    "font.family":       "DejaVu Sans",
    "font.size":         11,
})

PALETTE = [m["color"] for m in SEGMENT_META.values()]


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 — Load data
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "═"*60)
print("  E-COMMERCE RFM CUSTOMER SEGMENTATION")
print("  Portfolio Project — Data Analytics")
print("═"*60 + "\n")

real_data_path = os.path.join(DATA_DIR, "online_retail.xlsx")
csv_path       = os.path.join(DATA_DIR, "online_retail.csv")

if os.path.exists(real_data_path):
    df = load_data(real_data_path)
elif os.path.exists(csv_path):
    df = load_data(csv_path)
else:
    print("ℹ️  Real dataset not found — using synthetic data (4,000 customers)\n")
    df = generate_synthetic_data(n_customers=4000)


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 — Compute & Score RFM
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── STEP 2: Computing RFM Metrics ─────────────────────────────\n")
rfm = compute_rfm(df)
rfm = score_rfm(rfm)

print("\n📈 RFM Summary Statistics:")
print(get_rfm_summary(rfm).to_string())


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 — Assign Segments
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── STEP 3: Assigning Segments ────────────────────────────────\n")
rfm     = assign_segments(rfm)
summary = get_segment_summary(rfm)

print("\n💰 Segment Revenue Summary:")
print(summary[["Emoji", "Segment", "Customer_Count", "Total_Revenue", "Revenue_Pct"]].to_string(index=False))


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 4 — Save CSVs
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── STEP 4: Saving Outputs ────────────────────────────────────\n")

rfm_out     = os.path.join(OUTPUTS_DIR, "rfm_scores.csv")
summary_out = os.path.join(OUTPUTS_DIR, "segment_summary.csv")

rfm.to_csv(rfm_out, index=False)
summary.to_csv(summary_out, index=False)
print(f"   ✅ {rfm_out}")
print(f"   ✅ {summary_out}")


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 5 — Visualisations
# ═══════════════════════════════════════════════════════════════════════════════
print("\n── STEP 5: Generating Charts ─────────────────────────────────\n")

seg_colors = {seg: meta["color"] for seg, meta in SEGMENT_META.items()}

# ── Chart 1: Segment Customer Count Bar Chart ────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor("#0F1117")
ax.set_facecolor("#1A1D2E")

sorted_summary = summary.sort_values("Customer_Count", ascending=True)
colors = [seg_colors.get(s, "#B2BEC3") for s in sorted_summary["Segment"]]
bars = ax.barh(sorted_summary["Segment"], sorted_summary["Customer_Count"],
               color=colors, edgecolor="none", height=0.7)

for bar, val in zip(bars, sorted_summary["Customer_Count"]):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
            f"{val:,}", va="center", ha="left", color="#E0E0E0", fontsize=10)

ax.set_xlabel("Number of Customers", labelpad=12)
ax.set_title("Customer Count by Segment", fontsize=16, fontweight="bold",
             color="#FFFFFF", pad=20)
ax.spines[:].set_visible(False)
ax.tick_params(left=False)
ax.set_xlim(0, sorted_summary["Customer_Count"].max() * 1.18)
plt.tight_layout()
chart1 = os.path.join(CHARTS_DIR, "segment_bar.png")
plt.savefig(chart1, dpi=150, bbox_inches="tight", facecolor="#0F1117")
plt.close()
print(f"   ✅ segment_bar.png")


# ── Chart 2: Revenue Contribution Pie Chart ──────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor("#0F1117")
ax.set_facecolor("#0F1117")

top_n = summary.nlargest(8, "Total_Revenue")
other_rev = summary[~summary["Segment"].isin(top_n["Segment"])]["Total_Revenue"].sum()
if other_rev > 0:
    other_row = pd.DataFrame([{"Segment": "Others", "Total_Revenue": other_rev, "Color": "#B2BEC3"}])
    top_n = pd.concat([top_n, other_row], ignore_index=True)

pie_colors = [seg_colors.get(s, "#B2BEC3") for s in top_n["Segment"]]
wedges, texts, autotexts = ax.pie(
    top_n["Total_Revenue"],
    labels=None,
    autopct="%1.1f%%",
    colors=pie_colors,
    startangle=140,
    pctdistance=0.82,
    wedgeprops=dict(edgecolor="#0F1117", linewidth=2),
)
for at in autotexts:
    at.set_color("white")
    at.set_fontsize(9)

legend_labels = [f"{row['Segment']}  (${row['Total_Revenue']:,.0f})"
                 for _, row in top_n.iterrows()]
ax.legend(wedges, legend_labels, loc="lower center", bbox_to_anchor=(0.5, -0.12),
          ncol=2, frameon=False, fontsize=9, labelcolor="#E0E0E0")
ax.set_title("Revenue Contribution by Segment", fontsize=16, fontweight="bold",
             color="#FFFFFF", pad=20)
plt.tight_layout()
chart2 = os.path.join(CHARTS_DIR, "revenue_pie.png")
plt.savefig(chart2, dpi=150, bbox_inches="tight", facecolor="#0F1117")
plt.close()
print(f"   ✅ revenue_pie.png")


# ── Chart 3: RFM Score Distributions ─────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.patch.set_facecolor("#0F1117")
fig.suptitle("RFM Score Distributions", fontsize=16, fontweight="bold",
             color="#FFFFFF", y=1.02)

dims   = ["R_Score", "F_Score", "M_Score"]
titles = ["Recency Score", "Frequency Score", "Monetary Score"]
colors_dim = ["#6C5CE7", "#00B894", "#FDCB6E"]

for ax, dim, title, col in zip(axes, dims, titles, colors_dim):
    ax.set_facecolor("#1A1D2E")
    counts = rfm[dim].value_counts().sort_index()
    bars_d = ax.bar(counts.index, counts.values, color=col, alpha=0.85,
                    edgecolor="none", width=0.6)
    ax.set_title(title, color="#FFFFFF", fontsize=13)
    ax.set_xlabel("Score (1=Low, 5=High)", color="#A0A0A0")
    ax.set_ylabel("Customer Count",       color="#A0A0A0")
    ax.spines[:].set_visible(False)
    ax.tick_params(colors="#A0A0A0")
    ax.set_xticks([1, 2, 3, 4, 5])
    for bar in bars_d:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                f"{int(bar.get_height()):,}", ha="center", va="bottom",
                color="#E0E0E0", fontsize=9)

plt.tight_layout()
chart3 = os.path.join(CHARTS_DIR, "rfm_distributions.png")
plt.savefig(chart3, dpi=150, bbox_inches="tight", facecolor="#0F1117")
plt.close()
print(f"   ✅ rfm_distributions.png")


# ── Chart 4: Treemap ─────────────────────────────────────────────────────────
if HAS_SQUARIFY:
    fig, ax = plt.subplots(figsize=(14, 8))
    fig.patch.set_facecolor("#0F1117")
    ax.set_facecolor("#0F1117")

    sizes  = summary["Customer_Count"].tolist()
    labels = [
        f"{row['Emoji']} {row['Segment']}\n{row['Customer_Count']:,} customers\n{row['Revenue_Pct']}% revenue"
        for _, row in summary.iterrows()
    ]
    colors_tm = [seg_colors.get(s, "#B2BEC3") for s in summary["Segment"]]

    squarify.plot(sizes=sizes, label=labels, color=colors_tm,
                  alpha=0.88, ax=ax, text_kwargs={"fontsize": 9, "color": "white"})
    ax.set_title("Customer Segments — Treemap (Size = Customer Count)",
                 fontsize=15, fontweight="bold", color="#FFFFFF", pad=15)
    ax.axis("off")
    plt.tight_layout()
    chart4 = os.path.join(CHARTS_DIR, "segment_treemap.png")
    plt.savefig(chart4, dpi=150, bbox_inches="tight", facecolor="#0F1117")
    plt.close()
    print(f"   ✅ segment_treemap.png")


# ── Chart 5: Recency vs Monetary scatter coloured by segment ─────────────────
fig, ax = plt.subplots(figsize=(12, 7))
fig.patch.set_facecolor("#0F1117")
ax.set_facecolor("#1A1D2E")

for seg, group in rfm.groupby("Segment"):
    col = seg_colors.get(seg, "#B2BEC3")
    ax.scatter(group["Recency"], group["Monetary"],
               c=col, alpha=0.55, s=18, label=seg, edgecolors="none")

ax.set_xlabel("Recency (days since last purchase)",  fontsize=12)
ax.set_ylabel("Monetary Value (£ total spend)",      fontsize=12)
ax.set_title("Recency vs Monetary Value — Coloured by Segment",
             fontsize=15, fontweight="bold", color="#FFFFFF", pad=15)
ax.spines[:].set_visible(False)
legend = ax.legend(loc="upper right", frameon=False, fontsize=8,
                   labelcolor="#E0E0E0", markerscale=2)
plt.tight_layout()
chart5 = os.path.join(CHARTS_DIR, "recency_vs_monetary.png")
plt.savefig(chart5, dpi=150, bbox_inches="tight", facecolor="#0F1117")
plt.close()
print(f"   ✅ recency_vs_monetary.png")


# ── Chart 6: Average RFM Scores Heatmap by Segment ───────────────────────────
heatmap_data = rfm.groupby("Segment")[["R_Score", "F_Score", "M_Score"]].mean().round(2)
heatmap_data = heatmap_data.reindex(summary["Segment"])

fig, ax = plt.subplots(figsize=(9, len(heatmap_data) * 0.55 + 2))
fig.patch.set_facecolor("#0F1117")

cmap = sns.diverging_palette(220, 20, as_cmap=True)
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlOrRd",
            linewidths=0.5, linecolor="#0F1117",
            cbar_kws={"shrink": 0.6, "label": "Score"},
            ax=ax, vmin=1, vmax=5)
ax.set_title("Average RFM Scores per Segment", fontsize=14, fontweight="bold",
             color="#FFFFFF", pad=15)
ax.set_facecolor("#1A1D2E")
ax.tick_params(colors="#E0E0E0", labelsize=10)
ax.set_xlabel("RFM Dimension", color="#A0A0A0")
ax.set_ylabel("")
plt.tight_layout()
chart6 = os.path.join(CHARTS_DIR, "rfm_heatmap.png")
plt.savefig(chart6, dpi=150, bbox_inches="tight", facecolor="#0F1117")
plt.close()
print(f"   ✅ rfm_heatmap.png")


print("\n" + "═"*60)
print("  ✅ PIPELINE COMPLETE")
print(f"  📁 Outputs saved to: {OUTPUTS_DIR}")
print("═"*60 + "\n")
