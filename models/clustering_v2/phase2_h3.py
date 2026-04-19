"""
=============================================================
PHASE 2 - HYPOTHESIS 3 TESTING (H3)
=============================================================
Hypothesis: Knowledge–Action Gap
Goal: Identify whether people with high symptom awareness 
      still take passive or delayed actions.

Steps:
  1. Load data & encode binary variables
  2. Create contingency table (Symptom Awareness vs Action)
  3. Chi-Square Test
  4. Calculate Gap Percentage
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

# Binary Encoding
df['awareness_binary'] = df['symptom_awareness_cat'].map({
    'Low Symptom Awareness': 0, 
    'High Symptom Awareness': 1
})
df['action_binary'] = df['action_cat'].map({
    'Passive': 0, 
    'Proactive': 1
})

print("=" * 60)
print("PHASE 2: TESTING HYPOTHESIS 3 (H3)")
print("H3: Knowledge–Action Gap")
print("=" * 60)

# ─────────────────────────────────────────────
# STEP 2  CONTINGENCY TABLE
# ─────────────────────────────────────────────
print("\nSTEP 2: CONTINGENCY TABLE (Symptom Awareness vs Action)")
print("-" * 55)
# Rows: Awareness, Columns: Action
ct_h3 = pd.crosstab(df['symptom_awareness_cat'], df['action_cat'])
print(ct_h3)

# ─────────────────────────────────────────────
# STEP 3  CHI-SQUARE TEST
# ─────────────────────────────────────────────
print("\nSTEP 3: CHI-SQUARE TEST")
print("-" * 30)
chi2, p, dof, expected = chi2_contingency(ct_h3)

print(f"Chi-square statistic: {chi2:.4f}")
print(f"p-value:              {p:.4f}")

if p < 0.05:
    print("Interpretation: Significant association found (p < 0.05). Awareness and action are related.")
else:
    print("Interpretation: No significant association found (p >= 0.05).")

# ─────────────────────────────────────────────
# STEP 4  GAP PERCENTAGE
# ─────────────────────────────────────────────
print("\nSTEP 4: GAP PERCENTAGE ANALYSIS")
print("-" * 30)

high_awareness_df = df[df['symptom_awareness_cat'] == 'High Symptom Awareness']

if not high_awareness_df.empty:
    action_counts = high_awareness_df['action_cat'].value_counts(normalize=True) * 100
    passive_pct = action_counts.get('Passive', 0)
    proactive_pct = action_counts.get('Proactive', 0)
    
    print(f"In the High Awareness group ({len(high_awareness_df)} people):")
    print(f"  - Proactive (Knows & Does): {proactive_pct:.2f}%")
    print(f"  - Passive (Knows but Delays): {passive_pct:.2f}% <--- THE GAP")
    
    if passive_pct > 30:
        print(f"\nInterpretation: A substantial portion ({passive_pct:.1f}%) of knowledgeable people still delay action.")
        print("This strongly supports the 'Knowledge-Action Gap' hypothesis.")
    else:
        print(f"\nInterpretation: Most knowledgeable people ({proactive_pct:.1f}%) act proactivity. Gap is small.")
else:
    print("Error: High Awareness group not found.")

# ─────────────────────────────────────────────
# STEP 5  LOGISTIC REGRESSION
# ─────────────────────────────────────────────
print("\nSTEP 5: LOGISTIC REGRESSION")
print("-" * 30)

X = df[['awareness_binary']]
X = sm.add_constant(X)
y = df['action_binary']

try:
    model = sm.Logit(y, X).fit(disp=0)
    print(model.summary())
    
    p_logit = model.pvalues['awareness_binary']
    coef = model.params['awareness_binary']
    
    print(f"\nLogistic P-value for Awareness: {p_logit:.4f}")
    print(f"Coefficient for Awareness:      {coef:.4f}")
    
    if coef > 0 and p_logit < 0.05:
        print("Interpretation: High awareness significantly increases the odds of proactive action.")
    else:
        print("Interpretation: High awareness is not a significant positive predictor of proactive action.")
except Exception as e:
    print(f"Error in Logistic Regression: {e}")

# ─────────────────────────────────────────────
# STEP 6  CONCLUSION
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6: FINAL CONCLUSION")
print("=" * 60)

if passive_pct > 30:
    print("CONCLUSION: Hypothesis 3 (H3) is SUPPORTED.")
    print(f"Evidence shows a clear Knowledge-Action Gap: {passive_pct:.1f}% of high-awareness individuals act passively.")
else:
    print("CONCLUSION: Hypothesis 3 (H3) is NOT SUPPORTED.")
    print("There is no significant Knowledge-Action Gap in this dataset.")

print("=" * 60)
