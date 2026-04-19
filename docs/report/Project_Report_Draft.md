# Project Report: Stroke Awareness Analysis & Population Clustering

## Abstract
This project presents a data-driven approach to understanding stroke awareness, lifestyle risks, and medical urgency perception. By leveraging multiple clustering algorithms and statistical validation techniques, we identified four distinct population segments. The findings reveal a significant "Awareness-Action Gap" and provide actionable insights for targeted public health interventions.

---

## Chapter 1: Introduction

### 1.1 Background
Stroke remains a leading cause of disability and mortality worldwide. Early detection of symptoms and immediate medical response are critical for improving patient outcomes. However, public awareness of stroke symptoms and the necessity of rapid action varies significantly across different demographics.

### 1.2 Motivation
Traditional public health outreach often uses a "one-size-fits-all" approach. This project is motivated by the need for a more nuanced understanding of how different groups perceive stroke risk and how their knowledge translates into behavior.

### 1.3 Objectives
- To quantify stroke awareness and lifestyle risk using composite scoring.
- To segment the population into behavioral archetypes using advanced clustering.
- To validate research hypotheses regarding the relationship between awareness, age, and proactive health behavior.
- To provide an interactive dashboard for visualizing population insights.

---

## Chapter 2: Literature Survey

### 2.1 Stroke Awareness Studies
Existing research highlights that while many individuals can identify at least one stroke symptom, fewer are aware of the full range of symptoms or the importance of the "Golden Hour" for treatment.

### 2.2 Machine Learning in Public Health
Clustering algorithms have been increasingly used to identify health-risk patterns in large datasets. K-Means and Hierarchical clustering are common benchmarks, while density-based methods like DBSCAN help identify non-linear structures and outliers.

---

## Chapter 3: Proposed System

### 3.1 Data Preprocessing
The system begins with a robust cleaning pipeline:
- **Outlier Handling**: BMI values were capped to remove entry errors.
- **Normalization**: Z-score normalization was applied to lifestyle variables (Smoking, Alcohol, Inactivity) to ensure uniform weighting in clustering.

### 3.2 Scoring Methodology
Four key composite scores were developed:
1. **Awareness Score**: Sum of correctly identified symptoms and prevention methods.
2. **Lifestyle Risk Score**: A standardized aggregate of behavioral risk factors.
3. **Action Score**: Quantifying the speed and type of response to first symptoms.
4. **Urgency Score**: Measuring the perceived danger of stroke symptoms.

### 3.3 System Architecture
The pipeline consists of three main stages:
1. **Preprocessing & Scoring Engine** (Python/Pandas).
2. **Clustering & Validation Module** (Scikit-learn/SciPy).
3. **Visualization Dashboard** (React/Vite).

---

## Chapter 4: Design

### 4.1 Algorithm Selection
To ensure robust segmentation, five clustering algorithms were implemented and compared:
- **K-Means**: For partitioning-based grouping.
- **Hierarchical Clustering**: To understand the nested structure of health behaviors.
- **DBSCAN**: To identify dense "typical" groups and isolated "outlier" individuals.
- **Gaussian Mixture Models (GMM)**: For probabilistic, overlapping clusters.
- **Spectral Clustering**: For capturing complex connectivity patterns.

### 4.2 Visualization Design
- **PCA (Principal Component Analysis)**: Used to reduce high-dimensional behavioral data into 2D maps for visual inspection of cluster separation.
- **Radar Charts**: Employed to visualize the "archetype" of each cluster across multiple dimensions.

---

## Chapter 5: Result and Discussion

### 5.1 The 4-Cluster Solution
The analysis revealed four stable population archetypes ($N=6168$):

| Cluster | Archetype | Description |
| :--- | :--- | :--- |
| **0** | **Knowledgeable & Healthy** | High awareness, low lifestyle risk, and highly proactive. |
| **1** | **Willing but Uninformed** | Low awareness but still tends toward proactive action. |
| **2** | **High-Risk & Passive** | Lowest awareness and highest passivity in medical response. |
| **3** | **Knowledgeable but Risky** | High awareness but maintains high lifestyle risks (The "Paradox" group). |

### 5.2 Hypothesis Validation
- **H1 (Awareness → Action)**: Supported ($p < 0.001$, $OR = 1.99$). High awareness makes individuals nearly twice as likely to act proactively.
- **H2 (Risk → Urgency)**: Not Supported ($p = 0.94$). Lifestyle risk does not significantly change urgency perception.
- **H3 (Age → Awareness)**: Supported ($p < 0.001$). Older age groups show different behavioral structures compared to younger cohorts.
- **H4 (Clustering Validity)**: Supported. ANOVA results confirmed significant differences across all clusters for all key metrics.

---

## Chapter 6: Conclusion

### 6.1 Summary of Findings
The project successfully demonstrated that stroke awareness is the strongest predictor of proactive medical behavior. However, the discovery of the "Knowledgeable but Risky" group suggests that education alone is insufficient for individuals with established high-risk lifestyles.

### 6.2 Future Work
- Integration of real-time health sensor data.
- Expansion of the dashboard to include personalized risk assessments.
- Longitudinal study to track the impact of targeted awareness campaigns on these specific clusters.
