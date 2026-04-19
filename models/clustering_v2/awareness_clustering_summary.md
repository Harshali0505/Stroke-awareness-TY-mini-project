# Research Methodology: Decoding Stroke Awareness Patterns

This document provides a comprehensive technical and conceptual summary of the clustering analysis performed to understand stroke awareness and health behaviors.

---

## 🏗️ 1. Infrastructure & Data Foundations (Phase 1)
**What we did:**
We started by refining the raw data. We handled physical inactivity, smoking, alcohol, and BMI variables, applying a standard Z-score normalization to ensure no single variable overwhelmed the others.
**Why we did it:**
Algorithms are sensitive to scale and outliers. By cleaning BMI "entry errors" and standardizing scores, we ensured the clustering was based on actual behavioral patterns rather than data noise.
**Output:** A high-quality "behavioral baseline" dataset.
**Translation:** We "leveled the playing field" for all data points so we could see the real story behind people's habits.

## 🤖 2. The Multi-Model Experiment (Phase 2)
**What we did:**
We didn't just use one algorithm. We ran **K-Means, Hierarchical, GMM, Spectral, and DBSCAN**.
**Why we did it:**
Triangulation starts here. If a pattern only appears in one algorithm, it’s probably a fluke. If it appears in all of them, it’s a scientific fact.
**Output:** A consistent **4-cluster structure** emerged across all major models.
**Translation:** We double, triple, and quadruple-checked our work using different "lenses" to make sure the groups we found were real.

## 📏 3. Statistical Rigor (Phase 3)
**What we did:**
We ran ANOVA (Analysis of Variance) and Cross-Tabulations.
**Why we did it:**
To prove that the groups were actually different in a way that matters. We checked if the "High Awareness" group actually had statistically higher scores than the "Low Awareness" group.
**Output:** **p-values < 0.001** (Highly Significant).
**Translation:** The chances of these groups being accidental are less than 0.1%. They are mathematically distinct.

## 🔍 4. The Hypothesis Bridge (Phase 4)
**What we did:**
We bridged the gap between raw statistics and our four core research hypotheses (H1-H4).
**Why we did it:**
To see if the "story" we planned met the "reality" of the data. This is where we identified the **Cognitive Paradox** (people who know the symptoms but still hesitate to act).
**Output:** Strong validation of the "Awareness-Action Gap."
**Translation:** We found that knowledge doesn't always equal action, helping us find the exact people who need more than just a brochure—they need a nudge.

## 📈 5. The Insight Engine (Phase 5)
**What we did:**
Calculated **Odds Ratios** (e.g., High awareness = 2x more likely to act) and built a visual dashboard with **Radar Charts**.
**Why we did it:**
To make the data "speak." We moved from abstract clusters to actionable archetypes.
**Output:** Final results including a 1.99x likelihood ratio for proactive behavior.
**Translation:** We turned numbers into a strategy. We know who to talk to, what they think, and exactly how much knowledge influences their speed of response.
