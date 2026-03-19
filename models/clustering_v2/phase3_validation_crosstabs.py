import pandas as pd
import os

# Define file paths and algorithms
results_dir = r"c:\Projects\Stroke-awareness-TY-mini-project\clustering_v2"
algorithms = {
    "K-Means": "kmeans_results.csv",
    "Hierarchical": "hierarchical_results.csv",
    "DBSCAN": "dbscan_results.csv",
    "GMM": "gmm_results.csv",
    "Spectral": "spectral_results.csv"
}

cat_variables = [
    "awareness_cat",
    "lifestyle_risk_cat",
    "action_cat"
]

output_file = os.path.join(results_dir, "validation_crosstabs_results.txt")

with open(output_file, "w") as f:
    f.write("="*60 + "\n")
    f.write("PHASE 3.3 - CROSS-TABS BEHAVIORAL DOMINANCE VALIDATION\n")
    f.write("="*60 + "\n\n")

    for algo_name, file_name in algorithms.items():
        file_path = os.path.join(results_dir, file_name)
        if not os.path.exists(file_path):
            f.write(f"SKIPPING {algo_name}: File not found ({file_name})\n\n")
            continue
        
        f.write(f"ALGORITHM: {algo_name}\n")
        f.write("-" * 40 + "\n")
        
        df = pd.read_csv(file_path)
        
        # Identify the cluster column name
        cluster_col = [col for col in df.columns if col.startswith("cluster_")][0]
        
        # Filter out noise for DBSCAN
        df_clean = df[df[cluster_col] != -1].copy()
        
        for var in cat_variables:
            if var not in df_clean.columns:
                f.write(f"Variable {var} not found. Skipping.\n")
                continue
            
            # Create cross-tab
            ct = pd.crosstab(df_clean[cluster_col], df_clean[var], normalize='index') * 100
            
            f.write(f"Variable: {var} (Percentages by Cluster)\n")
            f.write(ct.to_string())
            f.write("\n\n")
            
            # Check for dominance (> 60%)
            f.write("Dominance Check (>60%):\n")
            dominant_found = False
            for cluster in ct.index:
                row = ct.loc[cluster]
                max_cat = row.idxmax()
                max_val = row.max()
                if max_val > 60:
                    f.write(f"  Cluster {cluster}: Dominant category '{max_cat}' ({max_val:.1f}%)\n")
                    dominant_found = True
            
            if not dominant_found:
                f.write("  No single category dominates > 60% in any cluster.\n")
            
            f.write("-" * 20 + "\n")
        
        f.write("\n" + "="*40 + "\n\n")

print(f"Cross-Tabs validation complete. Results saved to {output_file}")
