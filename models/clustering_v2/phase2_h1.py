"""
=============================================================
PHASE 2 - HYPOTHESIS 1 TESTING (H1)
=============================================================
Hypothesis: Low Awareness -> Higher Lifestyle Risk
Goal: Check if people with low awareness are more likely to have 
      high lifestyle risk.

Steps:
  1. Load data & encode binary variables
  2. Create 2x2 contingency table
  3. Chi-Square Test
  4. Odds Ratio Calculation
  5. Logistic Regression
  6. Final Conclusion
=============================================================
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import chi2_contingency
import os

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
DATA_PATH = r"C:\Projects\Stroke-awareness-TY-mini-project\clustering_v2\phase1_output.csv"

# ─────────────────────────────────────────────
# STEP 1  LOAD & ENCODE
# ─────────────────────────────────────────────
if not os.path.exists(DATA_PATH):
    print(f"Error: {DATA_PATH} not found. Run Phase 1 first.")
    exit(1)

df = pd.read_csv(DATA_PATH)

# Check column existence
required = ["awareness_cat", "lifestyle_risk_cat"]
for col in required:
    if col not in df.columns:
        print(f"Error: Column {col} missing from dataset.")
        exit(1)

# Binary Encoding (Low=0, High=1)
# Note: For awareness, Low Awareness = 0, High Awareness = 1
# For lifestyle risk, Low Risk = 0, High Risk = 1
df['awareness_binary']      = df['awareness_cat'].map({'Low Awareness': 0, 'High Awareness': 1})
df['lifestyle_risk_binary'] = df['lifestyle_risk_cat'].map({'Low Risk': 0, 'High Risk': 1})

print("=" * 60)
print("PHASE 2: TESTING HYPOTHESIS 1 (H1)")
print("H1: Low Awareness -> Higher Lifestyle Risk")
print("=" * 60)

# ── Check for missing mappings ──────────────────
if df['awareness_binary'].isnull().any() or df['lifestyle_risk_binary'].isnull().any():
    print("Warning: Some categories were not mapped correctly. Check values:")
    print("Awareness cat unique:", df['awareness_cat'].unique())
    print("Lifestyle risk cat unique:", df['lifestyle_risk_cat'].unique())

# ─────────────────────────────────────────────
# STEP 2  CONTINGENCY TABLE
# ─────────────────────────────────────────────
print("\nSTEP 2: CONTINGENCY TABLE (2x2)")
print("-" * 30)
# Rows: Awareness, Columns: Lifestyle Risk
# We want to see: Out of Low Awareness, how many have High Risk?
ct_h1 = pd.crosstab(df['awareness_cat'], df['lifestyle_risk_cat'])
print(ct_h1)

# ─────────────────────────────────────────────
# STEP 3  CHI-SQUARE TEST
# ─────────────────────────────────────────────
print("\nSTEP 3: CHI-SQUARE TEST")
print("-" * 30)
chi2, p, dof, expected = chi2_contingency(ct_h1)

print(f"Chi-square statistic: {chi2:.4f}")
print(f"p-value:              {p:.4f}")

if p < 0.05:
    print("Interpretation: Significant association found (p < 0.05).")
else:
    print("Interpretation: No significant association found (p >= 0.05).")

# ─────────────────────────────────────────────
# STEP 4  ODDS RATIO
# ─────────────────────────────────────────────
print("\nSTEP 4: ODDS RATIO (OR)")
print("-" * 30)
# ct_h1 format:
# lifestyle_risk_cat  High Risk  Low Risk
# awareness_cat                          
# High Awareness           ...       ...
# Low Awareness            ...       ...

try:
    # a = Low Awareness AND High Risk
    # b = Low Awareness AND Low Risk
    # c = High Awareness AND High Risk
    # d = High Awareness AND Low Risk
    a = ct_h1.loc['Low Awareness', 'High Risk']
    b = ct_h1.loc['Low Awareness', 'Low Risk']
    c = ct_h1.loc['High Awareness', 'High Risk']
    d = ct_h1.loc['High Awareness', 'Low Risk']

    # OR formula: (a/b) / (c/d) = (a*d) / (b*c)
    odds_ratio = (a * d) / (b * c)
    print(f"Odds Ratio: {odds_ratio:.4f}")

    if odds_ratio > 1:
        print(f"Interpretation: People with Low Awareness have {odds_ratio:.2f} times the odds of High Lifestyle Risk compared to High Awareness.")
    elif odds_ratio < 1:
        print("Interpretation: Low Awareness is associated with lower odds of High Lifestyle Risk.")
    else:
        print("Interpretation: No difference in odds (OR ≈ 1).")
except KeyError as e:
    print(f"Error calculating OR: Could not find key {e}. Check table labels.")

# ─────────────────────────────────────────────
# STEP 5  LOGISTIC REGRESSION
# ─────────────────────────────────────────────
print("\nSTEP 5: LOGISTIC REGRESSION")
print("-" * 30)

# We want to predict High Risk (1) using Low Awareness (0)
# To make it easier to interpret "Low Awareness predicts High Risk", 
# let's create a "is_low_awareness" column (1=Low, 0=High)
df['is_low_awareness'] = 1 - df['awareness_binary']

X = df[['is_low_awareness']]
X = sm.add_constant(X)
y = df['lifestyle_risk_binary']

try:
    model = sm.Logit(y, X).fit(disp=0)
    print(model.summary())
    
    # Extract p-value for is_low_awareness
    p_logit = model.pvalues['is_low_awareness']
    coef    = model.params['is_low_awareness']
    
    print(f"\nLogistic P-value: {p_logit:.4f}")
    print(f"Coefficient:      {coef:.4f}")
except Exception as e:
    print(f"Error in Logistic Regression: {e}")

# ─────────────────────────────────────────────
# STEP 6  CONCLUSION
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6: FINAL CONCLUSION")
print("=" * 60)

supported = False
if p < 0.05 and odds_ratio > 1:
    supported = True
    print("CONCLUSION: Hypothesis 1 (H1) is SUPPORTED.")
    print("Low awareness is statistically significantly associated with higher lifestyle risk.")
else:
    print("CONCLUSION: Hypothesis 1 (H1) is NOT SUPPORTED.")
    print("There is no significant evidence that low awareness leads to higher lifestyle risk in this dataset.")

print("\n(Note: Correlation diagnostics earlier showed r = 0.013, which consistent with these findings if p > 0.05)")
print("=" * 60)
