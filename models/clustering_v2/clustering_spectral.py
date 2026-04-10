"""
=============================================================
PHASE 3: SPECTRAL CLUSTERING
=============================================================
Goal: Segment population using graph-based similarity.

Steps:
  1. Load scaled data
  2. Fit Spectral Clustering (n_clusters=4)
  3. Visualize in 2D
  4. Profile results
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import SpectralClustering
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
print("ALGORITHM: SPECTRAL CLUSTERING")
print("-" * 60)

# ─────────────────────────────────────────────
# STEP 2: FIT SPECTRAL
# ─────────────────────────────────────────────
# Using nearest_neighbors affinity as RBF might be slow/memory intensive for 6k rows
k_val = 4
print(f"Fitting Spectral Clustering with k={k_val}... (This might take a while)")
sc = SpectralClustering(n_clusters=k_val, affinity='nearest_neighbors', random_state=42, n_jobs=-1)
df['cluster_spectral'] = sc.fit_predict(X)

# ─────────────────────────────────────────────
# STEP 3: VISUALIZATION (PCA)
# ─────────────────────────────────────────────
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X)
df['PCA1'] = principal_components[:, 0]
df['PCA2'] = principal_components[:, 1]

plt.figure(figsize=(10, 7))
sns.scatterplot(x='PCA1', y='PCA2', hue='cluster_spectral', data=df, palette='Spectral', alpha=0.6)
plt.title(f'Spectral Clusters (k={k_val}) - PCA Projection')
plt.savefig(os.path.join(OUTPUT_DIR, "spectral_pca.png"))
plt.close()

# ─────────────────────────────────────────────
# PROFILING
# ─────────────────────────────────────────────
orig_features = [f.replace('z_', '') for f in features_z]
profile = df.groupby('cluster_spectral')[orig_features].mean()
print("\nCluster Profiles (Mean Scores):")
print(profile)

counts = df['cluster_spectral'].value_counts().sort_index()
print("\nCluster Sizes:")
print(counts)

# Save results
df.to_csv(os.path.join(OUTPUT_DIR, "spectral_results.csv"), index=False)
print(f"\nResults saved to spectral_results.csv")
print("-" * 60)
