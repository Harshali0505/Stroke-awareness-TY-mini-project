# 🖼️ Diagrams & Variables Description

This document provides a comprehensive guide to all visual outputs generated during the Stroke Awareness Clustering Project. It explains what each chart represents, the variables involved, and how to interpret them.

---

## 🏗️ 1. Infrastructure & Diagnostics (Clustering V2)

### 📈 Correlation Heatmap
**File**: `correlation_heatmap.png`
- **What it is**: A matrix showing how variables relate to one another.
- **Variables**: `awareness_score`, `lifestyle_risk_score`, `score_urgency`, `score_action_first_symptom`.
- **Interpreting**: 1.0 (Dark Blue) means perfect correlation. We use this to see if two variables are basically the same thing (redundant) or if they influence each other.

### 📉 K-Means Elbow Plot
**File**: `kmeans_elbow.png`
- **What it is**: A technical tool used to find the "sweet spot" for how many groups (clusters) we should create.
- **Variables**: Number of Clusters (k) vs. Inertia (Variance).
- **Interpreting**: The "elbow" (where the line bends steeply) tells us that **4 clusters** is the most efficient division of our data.

### 🌌 PCA Factor Explanation: What are PCA1 and PCA2?
Since we can't visualize 6 dimensions at once (Awareness, Risk, Action, Urgency, etc.), we use Principal Component Analysis (PCA) to "squash" them into two main axes:
- **PCA1 (Primary Trend)**: This usually captures the broad contrast between people who are highly engaged (high knowledge/action) vs. those who are disengaged.
- **PCA2 (Secondary Trend)**: This usually captures differences in lifestyle risk or age patterns within those engagement groups.

### 🖼️ The PCA Algorithm Gallery
Every algorithm "sees" the same data but groups it using a different logic.

#### **K-Means Clustering**
- **File**: `kmeans_pca.png`
- **What it is**: The "Primary Map." It uses hard boundaries to divide people into the most statistically distinct groups.
- **Variables**: PCA1 (Engagement/Awareness) and PCA2 (Lifestyle Risk).
- **Interpretation**: Shows 4 crisp color zones. Best for seeing the absolute "Archetypes" of our population.

#### **Hierarchical Clustering**
- **File**: `hierarchical_pca.png`
- **What it is**: A "Family Tree" projection.
- **Variables**: PCA1 and PCA2.
- **Interpretation**: Shows how clusters are related to each other. You can see which groups "branched off" from common behaviors.

#### **DBSCAN (Density-Based)**
- **File**: `dbscan_pca.png`
- **What it is**: A "Crowd-Based" map that identifies dense clusters and isolated individuals.
- **Variables**: PCA1 and PCA2.
- **Interpretation**: Great for finding the "Average Person" (dense areas) and finding **Outliers** (isolated dots) who don't fit any common pattern.

#### **GMM (Gaussian Mixture)**
- **File**: `gmm_pca.png`
- **What it is**: The "Natural/Cloud" view.
- **Variables**: PCA1 and PCA2.
- **Interpretation**: Shows overlapping ovals. Highly realistic as it shows how people's habits "bleed" from one group into another rather than being in perfect boxes.

#### **Spectral Clustering**
- **File**: `spectral_pca.png`
- **What it is**: A "Graph-Based" map that identifies clusters based on connectivity.
- **Variables**: PCA1 and PCA2.
- **Interpretation**: Reveals complex, non-linear relationships that simple geometry might miss.

---

## 📊 2. Results Dashboard (Phase 5 Outputs)

### 🌀 Cluster Profiles (Radar Chart)
**File**: `phase5_outputs/radar_clusters.png`
- **What it is**: The "fingerprint" of each cluster.
- **Variables**: `Awareness Score`, `Lifestyle Risk`, `Action Score`, `Urgency Perception`.
- **Interpreting**: A wider shape means that group scores "High" on those variables. For example, Cluster 0 marks high on Awareness and Action, forming a large "kite" shape.

### 📦 Key Variable Boxplots
**File**: `phase5_outputs/cluster_boxplots.png`
- **What it is**: A side-by-side comparison of the core metrics across all 4 groups.
- **Variables**: `awareness_score`, `lifestyle_risk_score`, `score_urgency`, `score_action_first_symptom`.
- **Interpreting**: The box shows where the middle 50% of people fall. The lines (whiskers) show the spread. This proves that each cluster is statistically unique.

### 🌡️ Awareness vs Action (Scatter & Bar)
**Files**: `phase5_outputs/scatter_awareness_action.png`, `phase5_outputs/h1_awareness_action_bar.png`
- **Variables**: `awareness_score` (Input) vs. `action_score` (Output).
- **Interpreting**: The scatter plot shows the trend line—as knowledge goes up, speed of action tends to follow. The bar chart proves that "High Awareness" groups have nearly double the "Proactive" responses.

### 🎻 Urgency by Risk (Violin Plot)
**File**: `phase5_outputs/h2_urgency_risk_violin.png`
- **Variables**: `lifestyle_risk_cat` vs. `score_urgency`.
- **Interpreting**: The "thickness" of the violin shows where most people fall. Our results showed that both High and Low-Risk groups have similar "bulges," meaning risk doesn't change how urgent they think a stroke is.

### 🗺️ Age vs Awareness (Heatmap)
**File**: `phase5_outputs/h3_age_awareness_heatmap.png`
- **Variables**: `age_group_4cat` vs. `awareness_cat`.
- **Interpreting**: Darker colors show higher concentrations of people. This helps identify which age groups have the most "Low Awareness" individuals.

---

## 📝 Variable Definitions

| Variable Name | Simple Explanation | Value Range |
| :--- | :--- | :--- |
| **Awareness Score** | How much you know about stroke symptoms and prevention. | 0 (Low) to 10 (High) |
| **Lifestyle Risk Score** | Your risk based on smoking, alcohol, BMI, and activity. | Lower is Better |
| **Action Score** | How fast you would call the doctor if symptoms appeared. | 0 (Passive) to 2 (Proactive) |
| **Urgency Perception** | How dangerous you believe stroke symptoms are. | 0 (Low) to 2 (High) |
| **PCA1/PCA2** | "Summary" variables that combine all the above for plotting. | N/A |

---

## ❓ Follow-up Questions & Answers

**Q: What exactly is a "PCA Factor"?**
**A:** Think of it like a "Projected Shadow." If you shine a light on a 3D object from two different angles, you get two different 2D shadows. PCA1 is the shadow from the most informative angle (Health Knowledge), and PCA2 is the shadow from the next most informative angle (Lifestyle Habits). We use them because they let us plot all 6 of our research variables on a single X-Y graph without losing the core information.

**Q: Why do different algorithms show the same data differently in PCA?**
**A:** Because each algorithm has a different "Logic of Belonging." K-Means thinks you belong to the group whose *average* you are closest to. DBSCAN thinks you belong to the group where the *crowd* is thickest. GMM thinks you belong to the *cloud* you are most likely a part of. By looking at all of them, we confirm that our 4 segments (Baseline, Willing, Paradox, High-Risk) exist regardless of which logic you use.
