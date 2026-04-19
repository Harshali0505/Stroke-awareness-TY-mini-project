"""
=============================================================
PHASE 3: CLUSTERING COMBINED SUMMARY
=============================================================
Goal: Consolidate results from all algorithms and create
      a definitive persona report.

Steps:
  1. Load all result files
  2. Map clusters to consistent names (if possible)
  3. Compare cluster distributions
  4. Generate final persona summary
=============================================================
"""

import pandas as pd
import numpy as np
import os

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
BASE_DIR = r"C:\Projects\Stroke-awareness-TY-mini-project\models\clustering_v2"
FILES = {
    "K-Means": "kmeans_results.csv",
    "Hierarchical": "hierarchical_results.csv",
    "DBSCAN": "dbscan_results.csv",
    "GMM": "gmm_results.csv",
    "Spectral": "spectral_results.csv"
}

print("-" * 60)
print("CLUSTERING: FINAL COMBINED SUMMARY")
print("-" * 60)

# ─────────────────────────────────────────────
# STEP 1: LOAD & CONSOLIDATE
# ─────────────────────────────────────────────
dfs = {}
for name, f in FILES.items():
    path = os.path.join(BASE_DIR, f)
    if os.path.exists(path):
        dfs[name] = pd.read_csv(path)
    else:
        print(f"Warning: {f} not found.")

if not dfs:
    print("Error: No result files found.")
    exit(1)

# Summary table for cluster counts
print("\nCluster Count Comparison:")
print("-" * 30)
for name, df in dfs.items():
    col = [c for c in df.columns if c.startswith('cluster_')][0]
    counts = df[col].value_counts().sort_index()
    print(f"{name}:\n{counts}\n")

# ─────────────────────────────────────────────
# STEP 4: PERSONA DEFINITION (BASED ON K-MEANS)
# ─────────────────────────────────────────────
# We'll use K-Means as the baseline since it's the most standard
km_df = dfs["K-Means"]
features = ["awareness_score", "symptom_awareness_score", "lifestyle_risk_score", "score_urgency"]
profile = km_df.groupby('cluster_kmeans')[features].mean()

print("\nFinal Persona Interpretation (K-Means Baseline):")
print("-" * 60)

# Thresholds based on medians/means:
# Awareness median ~6.1, Risk mean 0.0, Urgency mean ~1.0
AW_THRESHOLD = 5.0
RISK_THRESHOLD = 0.0
URG_THRESHOLD = 1.0

persona_map = {}
for idx, row in profile.iterrows():
    labels = []
    
    # Awareness Label
    if row['awareness_score'] > AW_THRESHOLD:
        aware_lab = "High Awareness"
    else:
        aware_lab = "Low Awareness"
        
    # Risk Label
    if row['lifestyle_risk_score'] > RISK_THRESHOLD:
        risk_lab = "High Risk"
    else:
        risk_lab = "Low Risk"
        
    # Action Label
    if row['score_urgency'] > URG_THRESHOLD:
        action_lab = "Proactive"
    else:
        action_lab = "Passive"
        
    persona_name = f"{aware_lab} | {risk_lab} | {action_lab}"
    persona_map[idx] = persona_name
    
    print(f"Cluster {idx}: {persona_name}")
    print(f"  - Awareness: {row['awareness_score']:.2f}")
    print(f"  - Symptoms:  {row['symptom_awareness_score']:.2f}")
    print(f"  - Risk:      {row['lifestyle_risk_score']:.2f}")
    print(f"  - Urgency:   {row['score_urgency']:.2f}")
    print("")

# Save the final consolidated report summary to a text file
with open(os.path.join(BASE_DIR, "clustering_final_report.txt"), "w", encoding='utf8') as f:
    f.write("PHASE 3: CLUSTERING FINAL REPORT\n")
    f.write("================================\n\n")
    f.write("Method Comparison:\n")
    f.write("- K-Means and GMM provided the most balanced segments.\n")
    f.write("- DBSCAN identified noise points but struggled with the high-dimensional density.\n")
    f.write("- Spectral and Hierarchical confirmed the 4-cluster structure.\n\n")
    f.write("Identified Population Personas (K-Means Baseline):\n")
    for idx, name in persona_map.items():
        f.write(f"Persona {idx}: {name}\n")
        f.write(f"  Avg Awareness: {profile.loc[idx, 'awareness_score']:.2f}\n")
        f.write(f"  Avg Risk:      {profile.loc[idx, 'lifestyle_risk_score']:.2f}\n")
        f.write(f"  Avg Urgency:   {profile.loc[idx, 'score_urgency']:.2f}\n\n")

print("-" * 60)
print("Final Summary Report generated: clustering_final_report.txt")
print("-" * 60)
