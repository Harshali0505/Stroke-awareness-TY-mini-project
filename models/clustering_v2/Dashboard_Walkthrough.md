# Phase 5: Dashboard Walkthrough

This document showcases the visual findings from the Phase 5 analysis. All charts are located in the [phase5_outputs](file:///c:/Projects/Stroke-awareness-TY-mini-project/clustering_v2/phase5_outputs/) directory.

## 📊 1. Descriptive Distributions
- **Distributions**: See `dist_awareness_score.png`, `dist_lifestyle_risk_score.png`. These plots show the population spread with Mean (Red) and Median (Blue) lines.
- **Correlation**: `scatter_awareness_action.png` demonstrates the positive linear trend between health knowledge and the propensity for immediate action.

## 🧪 2. Hypothesis Visualizations
- **H1 (Awareness vs Action)**: `h1_awareness_action_bar.png` clearly shows that High Awareness groups have a significantly higher percentage of Proactive responses.
- **H2 (Urgency by Risk)**: `h2_urgency_risk_violin.png` visualizes why H2 was not supported—the distribution of urgency scores is almost identical for both high and low-risk groups.
- **H3 (Age vs Awareness)**: `h3_age_awareness_heatmap.png` provides a count-based view of how awareness levels are distributed across the four age tiers.

## 🌀 3. Cluster Profiling
- **Radar Chart**: `radar_clusters.png` is the "fingerprint" of our segmentation. It shows how Cluster 0 peaks in Awareness/Action while Cluster 2 is severely retracted across most dimensions.
- **Comparison**: `cluster_boxplots.png` provides a side-by-side view of the statistical spread for all key variables across the 4 clusters.

## 💡 How to use these results
1. **Cluster 0** should be used as a "Baseline" for successful awareness campaigns.
2. **Cluster 2** needs fundamental literacy education before actionable advice.
3. **Cluster 3** needs behavioral nudges rather than more information, as they already possess high knowledge.
