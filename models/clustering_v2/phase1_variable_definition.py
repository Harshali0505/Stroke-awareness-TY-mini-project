"""
=============================================================
PHASE 1  VARIABLE DEFINITION (Clustering Restart)
=============================================================
Goal: Build stable, well-defined variables before any clustering.

Steps:
  1.1  Clean lifestyle variables (missing values + BMI outliers)
  1.2  Standardize (Z-score)
  1.3  Create lifestyle_risk_score
  1.4  Cronbach's Alpha (internal consistency)
  1.5  Create categorical variables (median split)
  1.6  Validate categorization
  1.7  Final sanity check + save
=============================================================
"""

import pandas as pd
import numpy as np

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
DATA_PATH   = r"C:\Projects\Stroke-awareness-TY-mini-project\current_work\awareness_scores.csv"
OUTPUT_PATH = r"C:\Projects\Stroke-awareness-TY-mini-project\clustering_v2\phase1_output.csv"

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)

# Fix the corrupted column name that has a trailing ="
df.columns = [c.replace('\"=', '').strip() for c in df.columns]

print(f"Dataset loaded: {df.shape[0]} rows × {df.shape[1]} columns\n")

# ─────────────────────────────────────────────
# COLUMN ALIASES (map to clean short names)
# ─────────────────────────────────────────────
SMOKE_COL    = "do_you_smoke?_if_so,_how_much_and_often?"
ALCOHOL_COL  = "do_you__consume_alcohol?"
ACTIVITY_COL = "do_you_engage_in_regular_physical_activity_or_exercise?"
BMI_COL      = "bmi"

# ═══════════════════════════════════════════════════════════════
# STEP 1.1  CLEAN BEFORE YOU COMBINE
# ═══════════════════════════════════════════════════════════════
print("=" * 60)
print("STEP 1.1  MISSING VALUE CHECK & CLEANING")
print("=" * 60)

# ── 1. Encode lifestyle columns to numeric ──────────────────
#   Smoking:  no=0, yes=1  (higher = worse)
#   Alcohol:  no=0, yes=1  (higher = worse)
#   Inactivity: yes=0 (active), no=1 (inactive) → higher = worse
#   BMI: continuous (higher = worse for stroke risk)

smoke_map    = {"no": 0, "yes": 1}
alcohol_map  = {"no": 0, "yes": 1}
activity_map = {"yes": 0, "no": 1}   # FLIPPED: inactive = 1 = higher risk

df["smoking_enc"]    = df[SMOKE_COL].str.strip().str.lower().map(smoke_map)
df["alcohol_enc"]    = df[ALCOHOL_COL].str.strip().str.lower().map(alcohol_map)
df["inactivity_enc"] = df[ACTIVITY_COL].str.strip().str.lower().map(activity_map)

# ── 2. BMI: coerce to numeric, cap extreme outliers ────────
df["bmi_clean"] = pd.to_numeric(df[BMI_COL], errors="coerce")

bmi_outlier_threshold = 80
n_bmi_outliers = (df["bmi_clean"] > bmi_outlier_threshold).sum()
print(f"\nBMI outliers (> {bmi_outlier_threshold}): {n_bmi_outliers} rows")
print(f"  Examples: {sorted(df.loc[df['bmi_clean'] > bmi_outlier_threshold, 'bmi_clean'].dropna().tolist(), reverse=True)[:5]}")

# Cap BMI at 80 (extreme values are data entry errors)
df["bmi_clean"] = df["bmi_clean"].clip(upper=bmi_outlier_threshold)

# ── 3. Count missing values ─────────────────────────────────
lifestyle_cols = {
    "Smoking":             "smoking_enc",
    "Alcohol":             "alcohol_enc",
    "Physical Inactivity": "inactivity_enc",
    "BMI":                 "bmi_clean",
}

print("\nMissing value counts for lifestyle variables:")
print("-" * 40)
total_missing = 0
for label, col in lifestyle_cols.items():
    n_miss = df[col].isnull().sum()
    pct    = n_miss / len(df) * 100
    print(f"  {label:<22}: {n_miss:>4} missing  ({pct:.1f}%)")
    total_missing += n_miss

print(f"\nTotal missing across 4 variables: {total_missing}")

# ── 4. Handle missing values ────────────────────────────────
# Strategy: if a variable has < 5% missing → impute with median
#           (median for binary = mode; for BMI = median)
for label, col in lifestyle_cols.items():
    n_miss = df[col].isnull().sum()
    pct    = n_miss / len(df) * 100
    if n_miss > 0:
        fill_val = df[col].median()
        df[col]  = df[col].fillna(fill_val)
        print(f"  Imputed {label} ({n_miss} rows) with median = {fill_val:.2f}")

print(f"\nRows remaining after cleaning: {len(df)}")

