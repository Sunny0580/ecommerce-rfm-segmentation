"""
data_loader.py
==============
Loads and cleans the Online Retail II dataset.
Handles missing values, cancellations, and data type corrections.
"""

import pandas as pd
import numpy as np
import os


def load_data(filepath: str) -> pd.DataFrame:
    """
    Load the Online Retail CSV/Excel dataset.

    Args:
        filepath: Path to the data file (.csv or .xlsx)

    Returns:
        Cleaned DataFrame ready for RFM analysis
    """
    print(f"📂 Loading data from: {filepath}")

    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".csv":
        df = pd.read_csv(filepath, encoding="ISO-8859-1")
    elif ext in [".xlsx", ".xls"]:
        df = pd.read_excel(filepath, sheet_name="Year 2010-2011")
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    print(f"   Raw rows: {len(df):,}")
    df = clean_data(df)
    print(f"   Clean rows: {len(df):,}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply all cleaning steps to the raw dataframe.

    Cleaning steps:
    - Standardise column names
    - Drop rows with missing CustomerID
    - Remove cancelled orders (InvoiceNo starting with 'C')
    - Remove rows with Quantity <= 0 or UnitPrice <= 0
    - Parse InvoiceDate to datetime
    - Compute TotalPrice = Quantity * UnitPrice
    """
    # Standardise column names
    df.columns = df.columns.str.strip()

    # Drop missing CustomerID
    before = len(df)
    df = df.dropna(subset=["Customer ID"] if "Customer ID" in df.columns else ["CustomerID"])
    # Normalise column name
    if "Customer ID" in df.columns:
        df = df.rename(columns={"Customer ID": "CustomerID"})
    print(f"   Dropped {before - len(df):,} rows with missing CustomerID")

    # Remove cancellations
    before = len(df)
    df = df[~df["Invoice"].astype(str).str.startswith("C")] if "Invoice" in df.columns \
        else df[~df["InvoiceNo"].astype(str).str.startswith("C")]
    if "Invoice" in df.columns:
        df = df.rename(columns={"Invoice": "InvoiceNo", "StockCode": "StockCode",
                                  "InvoiceDate": "InvoiceDate", "Price": "UnitPrice",
                                  "Quantity": "Quantity"})
    print(f"   Dropped {before - len(df):,} cancelled orders")

    # Remove non-positive values
    before = len(df)
    df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
    print(f"   Dropped {before - len(df):,} rows with bad Quantity/Price")

    # Parse dates
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Compute revenue per line
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

    # Cast CustomerID to int then string
    df["CustomerID"] = df["CustomerID"].astype(int).astype(str)

    return df


def generate_synthetic_data(n_customers: int = 4000, seed: int = 42) -> pd.DataFrame:
    """
    Generate a realistic synthetic e-commerce dataset when the real one
    is unavailable. Produces varied purchase patterns across customer archetypes.

    Args:
        n_customers: Number of unique customers to simulate
        seed: Random seed for reproducibility

    Returns:
        DataFrame matching the Online Retail schema
    """
    rng = np.random.default_rng(seed)
    print(f"🔧 Generating synthetic data for {n_customers:,} customers …")

    # Simulate different customer archetypes (proportions)
    archetypes = {
        "champion":          (0.10, (1, 15),   (10, 30), (200, 800)),
        "loyal":             (0.15, (10, 40),  (7, 20),  (100, 400)),
        "potential_loyalist":(0.12, (20, 60),  (4, 10),  (50, 200)),
        "recent":            (0.08, (1, 10),   (1, 3),   (30, 120)),
        "promising":         (0.07, (15, 40),  (1, 4),   (20, 80)),
        "need_attention":    (0.10, (40, 80),  (3, 7),   (50, 150)),
        "about_to_sleep":    (0.08, (60, 100), (2, 5),   (20, 100)),
        "at_risk":           (0.10, (80, 150), (5, 15),  (100, 300)),
        "cannot_lose":       (0.05, (120, 200),(15, 30), (300, 1000)),
        "hibernating":       (0.08, (150, 250),(1, 4),   (20, 80)),
        "lost":              (0.07, (250, 365),(1, 2),   (10, 50)),
    }

    rows = []
    snapshot_date = pd.Timestamp("2011-12-10")
    invoice_counter = 100000
    customer_counter = 10000

    for archetype, (prop, r_range, f_range, m_range) in archetypes.items():
        n = int(n_customers * prop)
        for _ in range(n):
            cid = str(customer_counter)
            customer_counter += 1
            recency_days = int(rng.integers(*r_range))
            n_orders = int(rng.integers(*f_range))
            avg_spend = rng.uniform(*m_range)
            last_date = snapshot_date - pd.Timedelta(days=recency_days)

            for order_idx in range(n_orders):
                order_date = last_date - pd.Timedelta(
                    days=int(rng.integers(0, max(1, recency_days * 3)))
                )
                n_items = int(rng.integers(1, 6))
                for _ in range(n_items):
                    rows.append({
                        "InvoiceNo":   str(invoice_counter),
                        "StockCode":   f"PROD{rng.integers(1000, 9999)}",
                        "Description": "Product",
                        "Quantity":    int(rng.integers(1, 10)),
                        "InvoiceDate": order_date,
                        "UnitPrice":   round(avg_spend / n_items / rng.integers(1, 5), 2),
                        "CustomerID":  cid,
                        "Country":     rng.choice(["United Kingdom", "Germany",
                                                    "France", "Spain", "Netherlands"]),
                    })
                invoice_counter += 1

    df = pd.DataFrame(rows)
    df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]
    print(f"   Generated {len(df):,} transaction rows for {n_customers:,} customers")
    return df
