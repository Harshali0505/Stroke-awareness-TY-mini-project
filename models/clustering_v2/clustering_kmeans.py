"""
=============================================================
PHASE 3: K-MEANS CLUSTERING
=============================================================
Goal: Segment population using K-Means and analyze results.

Steps:
  1. Load scaled data
  2. Find optimal k (Elbow Method)
  3. Fit K-Means
  4. Visualize in 2D using PCA
  5. Profile clusters
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
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
    print(f"Error: {DATA_PATH} not found. Run preprocessing_clustering.py first.")
    exit(1)

df = pd.read_csv(DATA_PATH)

# Identify feature columns (z-scaled)
features_z = [c for c in df.columns if c.startswith('z_')]
X = df[features_z]

print("-" * 60)
print("ALGORITHM: K-MEANS CLUSTERING")
print("-" * 60)

# ─────────────────────────────────────────────
# STEP 2: FIND OPTIMAL K (ELBOW)
# ─────────────────────────────────────────────
inertia = []
K_range = range(2, 11)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X)
    inertia.append(km.inertia_)

plt.figure(figsize=(8, 5))
plt.plot(K_range, inertia, marker='o', linestyle='--')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia')
plt.title('K-Means Elbow Method')
plt.grid(True)
plt.savefig(os.path.join(OUTPUT_DIR, "kmeans_elbow.png"))
plt.close()

# For simplicity, let's pick k=4 based on expected segmentation 
# (Awareness Low/High x Risk Low/High approx)
k_optimal = 4 
print(f"Fitting K-Means with k={k_optimal}...")

# ─────────────────────────────────────────────
# STEP 3: FIT K-MEANS
# ─────────────────────────────────────────────
kmeans = KMeans(n_clusters=k_optimal, random_state=42, n_init=10)
df['cluster_kmeans'] = kmeans.fit_predict(X)

# ─────────────────────────────────────────────
# STEP 4: VISUALIZATION (PCA)
# ─────────────────────────────────────────────
pca = PCA(n_components=2)
principal_components = pca.fit_transform(X)
df['PCA1'] = principal_components[:, 0]
df['PCA2'] = principal_components[:, 1]

plt.figure(figsize=(10, 7))
sns.scatterplot(x='PCA1', y='PCA2', hue='cluster_kmeans', data=df, palette='viridis', style='cluster_kmeans')
plt.title(f'K-Means Clusters (k={k_optimal}) - PCA Projection')
plt.savefig(os.path.join(OUTPUT_DIR, "kmeans_pca.png"))
plt.close()

# ─────────────────────────────────────────────
# STEP 5: PROFILING
# ─────────────────────────────────────────────
# Profile using original (non-z) scores
orig_features = [f.replace('z_', '') for f in features_z]

profile = df.groupby('cluster_kmeans')[orig_features].mean()
print("\nCluster Profiles (Mean Scores):")
print(profile)

# Count sizes
counts = df['cluster_kmeans'].value_counts().sort_index()
print("\nCluster Sizes:")
print(counts)

# Save results
df.to_csv(os.path.join(OUTPUT_DIR, "kmeans_results.csv"), index=False)
print(f"\nResults saved to kmeans_results.csv and visualizations to {OUTPUT_DIR}")
print("-" * 60)
