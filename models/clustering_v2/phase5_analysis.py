import pandas as pd
import numpy as np
from scipy import stats
import statsmodels.api as sm
import json
import os

# Paths
results_dir = r"c:\Projects\Stroke-awareness-TY-mini-project\clustering_v2"
input_file = os.path.join(results_dir, "kmeans_results.csv")
output_dir = os.path.join(results_dir, "phase5_outputs")
os.makedirs(output_dir, exist_ok=True)

# Load data
df = pd.read_csv(input_file)
print("DF DTYPES:\n", df.dtypes)

# --- Step 1: Descriptive Statistics ---
desc_vars = ["awareness_score", "lifestyle_risk_score", "score_action_first_symptom", "score_urgency", "age"]
for v in desc_vars:
    df[v] = pd.to_numeric(df[v], errors='coerce')
print("CLEANED DTYPES:\n", df[desc_vars].dtypes)
desc_stats = df[desc_vars].describe().to_dict()

# Add Skewness
for var in desc_vars:
    desc_stats[var]['skew'] = df[var].skew()

# Basic correlations
correlations = df[desc_vars].corr().to_dict()

# --- Step 2: Hypothesis Testing ---

# H1: Awareness -> Action
# Categorical: awareness_cat vs action_cat (Chi-square)
contingency_h1 = pd.crosstab(df['awareness_cat'], df['action_cat'])
chi2_h1, p_chi2_h1, _, _ = stats.chi2_contingency(contingency_h1)

# Logistic Regression: action_cat (Proactive=1, Passive=0)
df['action_binary'] = df['action_cat'].map({'Proactive': 1, 'Passive': 0})
df['awareness_binary'] = df['awareness_cat'].map({'High Awareness': 1, 'Low Awareness': 0})

# Drop NaNs for regression
reg_df = df[['action_binary', 'awareness_binary']].dropna()
if not reg_df.empty and reg_df['awareness_binary'].nunique() > 1:
    X_h1 = sm.add_constant(reg_df['awareness_binary'].astype(float))
    model_h1 = sm.Logit(reg_df['action_binary'].astype(float), X_h1).fit()
    
    # Safely get odds ratio and CI for the coefficient (not the constant)
    coef_name = 'awareness_binary' if 'awareness_binary' in model_h1.params else model_h1.params.index[1]
    or_h1 = float(np.exp(model_h1.params[coef_name]))
    conf_h1 = np.exp(model_h1.conf_int().loc[coef_name]).tolist()
    p_logit_h1 = float(model_h1.pvalues[coef_name])
else:
    or_h1, conf_h1, p_logit_h1 = None, [None, None], None

# H2: Lifestyle Risk -> Urgency
# Categorical link
contingency_h2 = pd.crosstab(df['lifestyle_risk_cat'], df['action_cat']) 
chi2_h2, p_chi2_h2, _, _ = stats.chi2_contingency(contingency_h2)

# t-test for urgency scores between risk groups
high_risk_urgency = df[df['lifestyle_risk_cat'] == 'High Risk']['score_urgency'].dropna()
low_risk_urgency = df[df['lifestyle_risk_cat'] == 'Low Risk']['score_urgency'].dropna()
t_stat_h2, p_t_h2 = stats.ttest_ind(high_risk_urgency, low_risk_urgency)

# H3: Age Group -> Awareness
contingency_h3 = pd.crosstab(df['age_group_4cat'], df['awareness_cat'])
chi2_h3, p_chi2_h3, _, _ = stats.chi2_contingency(contingency_h3)

# H4: Clustering Validity
anova_results = {}
for var in desc_vars:
    # Ensure numeric and drop NaNs
    df[var] = pd.to_numeric(df[var], errors='coerce')
    clean_df = df.dropna(subset=[var, 'cluster_kmeans'])
    groups = [clean_df[clean_df['cluster_kmeans'] == i][var] for i in clean_df['cluster_kmeans'].unique()]
    if len(groups) > 1:
        f_stat, p_val = stats.f_oneway(*groups)
        anova_results[var] = {"f_stat": float(f_stat), "p_value": float(p_val)}

# Save findings
findings = {
    "descriptive_stats": desc_stats,
    "correlations": correlations,
    "hypothesis_tests": {
        "H1": {
            "chi2_p": float(p_chi2_h1),
            "odds_ratio": or_h1,
            "ci_lower": conf_h1[0],
            "ci_upper": conf_h1[1],
            "p_logit": p_logit_h1
        },
        "H2": {
            "chi2_p": p_chi2_h2,
            "t_test_p": p_t_h2,
            "t_stat": t_stat_h2
        },
        "H3": {
            "chi2_p": p_chi2_h3
        },
        "H4": anova_results
    }
}

with open(os.path.join(output_dir, "stats_summary.json"), "w") as f:
    json.dump(findings, f, indent=4)

print(f"Analysis complete. Results saved to {output_dir}/stats_summary.json")
