"""
=============================================================
PHASE 2 - HYPOTHESIS 2 TESTING (H2)
=============================================================
Hypothesis: Older Individuals -> More Cautious Behavior
Goal: Check whether older people take more immediate or 
      cautious actions compared to younger groups.

Steps:
  1. Load data & encode binary variables
  2. Create contingency table (Age vs Action)
  3. Chi-Square Test
  4. T-Test on Urgency Score (Older vs Younger)
  5. Logistic Regression
  6. Final Conclusion
=============================================================
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import chi2_contingency, ttest_ind
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

# Binary Encoding for Action (Passive=0, Proactive=1)
df['action_binary'] = df['action_cat'].map({'Passive': 0, 'Proactive': 1})

print("=" * 60)
print("PHASE 2: TESTING HYPOTHESIS 2 (H2)")
print("H2: Older Individuals -> More Cautious Behavior")
print("=" * 60)

# ─────────────────────────────────────────────
# STEP 2  CONTINGENCY TABLE
# ─────────────────────────────────────────────
print("\nSTEP 2: CONTINGENCY TABLE (Age Group vs Action)")
print("-" * 45)
# Rows: Age Group, Columns: Action Behavior
ct_h2 = pd.crosstab(df['age_group_4cat'], df['action_cat'])
print(ct_h2)

# ─────────────────────────────────────────────
# STEP 3  CHI-SQUARE TEST
# ─────────────────────────────────────────────
print("\nSTEP 3: CHI-SQUARE TEST")
print("-" * 30)
chi2, p, dof, expected = chi2_contingency(ct_h2)

print(f"Chi-square statistic: {chi2:.4f}")
print(f"p-value:              {p:.4f}")

if p < 0.05:
    print("Interpretation: Significant association found (p < 0.05). Age affects action behavior.")
else:
    print("Interpretation: No significant association found (p >= 0.05).")

# ─────────────────────────────────────────────
# STEP 4  T-TEST ON URGENCY SCORE
# ─────────────────────────────────────────────
print("\nSTEP 4: T-TEST (Urgency Score: Older vs Younger)")
print("-" * 45)

older_urgency = df[df['age_group_4cat'] == '60+']['score_urgency']
younger_urgency = df[df['age_group_4cat'] == '18-25']['score_urgency']

if len(older_urgency) > 0 and len(younger_urgency) > 0:
    t_stat, p_val = ttest_ind(older_urgency, younger_urgency)
    
    mean_older = older_urgency.mean()
    mean_younger = younger_urgency.mean()
    
    print(f"Mean Urgency (Older 60+):    {mean_older:.4f}")
    print(f"Mean Urgency (Younger 18-25): {mean_younger:.4f}")
    print(f"t-statistic:                 {t_stat:.4f}")
    print(f"p-value:                     {p_val:.4f}")
    
    if p_val < 0.05:
        if mean_older > mean_younger:
            print("Interpretation: Older individuals have significantly HIGHER urgency scores than younger individuals.")
        else:
            print("Interpretation: Older individuals have significantly LOWER urgency scores than younger individuals.")
    else:
        print("Interpretation: No statistically significant difference in urgency scores between age groups.")
else:
    print("Error: Missing data for T-test groups.")

# ─────────────────────────────────────────────
# STEP 5  LOGISTIC REGRESSION
# ─────────────────────────────────────────────
print("\nSTEP 5: LOGISTIC REGRESSION")
print("-" * 30)

# Dependent: action_binary (1=Proactive, 0=Passive)
# Independent: age_enc_v2 (Ordinal 1-4)
X = df[['age_enc_v2']]
X = sm.add_constant(X)
y = df['action_binary']

try:
    model = sm.Logit(y, X).fit(disp=0)
    print(model.summary())
    
    p_logit = model.pvalues['age_enc_v2']
    coef = model.params['age_enc_v2']
    
    print(f"\nLogistic P-value for Age: {p_logit:.4f}")
    print(f"Coefficient for Age:      {coef:.4f}")
except Exception as e:
    print(f"Error in Logistic Regression: {e}")

# ─────────────────────────────────────────────
# STEP 6  CONCLUSION
# ─────────────────────────────────────────────
print("\n" + "=" * 60)
print("STEP 6: FINAL CONCLUSION")
print("=" * 60)

h2_supported = False
if (p < 0.05 or p_logit < 0.05) and coef > 0:
    h2_supported = True
    print("CONCLUSION: Hypothesis 2 (H2) is SUPPORTED.")
    print("Older individuals are significantly more likely to take proactive/cautious behavior.")
else:
    print("CONCLUSION: Hypothesis 2 (H2) is NOT SUPPORTED.")
    print("Age does not appear to be a significant positive predictor of cautious/proactive behavior in this dataset.")

print("=" * 60)
