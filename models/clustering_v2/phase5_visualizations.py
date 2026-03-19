import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams['figure.figsize'] = (10, 6)

# Paths
results_dir = r"c:\Projects\Stroke-awareness-TY-mini-project\clustering_v2"
input_file = os.path.join(results_dir, "kmeans_results.csv")
output_dir = os.path.join(results_dir, "phase5_outputs")
os.makedirs(output_dir, exist_ok=True)

# Load data
df = pd.read_csv(input_file)

# --- Step 1: Descriptive Visuals ---

# Histograms with mean lines
vars_to_plot = ["awareness_score", "lifestyle_risk_score", "score_urgency"]
for var in vars_to_plot:
    plt.figure()
    sns.histplot(df[var], kde=True, color='teal')
    plt.axvline(df[var].mean(), color='red', linestyle='--', label=f'Mean: {df[var].mean():.2f}')
    plt.axvline(df[var].median(), color='blue', linestyle='-', label=f'Median: {df[var].median():.2f}')
    plt.title(f'Distribution of {var.replace("_", " ").title()}')
    plt.legend()
    plt.savefig(os.path.join(output_dir, f"dist_{var}.png"))
    plt.close()

# Scatter plot: Awareness vs Action Score
plt.figure()
sns.regplot(data=df, x="awareness_score", y="score_action_first_symptom", scatter_kws={'alpha':0.3}, line_kws={'color':'red'})
plt.title("Correlation: Awareness Score vs Action Score")
plt.savefig(os.path.join(output_dir, "scatter_awareness_action.png"))
plt.close()

# --- Step 2: Hypothesis Visuals ---

# H1: Awareness Levels vs % Taking Immediate Action
plt.figure()
ct_h1 = pd.crosstab(df['awareness_cat'], df['action_cat'], normalize='index') * 100
ct_h1.plot(kind='bar', stacked=True, color=['#ff9999','#66b3ff'])
plt.title("H1: Awareness Levels vs Action Propensity")
plt.ylabel("Percentage (%)")
plt.xticks(rotation=0)
plt.savefig(os.path.join(output_dir, "h1_awareness_action_bar.png"))
plt.close()

# H2: Urgency Scores by Risk Group (Violin Plot)
plt.figure()
sns.violinplot(data=df, x="lifestyle_risk_cat", y="score_urgency", inner="quart", palette="Set2")
plt.title("H2: Urgency Perception by Lifestyle Risk Category")
plt.savefig(os.path.join(output_dir, "h2_urgency_risk_violin.png"))
plt.close()

# H3: Age vs Awareness Heatmap
plt.figure()
ct_h3 = pd.crosstab(df['age_group_4cat'], df['awareness_cat'])
sns.heatmap(ct_h3, annot=True, fmt="d", cmap="YlGnBu")
plt.title("H3: Population Distribution (Age vs Awareness)")
plt.savefig(os.path.join(output_dir, "h3_age_awareness_heatmap.png"))
plt.close()

# --- Step 3: Cluster Interpretation ---

# Boxplots for key variables per cluster
key_vars = ["awareness_score", "lifestyle_risk_score", "score_urgency", "score_action_first_symptom"]
plt.figure(figsize=(15, 10))
for i, var in enumerate(key_vars):
    plt.subplot(2, 2, i+1)
    sns.boxplot(data=df, x="cluster_kmeans", y=var, palette="viridis")
    plt.title(f"{var.replace('_', ' ').title()} by Cluster")
plt.tight_layout()
plt.savefig(os.path.join(output_dir, "cluster_boxplots.png"))
plt.close()

# Radar Chart Data Generation
cluster_means = df.groupby('cluster_kmeans')[key_vars].mean()
# Normalize for radar chart (0-1)
cluster_means_norm = (cluster_means - cluster_means.min()) / (cluster_means.max() - cluster_means.min())

def make_radar_chart(data, labels, title, filename):
    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    for i, row in data.iterrows():
        values = row.tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=f'Cluster {i}')
        ax.fill(angles, values, alpha=0.1)
    
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    plt.title(title, size=20, y=1.1)
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig(filename)
    plt.close()

make_radar_chart(cluster_means_norm, [v.replace('_', '\n').title() for v in key_vars], 
                 "Cluster Profiles (Normalized)", os.path.join(output_dir, "radar_clusters.png"))

print(f"Visualizations complete. Results saved to {output_dir}/")
