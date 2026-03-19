"""
=============================================================
PHASE 3: CLUSTERING PREPROCESSING
=============================================================
Goal: Select features, handle missing values, and scale data
      for all clustering algorithms.

Features Selected:
  - awareness_score
  - symptom_awareness_score
  - lifestyle_risk_score
  - score_urgency
  - age_enc_v2 (Ordinal 1-4)
  - score_action_first_symptom (Ordinal 0-3)

Output: clustered_input_scaled.csv
=============================================================
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
INPUT_PATH  = r"C:\Projects\Stroke-awareness-TY-mini-project\clustering_v2\phase1_output.csv"
OUTPUT_PATH = r"C:\Projects\Stroke-awareness-TY-mini-project\clustering_v2\clustered_input_scaled.csv"

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
if not os.path.exists(INPUT_PATH):
    print(f"Error: {INPUT_PATH} not found. Run previous phases first.")
    exit(1)

df = pd.read_csv(INPUT_PATH)

# Define features for clustering
features = [
    "awareness_score",
    "symptom_awareness_score",
    "lifestyle_risk_score",
    "score_urgency",
    "age_enc_v2",
    "score_action_first_symptom"
]

print("-" * 60)
print("PHASE 3: CLUSTERING PREPROCESSING")
print("-" * 60)

# Check for missing columns
missing_cols = [c for c in features if c not in df.columns]
if missing_cols:
    print(f"Error: Missing columns in dataset: {missing_cols}")
    exit(1)

# Drop rows with missing values in target features if any (should be 0 after Phase 1)
df_clean = df.dropna(subset=features).copy()
print(f"Rows after dropping missing values (if any): {len(df_clean)}")

# ─────────────────────────────────────────────
# SCALING
# ─────────────────────────────────────────────
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df_clean[features])

# Create a DataFrame for scaled features
df_scaled = pd.DataFrame(X_scaled, columns=[f"z_{c}" for c in features])

# Add the non-scaled original features and ID/Categorical columns for later interpretation
cols_to_keep = [
    "awareness_cat", "lifestyle_risk_cat", "symptom_awareness_cat", 
    "action_cat", "age_group_4cat", "age", "gender"
]
# Only keep columns that exist
cols_to_keep = [c for c in cols_to_keep if c in df_clean.columns]

# Reset index to ensure alignment during concatenation
df_clean = df_clean.reset_index(drop=True)
df_scaled = df_scaled.reset_index(drop=True)

# Combine original data with scaled features
df_final = pd.concat([df_clean[cols_to_keep + features], df_scaled], axis=1)

# Save the prepared dataset
df_final.to_csv(OUTPUT_PATH, index=False)

print(f"Successfully processed {len(features)} features for {len(df_final)} individuals.")
print(f"Scaled data saved to: {OUTPUT_PATH}")
print("-" * 60)
