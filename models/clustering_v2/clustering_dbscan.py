"""
=============================================================
PHASE 3: DBSCAN CLUSTERING
=============================================================
Goal: Segment population using Density-Based Clustering.

Steps:
  1. Load scaled data
  2. Tune eps and min_samples
  3. Fit DBSCAN
  4. Visualize noise (-1) vs clusters
  5. Profile results
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import os

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
DATA_PATH = r"C:\Projects\Stroke-awareness-TY-mini-project\clustering_v2\clustered_input_scaled.csv"
OUTPUT_DIR = r"C:\Projects\Stroke-awareness-TY-mini-project\clustering_v2"

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
print("ALGORITHM: DBSCAN CLUSTERING")
print("-" * 60)

# ─────────────────────────────────────────────
# STEP 2 & 3: FIT DBSCAN
# ─────────────────────────────────────────────
# Since we have 6 features, min_samples=2*dim = 12 is a good rule of thumb
# eps requires tuning depending on distance. Let's try 0.5 first.
eps_val = 0.5
min_samples_val = 12

print(f"Fitting DBSCAN with eps={eps_val}, min_samples={min_samples_val}...")
dbscan = DBSCAN(eps=eps_val, min_samples=min_samples_val)
df['cluster_dbscan'] = dbscan.fit_predict(X)

# ─────────────────────────────────────────────
# STEP 4: VISUALIZATION (PCA)
# ─────────────────────────────────────────────
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X)
df['PCA1'] = principal_components[:, 0]
df['PCA2'] = principal_components[:, 1]

plt.figure(figsize=(10, 7))
# Cluster -1 is noise, let's highlight it
sns.scatterplot(x='PCA1', y='PCA2', hue='cluster_dbscan', data=df, palette='tab10', alpha=0.6)
plt.title(f'DBSCAN Clusters (eps={eps_val}) - PCA Projection')
plt.savefig(os.path.join(OUTPUT_DIR, "dbscan_pca.png"))
plt.close()

# ─────────────────────────────────────────────
# PROFILING
# ─────────────────────────────────────────────
n_clusters = len(set(df['cluster_dbscan'])) - (1 if -1 in df['cluster_dbscan'] else 0)
n_noise = list(df['cluster_dbscan']).count(-1)

print(f"Number of clusters found: {n_clusters}")
print(f"Number of noise points:   {n_noise} ({ (n_noise/len(df))*100:.1f}%)")

if n_clusters > 0:
    orig_features = [f.replace('z_', '') for f in features_z]
    profile = df[df['cluster_dbscan'] != -1].groupby('cluster_dbscan')[orig_features].mean()
    print("\nCluster Profiles (Mean Scores, excluding Noise):")
    print(profile)

counts = df['cluster_dbscan'].value_counts().sort_index()
print("\nCluster Sizes (including -1 for Noise):")
print(counts)

# Save results
df.to_csv(os.path.join(OUTPUT_DIR, "dbscan_results.csv"), index=False)
print(f"\nResults saved to dbscan_results.csv")
print("-" * 60)
