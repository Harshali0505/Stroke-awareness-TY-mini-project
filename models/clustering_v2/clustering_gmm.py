"""
=============================================================
PHASE 3: GAUSSIAN MIXTURE MODELS (GMM)
=============================================================
Goal: Segment population using probabilistic clustering.

Steps:
  1. Load scaled data
  2. Select number of components (k=4)
  3. Fit GMM
  4. Visualize probabilities/clusters
  5. Profile results
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.mixture import GaussianMixture
from sklearn.decomposition import PCA
import os

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
DATA_PATH = r"C:\Projects\Stroke-awareness-TY-mini-project\models\clustering_v2\clustered_input_scaled.csv"
OUTPUT_DIR = r"C:\Projects\Stroke-awareness-TY-mini-project\models\clustering_v2"

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
if not os.path.exists(DATA_PATH):
    print(f"Error: {DATA_PATH} not found.")
    exit(1)

df = pd.read_csv(DATA_PATH)
features_z = [c for c in df.columns if c.startswith('z_')]
X = df[features_z]

print("-" * 60)
print("ALGORITHM: GAUSSIAN MIXTURE MODELS (GMM)")
print("-" * 60)

# ─────────────────────────────────────────────
# STEP 2 & 3: FIT GMM
# ─────────────────────────────────────────────
n_components_val = 4
print(f"Fitting GMM with n_components={n_components_val}...")
gmm = GaussianMixture(n_components=n_components_val, random_state=42)
df['cluster_gmm'] = gmm.fit_predict(X)

# Optional: Get probabilities
# probs = gmm.predict_proba(X)
# print(f"Probabilities calculated for {n_components_val} clusters.")

# ─────────────────────────────────────────────
# STEP 4: VISUALIZATION (PCA)
# ─────────────────────────────────────────────
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X)
df['PCA1'] = principal_components[:, 0]
df['PCA2'] = principal_components[:, 1]

plt.figure(figsize=(10, 7))
sns.scatterplot(x='PCA1', y='PCA2', hue='cluster_gmm', data=df, palette='magma', alpha=0.6)
plt.title(f'GMM Clusters (k={n_components_val}) - PCA Projection')
plt.savefig(os.path.join(OUTPUT_DIR, "gmm_pca.png"))
plt.close()

# ─────────────────────────────────────────────
# PROFILING
# ─────────────────────────────────────────────
orig_features = [f.replace('z_', '') for f in features_z]
profile = df.groupby('cluster_gmm')[orig_features].mean()
print("\nCluster Profiles (Mean Scores):")
print(profile)

counts = df['cluster_gmm'].value_counts().sort_index()
print("\nCluster Sizes:")
print(counts)

# Save results
df.to_csv(os.path.join(OUTPUT_DIR, "gmm_results.csv"), index=False)
print(f"\nResults saved to gmm_results.csv")
print("-" * 60)
