# Stroke Awareness Analysis & Clustering Project

This project aims to analyze stroke awareness, lifestyle risks, and demographic factors using a data-driven approach. It involves comprehensive data cleaning, exploratory data analysis (EDA), and advanced population segmentation using multiple clustering algorithms.

## 📁 Project Structure

The project is modularized based on functionality to maintain a clean root directory:

- **`core_data/`**: Centralized repository for shared datasets (CSV/Excel) and metadata.
- **`awareness_scoring/`**: Scripts and notebooks for data cleaning and awareness scoring logic.
- **`awareness_visualization/`**: Visual insights, plots, and exploratory analysis notebooks.
- **`models/`**: Major development sub-projects.
  - `clustering_v2/`: Comprehensive population segmentation analysis.
  - `stroke-disease-prediction/`: Predictive modeling for stroke risk.
- **`dashboard/`**: React/Vite-based user interface for displaying insights.
- **`docs/`**: Documentation, reports, and attribute definitions.
- **`utils/`**: Helper scripts, debug tools, and temporary trials.
- **`current_work/`**: Active working directory for ongoing tasks.

## 🚀 Key Features & Workflow

### 1. Data Preprocessing & Variable Definition
- **Cleaning**: Handling missing values and capping BMI outliers.
- **Standardization**: Z-score normalization for lifestyle variables (Smoking, Alcohol, Inactivity, BMI).
- **Composite Scoring**: Creating a `lifestyle_risk_score` and validating internal consistency using Cronbach's Alpha.
- **Categorization**: Median split branding for Awareness and Risk levels.

### 2. Exploratory Data Analysis (EDA)
- Visualization of demographic distributions.
- Correlation analysis between awareness, lifestyle, and medical risk factors.

### 3. Advanced Clustering Analysis
The project utilizes multiple algorithms to segment the population:
- **K-Means**: Baseline partitioning.
- **Hierarchical Clustering**: Understanding nested group structures.
- **DBSCAN**: Density-based clustering to find non-linear segments.
- **GMM (Gaussian Mixture Models)**: Probabilistic clustering.
- **Spectral Clustering**: For complex manifold structures.

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone [repository-url]
   ```
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 📊 Project Progress

The project has successfully moved through several critical phases:

- **Phase 1 (Variable Definition & Preprocessing)**: ✅ **Complete**. Datasets standardized, BMI outliers handled, and composite lifestyle risk scores generated.
- **Phase 2 (Clustering Implementation)**: ✅ **Complete**. Successfully executed 5 major algorithms (K-Means, DBSCAN, GMM, Hierarchical, Spectral) to segment the population.
- **Phase 3 (Statistical Validation & Diagnostics)**: ✅ **Complete**. Clusters validated using ANOVA and Crosstabs to ensure significant between-group differences.
- **Phase 4 (Result Triangulation & Comparison)**: ✅ **Complete**. Compared findings across different methods to ensure findings were robust and consistent.
- **Phase 5 (Dashboard & Final Reporting)**: ✅ **Complete**. Integrated clusters into an interactive React dashboard and generated comprehensive summary reports.

## 🧪 Technologies Used
- **Python 3.x**
- **Pandas & NumPy**: Data manipulation.
- **Scikit-learn**: Machine learning and clustering algorithms.
- **Matplotlib & Seaborn**: Data visualization.
- **Openpyxl**: Excel file handling.
