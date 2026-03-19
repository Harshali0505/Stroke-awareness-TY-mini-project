"""
=============================================================
PHASE 1.5 - CORRELATION DIAGNOSTICS
=============================================================
Goal: Analyze relationships between key composite variables,
      check hypotheses, and identify multicollinearity.

Variables Analyzed:
  - awareness_score
  - lifestyle_risk_score
  - symptom_awareness_score
  - score_action_first_symptom
  - score_urgency
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
INPUT_PATH  = r"C:\Projects\Stroke-awareness-TY-mini-project\clustering_v2\phase1_output.csv"
OUTPUT_DIR  = r"C:\Projects\Stroke-awareness-TY-mini-project\clustering_v2"
PLOT_NAME   = "correlation_heatmap.png"

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
if not os.path.exists(INPUT_PATH):
    print(f"Error: Could not find {INPUT_PATH}. Please run phase1_variable_definition.py first.")
    exit(1)

df = pd.read_csv(INPUT_PATH)

target_vars = [
    "awareness_score",
    "lifestyle_risk_score",
    "symptom_awareness_score",
    "score_action_first_symptom",
    "score_urgency"
]

# Ensure all columns exist
target_vars = [c for c in target_vars if c in df.columns]
print(f"Analyzing {len(target_vars)} variables: {target_vars}\n")

analysis_df = df[target_vars]

# ═══════════════════════════════════════════════════════════════
# STEP 2  DISTRIBUTION CHECKS (Sanity Check)
# ═══════════════════════════════════════════════════════════════
print("=" * 60)
print("STEP 2  DISTRIBUTION ANALYSIS")
print("=" * 60)

dist_stats = []
for var in target_vars:
    skew = analysis_df[var].skew()
    kurt = analysis_df[var].kurtosis()
    
    # Simple interpretation for the user
    if abs(skew) < 0.5:
        skew_label = "Fairly Symmetrical"
    elif abs(skew) < 1:
        skew_label = "Moderately Skewed"
    else:
        skew_label = "Highly Skewed"
        
    dist_stats.append({
        "Variable": var,
        "Skewness": round(skew, 3),
        "Kurtosis": round(kurt, 3),
        "Interpretation": skew_label
    })

dist_report = pd.DataFrame(dist_stats)
print(dist_report.to_string(index=False))
print("\nRecommendation: Pearson correlation is suitable for symmetrical distributions.")
print("If highly skewed, consider Spearman rank correlation as a robustness check.")

# ═══════════════════════════════════════════════════════════════
# STEP 3 & 4  CORRELATION MATRIX & INTERPRETATION
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 3 & 4  CORRELATION MATRIX (Pearson r)")
print("=" * 60)

corr_matrix = analysis_df.corr(method='pearson')

# Function to calculate p-values for the matrix
def calculate_pvalues(df):
    cols = df.columns
    p_values = pd.DataFrame(index=cols, columns=cols)
    for i in range(len(cols)):
        for j in range(len(cols)):
            if i == j:
                p_values.iloc[i, j] = 0.0
            else:
                coef, pval = stats.pearsonr(df.iloc[:, i], df.iloc[:, j])
                p_values.iloc[i, j] = pval
    return p_values

p_matrix = calculate_pvalues(analysis_df)

print("\nCorrelation Coefficients (r):")
print(corr_matrix.round(3).to_string())

print("\nP-Values (Significance):")
print(p_matrix.apply(lambda x: x.astype(float).map('{:.4f}'.format)).to_string())

# ═══════════════════════════════════════════════════════════════
# STEP 5 & 6  HYPOTHESIS CHECK & MULTICOLLINEARITY
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 5 & 6  SPECIFIC HYPOTHESIS & SAFETY CHECKS")
print("=" * 60)

def interpret_strength(r):
    r_abs = abs(r)
    if r_abs < 0.10: return "No relationship"
    if r_abs < 0.30: return "Weak"
    if r_abs < 0.50: return "Moderate"
    if r_abs < 0.70: return "Strong"
    return "Very strong"

# Hypotheses
hypotheses = [
    ("awareness_score", "lifestyle_risk_score", "Higher awareness should lead to lower lifestyle risk (Negative Correlation)."),
    ("symptom_awareness_score", "score_action_first_symptom", "Knowledge–Action Gap check (Positive expected)."),
    ("score_urgency", "score_action_first_symptom", "Urgency perception should drive prompt action (Positive Correlation).")
]

for var1, var2, desc in hypotheses:
    if var1 in corr_matrix.index and var2 in corr_matrix.columns:
        r = corr_matrix.loc[var1, var2]
        p = p_matrix.loc[var1, var2]
        strength = interpret_strength(r)
        sig = "Significant" if p < 0.05 else "Not Significant"
        
        print(f"\n- HYPOTHESIS: {desc}")
        print(f"  Result: r = {r:.3f}, p = {p:.4f} ({strength}, {sig})")

# Multicollinearity Check
print("\nMulticollinearity Safety Check (r > 0.80):")
found_multicollinearity = False
for i in range(len(target_vars)):
    for j in range(i + 1, len(target_vars)):
        r = corr_matrix.iloc[i, j]
        if abs(r) > 0.80:
            print(f"  [!] RED FLAG: {target_vars[i]} and {target_vars[j]} are highly correlated (r = {r:.3f})")
            found_multicollinearity = True

if not found_multicollinearity:
    print("  OK: No evidence of severe multicollinearity (r > 0.80). Models will be stable.")

# ═══════════════════════════════════════════════════════════════
# STEP 7  CORRELATION HEATMAP
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 7  GENERATING HEATMAP")
print("=" * 60)

plt.figure(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, 
            mask=mask, 
            annot=True, 
            fmt=".2f", 
            cmap='RdBu_r', 
            center=0,
            square=True, 
            linewidths=.5, 
            cbar_kws={"shrink": .8})

plt.title('Correlation Matrix of Stroke Awareness & Risk Variables', size=15)
plt.tight_layout()

plot_path = os.path.join(OUTPUT_DIR, PLOT_NAME)
plt.savefig(plot_path)
print(f"DONE: Heatmap saved to: {plot_path}")

print("\n" + "=" * 60)
print("DIAGNOSTICS COMPLETE")
print("=" * 60)