# ── 5. Verify direction: higher = higher risk ───────────────
print("\nDirection check (higher value = higher risk):")
print(f"  Smoking    → 0=no, 1=yes            ✔ higher = worse")
print(f"  Alcohol    → 0=no, 1=yes            ✔ higher = worse")
print(f"  Inactivity → 0=active, 1=inactive   ✔ higher = worse")
print(f"  BMI        → continuous, capped @80 ✔ higher = worse")

# ═══════════════════════════════════════════════════════════════
# STEP 1.2  STANDARDIZE (Z-SCORE)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 1.2  Z-SCORE STANDARDIZATION")
print("=" * 60)

def z_score(series):
    return (series - series.mean()) / series.std()

df["z_smoking"]    = z_score(df["smoking_enc"])
df["z_alcohol"]    = z_score(df["alcohol_enc"])
df["z_inactivity"] = z_score(df["inactivity_enc"])
df["z_bmi"]        = z_score(df["bmi_clean"])

z_cols = ["z_smoking", "z_alcohol", "z_inactivity", "z_bmi"]

print("\nZ-score stats (mean ≈ 0, std ≈ 1):")
print("-" * 50)
for col in z_cols:
    print(f"  {col:<16}: mean={df[col].mean():+.4f}  std={df[col].std():.4f}")

# ═══════════════════════════════════════════════════════════════
# STEP 1.3  CREATE LIFESTYLE RISK SCORE
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 1.3  LIFESTYLE RISK SCORE")
print("=" * 60)

df["lifestyle_risk_score"] = df[z_cols].mean(axis=1)

print(f"\nlifestyle_risk_score summary:")
print(df["lifestyle_risk_score"].describe().round(4).to_string())
print("\n  Higher score → worse lifestyle risk")

# ═══════════════════════════════════════════════════════════════
# STEP 1.4  CRONBACH'S ALPHA (Internal Consistency)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 1.4  CRONBACH'S ALPHA")
print("=" * 60)

def cronbach_alpha(df_items):
    """
    Compute Cronbach's Alpha for a DataFrame of items.
    Formula: alpha = (k / (k-1)) * (1 - Σvar_i / var_total)
    """
    k         = df_items.shape[1]
    item_vars = df_items.var(axis=0, ddof=1)
    total_var = df_items.sum(axis=1).var(ddof=1)
    alpha     = (k / (k - 1)) * (1 - item_vars.sum() / total_var)
    return alpha

items_df = df[z_cols]
alpha    = cronbach_alpha(items_df)

print(f"\nCronbach's Alpha = {alpha:.4f}")

if alpha >= 0.7:
    interpretation = "Good (≥ 0.7) ✔"
elif alpha >= 0.6:
    interpretation = "Acceptable (0.6 to 0.7) ⚠"
else:
    interpretation = "Weak (< 0.6) — variables may not form a coherent group ✗"

print(f"Interpretation  : {interpretation}")

# ═══════════════════════════════════════════════════════════════
# STEP 1.5   CREATE CATEGORICAL VARIABLES (MEDIAN SPLIT)
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 1.5  CATEGORICAL VARIABLES (MEDIAN SPLIT)")
print("=" * 60)

# ── A. Awareness Category ───────────────────────────────────
med_awareness = df["awareness_score"].median()
df["awareness_cat"] = np.where(
    df["awareness_score"] <= med_awareness, "Low Awareness", "High Awareness"
)
print(f"\nA. awareness_cat  (median = {med_awareness:.2f})")
print(df["awareness_cat"].value_counts().to_string())

# ── B. Lifestyle Risk Category ──────────────────────────────
med_lifestyle = df["lifestyle_risk_score"].median()
df["lifestyle_risk_cat"] = np.where(
    df["lifestyle_risk_score"] <= med_lifestyle, "Low Risk", "High Risk"
)
print(f"\nB. lifestyle_risk_cat  (median = {med_lifestyle:.4f})")
print(df["lifestyle_risk_cat"].value_counts().to_string())

# ── C. Symptom Awareness Category ──────────────────────────
med_symptom = df["symptom_awareness_score"].median()
df["symptom_awareness_cat"] = np.where(
    df["symptom_awareness_score"] <= med_symptom, "Low Symptom Awareness", "High Symptom Awareness"
)
print(f"\nC. symptom_awareness_cat  (median = {med_symptom:.2f})")
print(df["symptom_awareness_cat"].value_counts().to_string())

# ── D. Action Category ──────────────────────────────────────
# score_action_first_symptom: 0=no action/unaware, 1=within a week, 2=within a day, 3=immediately
# Proactive: score >= 2 (within a day OR immediately)
# Passive:   score <  2 (no action, within a week, or other)
df["action_cat"] = np.where(
    df["score_action_first_symptom"] >= 2, "Proactive", "Passive"
)
print(f"\nD. action_cat  (Proactive if score_action_first_symptom >= 2)")
print(df["action_cat"].value_counts().to_string())
print(f"   score_action_first_symptom distribution:")
print(df["score_action_first_symptom"].value_counts().sort_index().to_string())

