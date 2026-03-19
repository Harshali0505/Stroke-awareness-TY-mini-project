"""
=============================================================
PHASE 3: HIERARCHICAL CLUSTERING
=============================================================
Goal: Segment population using Agglomerative Clustering.

Steps:
  1. Load scaled data
  2. Compute Linkage Matrix (Ward)
  3. Plot Dendrogram
  4. Cut Tree (k=4)
  5. Profile results
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
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
print("ALGORITHM: HIERARCHICAL CLUSTERING")
print("-" * 60)

# ─────────────────────────────────────────────
# STEP 2: LINKAGE
# ─────────────────────────────────────────────
print("Computing Ward linkage... (This may take a moment for 6000+ rows)")
Z = linkage(X, method='ward')

# ─────────────────────────────────────────────
# STEP 3: DENDROGRAM
# ─────────────────────────────────────────────
plt.figure(figsize=(12, 7))
dendrogram(Z, truncate_mode='lastp', p=30, leaf_rotation=90., leaf_font_size=10., show_contracted=True)
plt.title('Hierarchical Clustering Dendrogram (Ward Linkage)')
plt.xlabel('Cluster size')
plt.ylabel('Distance')
plt.savefig(os.path.join(OUTPUT_DIR, "hierarchical_dendrogram.png"))
plt.close()

# ─────────────────────────────────────────────
# STEP 4: CUT TREE
# ─────────────────────────────────────────────
# Cutting at k=4 to stay consistent with K-Means for comparison
k = 4
df['cluster_hierarchical'] = fcluster(Z, t=k, criterion='maxclust')

# ─────────────────────────────────────────────
# STEP 5: VISUALIZATION (PCA)
# ─────────────────────────────────────────────
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X)
df['PCA1'] = principal_components[:, 0]
df['PCA2'] = principal_components[:, 1]

plt.figure(figsize=(10, 7))
sns.scatterplot(x='PCA1', y='PCA2', hue='cluster_hierarchical', data=df, palette='Set1', alpha=0.6)
plt.title(f'Hierarchical Clusters (k={k}) - PCA Projection')
plt.savefig(os.path.join(OUTPUT_DIR, "hierarchical_pca.png"))
plt.close()

# ─────────────────────────────────────────────
# PROFILING
# ─────────────────────────────────────────────
orig_features = [f.replace('z_', '') for f in features_z]
profile = df.groupby('cluster_hierarchical')[orig_features].mean()
print("\nCluster Profiles (Mean Scores):")
print(profile)

counts = df['cluster_hierarchical'].value_counts().sort_index()
print("\nCluster Sizes:")
print(counts)

# Save results
df.to_csv(os.path.join(OUTPUT_DIR, "hierarchical_results.csv"), index=False)
print(f"\nResults saved to hierarchical_results.csv")
print("-" * 60)
