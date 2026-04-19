import pandas as pd
import numpy as np
import os
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

# ─────────────────────────────────────────────
# SETTINGS & PATHS
# ─────────────────────────────────────────────
BASE_DIR = r"C:\Projects\Stroke-awareness-TY-mini-project\models\clustering_v2"
DATA_PATH = os.path.join(BASE_DIR, "clustered_input_scaled.csv")

MODELS = {
    "K-Means": "kmeans_results.csv",
    "GMM": "gmm_results.csv",
    "Hierarchical": "hierarchical_results.csv",
    "Spectral": "spectral_results.csv",
    "DBSCAN": "dbscan_results.csv"
}

# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
if not os.path.exists(DATA_PATH):
    print(f"Error: Data path {DATA_PATH} not found.")
    exit(1)

df_scaled = pd.read_csv(DATA_PATH)
features_z = [c for c in df_scaled.columns if c.startswith('z_')]
X = df_scaled[features_z]

results = []

print("-" * 80)
print(f"{'Model':<20} | {'Silhouette':<12} | {'Davies-Bouldin':<15} | {'Calinski-Harabasz':<18}")
print("-" * 80)

# ─────────────────────────────────────────────
# METRIC CALCULATION
# ─────────────────────────────────────────────
for model_name, file_name in MODELS.items():
    file_path = os.path.join(BASE_DIR, file_name)
    
    if not os.path.exists(file_path):
        print(f"{model_name:<20} | File not found.")
        continue
    
    df_res = pd.read_csv(file_path)
    
    # Identify the cluster column
    cluster_col = [c for c in df_res.columns if c.startswith('cluster_')][0]
    labels = df_res[cluster_col]
    
    # Handle DBSCAN noise (-1)
    # Most metrics don't support noise points as a 'cluster' for valid comparison
    # We will compute metrics on the subset of data that is NOT noise for DBSCAN
    if model_name == "DBSCAN":
        mask = labels != -1
        X_eval = X[mask]
        labels_eval = labels[mask]
        n_clusters = len(np.unique(labels_eval))
        noise_pct = (labels == -1).sum() / len(labels) * 100
        
        if n_clusters < 2:
            print(f"{model_name:<20} | Too few clusters ({n_clusters}) or too much noise ({noise_pct:.1f}%). SKIPPING METRICS.")
            continue
    else:
        X_eval = X
        labels_eval = labels
        noise_pct = 0.0

    try:
        # Calculate scores
        s_score = silhouette_score(X_eval, labels_eval)
        db_index = davies_bouldin_score(X_eval, labels_eval)
        ch_index = calinski_harabasz_score(X_eval, labels_eval)
        
        results.append({
            "Model": model_name,
            "Silhouette": s_score,
            "Davies-Bouldin": db_index,
            "Calinski-Harabasz": ch_index,
            "Noise %": noise_pct,
            "Clusters": len(np.unique(labels_eval))
        })
        
        print(f"{model_name:<20} | {s_score:<12.4f} | {db_index:<15.4f} | {ch_index:<18.2f}")
        
    except Exception as e:
        print(f"{model_name:<20} | Error: {str(e)}")

print("-" * 80)

# ─────────────────────────────────────────────
# SAVE SUMMARY
# ─────────────────────────────────────────────
summary_df = pd.DataFrame(results)
summary_csv = os.path.join(BASE_DIR, "clustering_model_comparison.csv")
summary_df.to_csv(summary_csv, index=False)
print(f"\nComparative analysis saved to {summary_csv}")
