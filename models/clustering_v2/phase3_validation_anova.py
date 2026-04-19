import pandas as pd
from scipy.stats import f_oneway, kruskal, shapiro
import os

# Define file paths and algorithms
results_dir = r"C:\Projects\Stroke-awareness-TY-mini-project\models\clustering_v2"
algorithms = {
    "K-Means": "kmeans_results.csv",
    "Hierarchical": "hierarchical_results.csv",
    "DBSCAN": "dbscan_results.csv",
    "GMM": "gmm_results.csv",
    "Spectral": "spectral_results.csv"
}

variables = [
    "awareness_score",
    "lifestyle_risk_score",
    "score_action_first_symptom",
    "score_urgency",
    "age_enc_v2" # Numericage encoding used in clustering
]

output_file = os.path.join(results_dir, "validation_anova_results.txt")

with open(output_file, "w") as f:
    f.write("="*60 + "\n")
    f.write("PHASE 3.2 - ANOVA / KRUSKAL-WALLIS VALIDATION RESULTS\n")
    f.write("="*60 + "\n\n")

    for algo_name, file_name in algorithms.items():
        file_path = os.path.join(results_dir, file_name)
        if not os.path.exists(file_path):
            f.write(f"SKIPPING {algo_name}: File not found ({file_name})\n\n")
            continue
        
        f.write(f"ALGORITHM: {algo_name}\n")
        f.write("-" * 40 + "\n")
        
        df = pd.read_csv(file_path)
        
        # Identify the cluster column name (e.g., cluster_kmeans, cluster_hierarchical, etc.)
        cluster_col = [col for col in df.columns if col.startswith("cluster_")][0]
        
        # Filter out noise/unassigned if any (mostly for DBSCAN)
        df_clean = df[df[cluster_col] != -1].copy()
        
        clusters = sorted(df_clean[cluster_col].unique())
        f.write(f"Validated Clusters: {clusters}\n\n")
        
        for var in variables:
            if var not in df_clean.columns:
                f.write(f"Variable {var} not found. Skipping.\n")
                continue
                
            groups = [df_clean[df_clean[cluster_col] == i][var] for i in clusters]
            
            # Check for normality using Shapiro-Wilk (on a sample if too large)
            # However, for simplicity and robustness as suggested by the instructions, 
            # we can run both or choose Kruskal if we suspect skewness.
            # Here we follow the instruction's primary path (ANOVA) but mention Kruskal.
            
            try:
                f_stat, p_value_anova = f_oneway(*groups)
                h_stat, p_value_kruskal = kruskal(*groups)
                
                f.write(f"Variable: {var}\n")
                f.write(f"  ANOVA F-statistic: {f_stat:.3f}, P-value: {p_value_anova:.5e}\n")
                f.write(f"  Kruskal H-statistic: {h_stat:.3f}, P-value: {p_value_kruskal:.5e}\n")
                
                interpretation = ""
                if p_value_anova < 0.001:
                    interpretation = "VERY STRONG separation"
                elif p_value_anova < 0.05:
                    interpretation = "Statistically significant separation"
                else:
                    interpretation = "NOT meaningfully different"
                
                f.write(f"  Interpretation: {interpretation}\n")
                f.write("-" * 20 + "\n")
            except Exception as e:
                f.write(f"  Error calculating stats for {var}: {str(e)}\n")
        
        f.write("\n" + "="*40 + "\n\n")

print(f"ANOVA validation complete. Results saved to {output_file}")
