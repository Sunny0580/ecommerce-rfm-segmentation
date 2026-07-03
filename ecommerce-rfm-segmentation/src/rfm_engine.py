"""
rfm_engine.py
=============
Core RFM scoring logic.
Computes Recency, Frequency, and Monetary values per customer,
then assigns quantile-based scores (1–5) for each dimension.
"""

import pandas as pd
import numpy as np


def compute_rfm(df: pd.DataFrame, snapshot_date: pd.Timestamp = None) -> pd.DataFrame:
    """
    Compute RFM metrics for every unique customer.

    Args:
        df: Cleaned transaction DataFrame with columns:
            InvoiceNo, InvoiceDate, CustomerID, TotalPrice
        snapshot_date: Reference date for Recency calculation.
                       Defaults to 1 day after the last invoice.

    Returns:
        DataFrame indexed by CustomerID with columns:
        Recency, Frequency, Monetary
    """
    if snapshot_date is None:
        snapshot_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

    print(f"📅 Snapshot date: {snapshot_date.date()}")

    rfm = df.groupby("CustomerID").agg(
        Recency   = ("InvoiceDate",  lambda x: (snapshot_date - x.max()).days),
        Frequency = ("InvoiceNo",    "nunique"),
        Monetary  = ("TotalPrice",   "sum"),
    ).reset_index()

    rfm["Monetary"] = rfm["Monetary"].round(2)
    print(f"   Customers computed: {len(rfm):,}")
    return rfm


def score_rfm(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Assign quantile-based scores (1 = worst, 5 = best) for R, F, M.

    Recency is reverse-scored: lower days = better = higher score.

    Args:
        rfm: DataFrame with Recency, Frequency, Monetary columns

    Returns:
        rfm DataFrame with added R_Score, F_Score, M_Score, RFM_Score columns
    """
    rfm = rfm.copy()

    # Recency: lower is better → reverse scoring
    rfm["R_Score"] = pd.qcut(rfm["Recency"],  q=5, labels=[5, 4, 3, 2, 1]).astype(int)

    # Frequency: higher is better
    rfm["F_Score"] = pd.qcut(rfm["Frequency"].rank(method="first"),
                              q=5, labels=[1, 2, 3, 4, 5]).astype(int)

    # Monetary: higher is better
    rfm["M_Score"] = pd.qcut(rfm["Monetary"].rank(method="first"),
                              q=5, labels=[1, 2, 3, 4, 5]).astype(int)

    # Composite RFM string and numeric score
    rfm["RFM_Score"] = rfm["R_Score"].astype(str) + rfm["F_Score"].astype(str) + rfm["M_Score"].astype(str)
    rfm["RFM_Total"] = rfm["R_Score"] + rfm["F_Score"] + rfm["M_Score"]

    print("✅ RFM scores assigned")
    return rfm


def get_rfm_summary(rfm: pd.DataFrame) -> pd.DataFrame:
    """
    Return descriptive statistics of the RFM metrics.
    """
    return rfm[["Recency", "Frequency", "Monetary"]].describe().round(2)
