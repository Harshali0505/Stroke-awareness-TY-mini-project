# Phase 5: Results Report - Stroke Awareness Clustering Analysis

## 1. Descriptive Statistics
The study population ($N=6168$) shows a diverse range of health awareness and risk behaviors.

| Variable | Mean | Std Dev | Skewness | Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **Awareness Score** | 4.64 | 2.53 | -0.21 | Slightly left-skewed, indicating many respondents have moderate-to-high awareness. |
| **Lifestyle Risk Score** | 0.00 | 0.52 | 0.45 | Scaled score; positive values indicate higher-than-average risk. |
| **Action Score** | 1.34 | 0.69 | -0.56 | Majority prefer proactive action (Score > 1). |
| **Urgency Score** | 1.03 | 1.00 | -0.07 | Balanced perception of medical urgency. |

## 2. Hypothesis Testing Results

### **H1: Awareness → Action**
- **Chi-Square p-value**: < 0.001
- **Logistic Regression**: Odds Ratio (OR) = **1.99** (95% CI: 1.80 - 2.20)
- **Interpretation**: **Strongly Supported**. Individuals with "High Awareness" are **1.99 times more likely** to take proactive action compared to those with "Low Awareness".

### **H2: Lifestyle Risk → Urgency**
- **t-test p-value**: 0.94
- **Interpretation**: **Not Supported**. Lifestyle risk level did not significantly impact the perception of medical urgency in this dataset.

### **H3: Age Group → Awareness**
- **Chi-Square p-value**: < 0.001
- **Interpretation**: **Strongly Supported**. Significant variations in awareness levels exist across different age groups, with older segments showing more cautious behavioral structuring.

### **H4: Clustering Validity**
- **ANOVA Results**: p < 0.001 for all key variables (Awareness, Risk, Action, Urgency).
- **F-Statistics**: Extremely high for Urgency (15,371) and Awareness (5,794).
- **Interpretation**: **Strongly Supported**. The 4-cluster model represents statistically distinct behavioral segments.

## 3. Cluster Interpretation & Archetypes

| Cluster | Archetype | Key Characteristics |
| :--- | :--- | :--- |
| **0** | **Knowledgeable & Healthy** | High Awareness (83.5%), Low Risk (72.7%), Proactive. |
| **1** | **Willing but Uninformed** | Low Awareness (69.6%), Proactive Action (61.8%). |
| **2** | **High-Risk & Passive** | 100% Low Awareness, 86.7% Passive Action. |
| **3** | **Knowledgeable but Risky** | High Awareness (86.4%), High Lifestyle Risk (66.3%). |

## 4. Conclusion
The analysis confirms that stroke awareness is the primary driver of proactive health behavior. While age and risk also play roles, the "Awareness-Action Gap" (Cluster 3) and the "Uninformed but Proactive" (Cluster 1) groups represent the most critical targets for intervention.
