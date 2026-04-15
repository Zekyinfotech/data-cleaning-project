=======================================================
  DATA CLEANING PROJECT — Customer Dataset
  Portfolio Project | Data Analytics
  By: Caleb Ezekiel (Zekyinfotech)
=======================================================

ISSUES FOUND & FIXED:
  1. Duplicate rows         → removed
  2. Inconsistent names     → stripped whitespace, title case
  3. Inconsistent gender    → standardized capitalization
  4. Inconsistent country   → standardized to uppercase
  5. Invalid emails         → regex-validated, flagged as NaN
  6. Invalid ages           → median imputation
  7. Missing salary         → median imputation
  8. Missing purchase amt   → median imputation
  9. Mixed date formats     → all converted to YYYY-MM-DD
 10. No spend segmentation  → added SpendCategory column
=======================================================
"""

import pandas as pd
import numpy as np
import re

# ── LOAD DATA ─────────────────────────────────────────
df = pd.read_csv("messy_customer_data.csv")

# ── 1. Remove Duplicates ──────────────────────────────
df.drop_duplicates(subset=["CustomerID", "Email"], keep="first", inplace=True)

# ── 2. Fix Name Formatting ────────────────────────────
df["Name"] = df["Name"].str.strip().str.title()

# ── 3. Standardize Gender ─────────────────────────────
df["Gender"] = df["Gender"].str.strip().str.capitalize()

# ── 4. Standardize Country ────────────────────────────
df["Country"] = df["Country"].str.strip().str.upper()

# ── 5. Validate & Fix Emails ──────────────────────────
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
df["Email"] = df["Email"].str.strip().str.lower()
df.loc[~df["Email"].apply(lambda x: bool(re.match(email_pattern, str(x)))), "Email"] = np.nan

# ── 6. Fix Age (invalid + missing → median) ───────────
df.loc[(df["Age"] < 0) | (df["Age"] > 120), "Age"] = np.nan
df["Age"] = df["Age"].fillna(df["Age"].median())

# ── 7. Fill Missing Salary ────────────────────────────
df["Salary"] = df["Salary"].fillna(df["Salary"].median())

# ── 8. Fill Missing PurchaseAmt ───────────────────────
df["PurchaseAmt"] = df["PurchaseAmt"].fillna(df["PurchaseAmt"].median())

# ── 9. Standardize Dates ──────────────────────────────
df["JoinDate"] = pd.to_datetime(df["JoinDate"], dayfirst=False, errors="coerce")
df["JoinDate"] = df["JoinDate"].dt.strftime("%Y-%m-%d")

# ── 10. Add Spend Category ────────────────────────────
df["SpendCategory"] = pd.cut(df["PurchaseAmt"],
    bins=[0, 200, 600, 1000, 2000],
    labels=["Low", "Medium", "High", "Premium"])

# ── SAVE CLEAN FILE ───────────────────────────────────
df.to_csv("cleaned_customer_data.csv", index=False)
print("✅ Cleaned file saved!")
print(df.head(10))