# ── E. Age Category (4-Group Balanced - v2) ──────────────────
# Mapping based on typical public health research for Stroke:
# 1. Young Adults (18–25)
# 2. Early Middle Age (26–40)
# 3. High-Risk Age (41–60)
# 4. Elderly (60+)

# First, ensure clean mapping from raw labels
age_label_map = {
    "0-15":  "18-25", # Merge very young into youngest adult group if exists
    "15-25": "18-25",
    "26-40": "26-40",
    "41-60": "41-60",
    "60+":   "60+"
}

df["age_group_4cat"] = df["age"].str.strip().map(age_label_map)

# Ordinal encoding for the 4 categories
age_enc_4cat_map = {
    "18-25": 1,
    "26-40": 2,
    "41-60": 3,
    "60+":   4
}
df["age_enc_v2"] = df["age_group_4cat"].map(age_enc_4cat_map)

print(f"\nE. age_group_4cat (4-Group Structure)")
print(df["age_group_4cat"].value_counts().sort_index().to_string())

# ═══════════════════════════════════════════════════════════════
# STEP 1.6  VALIDATE CATEGORIZATION
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 1.6  VALIDATE CATEGORIZATION (Split Balance)")
print("=" * 60)

cat_vars = [
    "awareness_cat",
    "lifestyle_risk_cat",
    "symptom_awareness_cat",
    "action_cat",
    "age_group_4cat",
]

print(f"\n{'Variable':<25} {'Split (Min/Max)':<20} {'Status'}")
print("-" * 70)
for var in cat_vars:
    # Use age_group_4cat for the age variable check
    check_var = "age_group_4cat" if var == "age_cat" else var
    
    counts   = df[check_var].value_counts()
    total    = counts.sum()
    pct_max  = counts.max() / total * 100
    pct_min  = counts.min() / total * 100
    split_str = f"{pct_min:.1f}% / {pct_max:.1f}%"
    
    # Sanity Test Logic:
    # 1. No group under 5%
    # 2. No group over 85%
    is_balanced = (pct_min >= 5.0) and (pct_max <= 85.0)
    
    status = "✔ Balanced" if is_balanced else "⚠ Imbalanced"
    print(f"  {var:<23} {split_str:<20} {status}")
    
    if not is_balanced:
        print(f"    [!] WARNING: {var} distribution is outside safety limits (5%-85%)")

# ═══════════════════════════════════════════════════════════════
# STEP 1.7  FINAL SANITY CHECK + SAVE
# ═══════════════════════════════════════════════════════════════
print("\n" + "=" * 60)
print("STEP 1.7  FINAL SANITY CHECK")
print("=" * 60)

required_cols = [
    "awareness_score",
    "lifestyle_risk_score",
    "symptom_awareness_score",
    "score_action_first_symptom",
    "score_urgency",
    "awareness_cat",
    "lifestyle_risk_cat",
    "symptom_awareness_cat",
    "action_cat",
    "age_group_4cat",
    "age_enc_v2",
]

print("\nRequired columns check:")
all_present = True
for col in required_cols:
    present = col in df.columns
    missing = df[col].isnull().sum() if present else "N/A"
    status  = "✔" if present else "✗ MISSING"
    print(f"  {col:<35} {status}  (nulls: {missing})")
    if not present:
        all_present = False

if all_present:
    print("\n✅ All 10 required columns are present and ready.")
else:
    print("\n❌ Some columns are missing — check above.")

# ── Save output ─────────────────────────────────────────────
output_cols = required_cols + z_cols + [
    "smoking_enc", "alcohol_enc", "inactivity_enc", "bmi_clean",
    "age_enc_v2", "age_group_4cat", "age", "gender", "educational_level", "salary",
    "score_specialist", "score_first_contact", "score_location",
    "score_advice", "score_confusion", "score_numbness",
    "score_vision", "score_nosebleed", "score_symptoms",
    "score_risk", "tia",
]

# Only keep columns that actually exist
output_cols = [c for c in output_cols if c in df.columns]
# Remove duplicates while preserving order
seen = set()
output_cols_dedup = []
for c in output_cols:
    if c not in seen:
        output_cols_dedup.append(c)
        seen.add(c)

df[output_cols_dedup].to_csv(OUTPUT_PATH, index=False)
print(f"\n✅ Phase 1 output saved to:\n   {OUTPUT_PATH}")
print(f"   Shape: {len(df)} rows × {len(output_cols_dedup)} columns")
print("\n" + "=" * 60)
print("PHASE 1 COMPLETE — Ready for Phase 2 (Clustering)")
print("=" * 60)