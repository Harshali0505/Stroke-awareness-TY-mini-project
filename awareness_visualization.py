import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# === Step 1: Load the scored data ===
df = pd.read_csv("C:/Projects/stroke_ml_project/awareness_scores.csv")

# === Step 2: Categorize awareness levels ===
def categorize_awareness(score):
    if score < 3:
        return "Low Awareness"
    elif 3< score < 7:
        return "Moderate Awareness"
    else:
        return "High Awareness"

df["awareness_category"] = df["awareness_score"].apply(categorize_awareness)

# === Step 4: Horizontal Histogram — Distribution of Awareness Scores ===
plt.figure(figsize=(8, 6))
plt.hist(df["awareness_score"], bins=10, color="skyblue", edgecolor="black", orientation='horizontal')
plt.title("Distribution of Awareness Scores (Out of 10)")
plt.ylabel("Awareness Score")  # Now vertical axis = Score
plt.xlabel("Number of Respondents")  # Horizontal axis = Count
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()


# === Step 5: Pie Chart — Awareness Categories ===
category_counts = df["awareness_category"].value_counts()

plt.figure(figsize=(7, 7))
plt.pie(category_counts, labels=category_counts.index,
        autopct='%1.1f%%', startangle=90, colors=["#ff9999","#66b3ff","#063c06"])
plt.title("Awareness Level Distribution")
plt.show()

# === Step 6: Save categorized results ===
df.to_csv("C:/Projects/stroke_ml_project/awareness_scores_with_categories.csv", index=False)
print("✅ Visuals generated and file saved with awareness categories.")