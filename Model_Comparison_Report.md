# Clustering Model Comparison Report

This report evaluates five different clustering algorithms applied to the stroke awareness dataset ($N=6168$). The goal is to identify the most statistically robust model for defining behavioral personas.

## Comparison Metrics

The following metrics were used to evaluate the clusters:
- **Silhouette Score**: Measures cluster cohesion and separation. (Range: -1 to 1; Higher is better).
- **Davies-Bouldin Index**: Measures the average 'similarity' between clusters. (Lower is better).
- **Calinski-Harabasz Index**: The ratio of the sum of between-clusters scatter and within-cluster scatter. (Higher is better).

### Quantitative Results

| Model | Silhouette Score | Davies-Bouldin Index | Calinski-Harabasz | Clusters Found |
| :--- | :--- | :--- | :--- | :--- |
| **K-Means** | **0.2323** | 1.5586 | **2007.39** | 4 |
| **GMM** | 0.1708 | 1.6324 | 1334.48 | 4 |
| **Hierarchical** | 0.2121 | 2.2438 | 1437.48 | 4 |
| **Spectral** | 0.1573 | **1.4431** | 1247.12 | 4 |
| **DBSCAN** | 0.1618 | 1.4607 | 625.12 | 3* |

*\*DBSCAN results exclude noise points. 1.2% of the population was identified as noise.*

## Model Analysis

### 1. K-Means (Winner)
K-Means produced the highest **Silhouette Score** and **Calinski-Harabasz Index**, indicating that its clusters are the most compact and well-separated. It effectively captured the four primary personas (Knowledgeable/Healthy, Uninformed/Willing, High-Risk/Passive, Knowledgeable/Risky) with clear boundaries.

### 2. Spectral Clustering
While Spectral Clustering achieved the best (lowest) **Davies-Bouldin Index**, its Silhouette score was significantly lower than K-Means. This suggests that while it creates very distinct "centers," the density within those clusters is less consistent across the entire feature space.

### 3. Hierarchical (Agglomerative)
Hierarchical clustering performed reasonably well on the Silhouette score (0.212) but suffered from a very high Davies-Bouldin Index (2.24). This often happens when clusters have varying shapes or densities, leading to overlap in some areas of the feature space.

### 4. GMM (Expectation-Maximization)
GMM provided a probabilistic approach. While useful for understanding "fuzzy" boundaries between personas, it did not achieve the same level of structural separation as K-Means or Hierarchical clustering in this specific manifold.

### 5. DBSCAN
DBSCAN was useful for identifying outliers (noise), but it struggled to differentiate between the major personas due to the high-density nature of the survey data. It collapsed multiple theoretical personas into fewer, larger clusters.

## Recommendation

Based on the quantitative metrics and the need for clear, actionable behavioral segments:

**K-Means with $k=4$ is the recommended model.**

It provides:
- The highest mathematical separation between groups.
- A balanced distribution of respondents across segments.
- High interpretability for public health intervention planning.

---
*Analysis generated on 2026-04-16*
