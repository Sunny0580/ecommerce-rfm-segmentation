"""
segmentation.py
===============
Maps RFM scores to human-readable customer segments using
industry-standard RFM segment rules.
"""

import pandas as pd
import numpy as np


# ── Segment definitions ────────────────────────────────────────────────────────
# Each segment is defined by ranges for R_Score, F_Score, M_Score.
# Rules are evaluated in priority order (first match wins).

SEGMENT_RULES = [
    # (segment_name, R_min, R_max, F_min, F_max, M_min, M_max)
    ("Champions",           5, 5, 4, 5, 4, 5),
    ("Champions",           5, 5, 5, 5, 3, 5),
    ("Loyal Customers",     4, 5, 3, 5, 3, 5),
    ("Loyal Customers",     3, 4, 4, 5, 4, 5),
    ("Potential Loyalists", 4, 5, 2, 3, 2, 3),
    ("Potential Loyalists", 3, 5, 1, 3, 1, 3),
    ("Recent Customers",    5, 5, 1, 1, 1, 5),
    ("Promising",           4, 4, 1, 1, 1, 2),
    ("Need Attention",      3, 3, 2, 3, 2, 3),
    ("About To Sleep",      2, 3, 1, 2, 1, 2),
    ("At Risk",             1, 2, 3, 5, 3, 5),
    ("At Risk",             1, 2, 2, 4, 2, 4),
    ("Cannot Lose Them",    1, 2, 4, 5, 4, 5),
    ("Hibernating",         1, 2, 1, 2, 1, 2),
    ("Lost",                1, 1, 1, 1, 1, 2),
]

# Fallback segment for anything not caught above
DEFAULT_SEGMENT = "Others"

# ── Segment metadata ───────────────────────────────────────────────────────────
SEGMENT_META = {
    "Champions": {
        "emoji": "🏆",
        "color": "#6C5CE7",
        "description": "Bought recently, buy often, and spend the most.",
        "action": "Reward them. Offer early access, loyalty perks, and VIP treatment.",
    },
    "Loyal Customers": {
        "emoji": "💎",
        "color": "#00B894",
        "description": "Consistent buyers with high overall value.",
        "action": "Upsell higher-value products. Ask for reviews and referrals.",
    },
    "Potential Loyalists": {
        "emoji": "🌟",
        "color": "#0984E3",
        "description": "Recent customers with average frequency.",
        "action": "Offer membership or loyalty programs. Personalise recommendations.",
    },
    "Recent Customers": {
        "emoji": "🆕",
        "color": "#74B9FF",
        "description": "Bought very recently but infrequently.",
        "action": "Onboard well. Send helpful content and gentle follow-ups.",
    },
    "Promising": {
        "emoji": "🌱",
        "color": "#55EFC4",
        "description": "Recent shoppers with low frequency.",
        "action": "Create brand awareness. Offer free shipping on next order.",
    },
    "Need Attention": {
        "emoji": "⚠️",
        "color": "#FDCB6E",
        "description": "Above average recency/frequency but haven't bought recently.",
        "action": "Make limited-time offers. Reactivate with personalised emails.",
    },
    "About To Sleep": {
        "emoji": "😴",
        "color": "#E17055",
        "description": "Below average recency and frequency — slipping away.",
        "action": "Share popular products. Offer discounts to re-engage them.",
    },
    "At Risk": {
        "emoji": "🚨",
        "color": "#D63031",
        "description": "Spent big and bought often but not recently.",
        "action": "Send personalised win-back emails. Offer special discounts.",
    },
    "Cannot Lose Them": {
        "emoji": "❗",
        "color": "#E84393",
        "description": "Made the biggest purchases but haven't returned.",
        "action": "Win them back via renewals or newer products. Don't lose them!",
    },
    "Hibernating": {
        "emoji": "🌙",
        "color": "#636E72",
        "description": "Low recency, frequency, and monetary.",
        "action": "Offer relevant products and special discounts.",
    },
    "Lost": {
        "emoji": "💀",
        "color": "#2D3436",
        "description": "Lowest recency, frequency, and monetary scores.",
        "action": "Revive interest with a bold offer, or let them go to save budget.",
    },
    "Others": {
        "emoji": "❓",
        "color": "#B2BEC3",
        "description": "Doesn't fit neatly into any segment.",
        "action": "Analyse individually.",
    },
}


def assign_segments(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Assign a segment label to every customer based on their R/F/M scores.

    Args:
        rfm: DataFrame with R_Score, F_Score, M_Score columns

    Returns:
        rfm DataFrame with added 'Segment' column
    """
    rfm = rfm.copy()
    rfm["Segment"] = DEFAULT_SEGMENT

    for rule in SEGMENT_RULES:
        seg, r_min, r_max, f_min, f_max, m_min, m_max = rule
        mask = (
            rfm["R_Score"].between(r_min, r_max) &
            rfm["F_Score"].between(f_min, f_max) &
            rfm["M_Score"].between(m_min, m_max) &
            (rfm["Segment"] == DEFAULT_SEGMENT)   # first match wins
        )
        rfm.loc[mask, "Segment"] = seg

    n_segmented = (rfm["Segment"] != DEFAULT_SEGMENT).sum()
    print(f"✅ {n_segmented:,} / {len(rfm):,} customers assigned to named segments")
    print("\n📊 Segment distribution:")
    dist = rfm["Segment"].value_counts()
    for seg, count in dist.items():
        print(f"   {SEGMENT_META.get(seg, {}).get('emoji', '•')} {seg:<22} {count:>5,}  ({count/len(rfm)*100:.1f}%)")

    return rfm


def get_segment_summary(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate RFM metrics and revenue by segment.

    Returns:
        DataFrame with segment-level statistics sorted by Monetary desc
    """
    summary = rfm.groupby("Segment").agg(
        Customer_Count = ("CustomerID",  "count"),
        Avg_Recency    = ("Recency",     "mean"),
        Avg_Frequency  = ("Frequency",   "mean"),
        Avg_Monetary   = ("Monetary",    "mean"),
        Total_Revenue  = ("Monetary",    "sum"),
        Avg_RFM_Total  = ("RFM_Total",   "mean"),
    ).round(2).reset_index()

    summary["Revenue_Pct"] = (summary["Total_Revenue"] /
                               summary["Total_Revenue"].sum() * 100).round(1)

    # Add metadata
    summary["Emoji"]       = summary["Segment"].map(lambda s: SEGMENT_META.get(s, {}).get("emoji", "•"))
    summary["Color"]       = summary["Segment"].map(lambda s: SEGMENT_META.get(s, {}).get("color", "#B2BEC3"))
    summary["Description"] = summary["Segment"].map(lambda s: SEGMENT_META.get(s, {}).get("description", ""))
    summary["Action"]      = summary["Segment"].map(lambda s: SEGMENT_META.get(s, {}).get("action", ""))

    return summary.sort_values("Total_Revenue", ascending=False).reset_index(drop=True)
