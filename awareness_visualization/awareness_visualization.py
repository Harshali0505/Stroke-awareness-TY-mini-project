import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
print("🔥 RUNNING LATEST VERSION 🔥")

# === Step 1: Load the scored data ===
df = pd.read_csv("C:/Projects/Stroke-awareness-TY-mini-project/current_work/awareness_scores.csv")

# === Step 2: Categorize awareness levels ===
def categorize_awareness(score):
    if score < 6:
        return "Low Awareness"
    elif 6<= score < 8.5:
        return "Moderate Awareness"
    else:
        return "High Awareness"
def categorize_awareness_specialist(score):
    if score == 0:
        return "Low Awareness"
    elif score in [1, 2]:
        return "Moderate Awareness"
    else:  # score == 4
        return "High Awareness"
def categorize_know_stroke(score):
    if score ==0:
        return "Low Awareness"
    else:
        return "High Awareness"
def categorize_action_first_symptom(score):
    if score ==0:
        return "Low Awareness"
    elif score ==1:
        return "Moderate Awareness"
    else:
        return "High Awareness"
def categorize_symptom_awareness(score):
    if score <=3:
        return "Low Awareness"
    elif 4<=score<5:
        return "Moderate Awareness"
    else:
        return "High Awareness"
def categorize_first_contact(score):
    if score ==0:
        return "Low Awareness"
    elif score == 3:
        return "Moderate Awareness"
    else:  # score == 4
        return "High Awareness"
def categorize_urgency(score):
    if score ==0:
        return "Low Awareness"
    elif score ==1:
        return "Moderate Awareness"
    else:  # score == 2
        return "High Awareness"
def categorize_risk_awareness(score):
    if 0<=score <=3:
        return "Low Awareness"
    elif 3<score <=6:
        return "Moderate Awareness"
    else:
        return "High Awareness"

def categorize_advice(score):
    if score in [0, 1]:
        return "Low Awareness"
    else:  # score == 3
        return "High Awareness"
    
df["awareness_category"] = df["awareness_score"].apply(categorize_awareness)
df["awareness_specialist"] = df["score_specialist"].apply(categorize_awareness_specialist)
df["awareness_know_stroke"] = df["score_know_stroke"].apply(categorize_know_stroke)
df["awareness_action_first_symptom"] = df["score_action_first_symptom"].apply(categorize_action_first_symptom)
df["awareness_symptom_checklist"] = df["score_symptoms"].apply(categorize_symptom_awareness)
df["awareness_first_contact"] = df["score_first_contact"].apply(categorize_first_contact)
df["awareness_urgency"] = df["score_urgency"].apply(categorize_urgency)
df["awareness_location"] = df["score_location"].apply(categorize_first_contact)
df["awareness_risk_factors"] = df["score_risk"].apply(categorize_risk_awareness)
df["awareness_advice"] = df["score_advice"].apply(categorize_advice)

# === Step 4: Horizontal Histogram — Distribution of Awareness Scores ===
plt.figure(figsize=(8, 6))
plt.hist(df["awareness_score"], bins=10, color="skyblue", edgecolor="black", orientation='horizontal')
plt.title("Distribution of Awareness Scores (Out of 10)")
plt.ylabel("Awareness Score")  # Now vertical axis = Score
plt.xlabel("Number of Respondents")  # Horizontal axis = Count
plt.grid(axis="x", linestyle="--", alpha=0.7)
plt.show()

# === Step 5: Pie Chart — Awareness Categories ===

color_map = {
    "Low Awareness": "#ff9999",       # red
    "Moderate Awareness": "#66b3ff",  # blue
    "High Awareness": "#4bbc4b"       # green
}

category_order = ["Low Awareness", "Moderate Awareness", "High Awareness"]
category_counts1 = (
    df["awareness_category"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)

plt.figure(figsize=(7, 7))
plt.pie(
    category_counts1,
    labels=category_counts1.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=[color_map[label] for label in category_counts1.index]
)
plt.title("Awareness Level Distribution")
plt.show()

category_counts2 = (
    df["awareness_specialist"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)

plt.figure(figsize=(7, 7))
plt.pie(
    category_counts2,
    labels=category_counts2.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=[color_map[label] for label in category_counts2.index]
)
plt.title("Awareness Level Distribution - Specialist")
plt.show()

category_counts3 = (
    df["awareness_know_stroke"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)

plt.figure(figsize=(7, 7))
plt.pie(
    category_counts3,
    labels=category_counts3.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=[color_map[label] for label in category_counts3.index]
)
plt.title("Awareness Level Distribution - Know Stroke")
plt.show()

category_counts4 = (
    df["awareness_action_first_symptom"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)

plt.figure(figsize=(7, 7))
plt.pie(
    category_counts4,
    labels=category_counts4.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=[color_map[label] for label in category_counts4.index]
)
plt.title("Awareness Level Distribution - Action First Symptom")
plt.show()

category_counts5 = (
    df["awareness_symptom_checklist"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)
plt.figure(figsize=(7, 7))
plt.pie(
    category_counts5,
    labels=category_counts5.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=[color_map[label] for label in category_counts5.index]
)
plt.title("Awareness Level Distribution - Symptom Checklist")
plt.show()

category_counts6 = (
    df["awareness_first_contact"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)
plt.figure(figsize=(7, 7))
plt.pie(
    category_counts6,
    labels=category_counts6.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=[color_map[label] for label in category_counts6.index]
)
plt.title("Awareness Level Distribution - First Contact")
plt.show()

category_counts7 = (
    df["awareness_urgency"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)
plt.figure(figsize=(7, 7))
plt.pie(
    category_counts7,
    labels=category_counts7.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=[color_map[label] for label in category_counts7.index]
)
plt.title("Awareness Level Distribution - Urgency")
plt.show()

category_counts8 = (
    df["awareness_location"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)
plt.figure(figsize=(7, 7))
plt.pie(
    category_counts8,
    labels=category_counts8.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=[color_map[label] for label in category_counts8.index]
)
plt.title("Awareness Level Distribution - Location")
plt.show()

category_counts9 = (
    df["awareness_risk_factors"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)
plt.figure(figsize=(7, 7))
plt.pie(
    category_counts9,
    labels=category_counts9.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=[color_map[label] for label in category_counts9.index]
)
plt.title("Awareness Level Distribution - Risk Factors")
plt.show()

category_counts10 = (
    df["awareness_advice"]
    .value_counts()
    .reindex(category_order, fill_value=0)
)
plt.figure(figsize=(7, 7))
plt.pie(
    category_counts10,
    labels=category_counts10.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=[color_map[label] for label in category_counts10.index]
)
plt.title("Awareness Level Distribution - Advice")
plt.show()

# === Step 6: Save categorized results ===
df.to_csv("C:/Projects/Stroke-awareness-TY-mini-project/current_work/awareness_scores_with_categories.csv", index=False)
print("✅ Visuals generated and file saved with awareness categories.")
#print(df["score_action_first_symptom"].value_counts())
#print(df["symptom_awareness_score"].value_counts())
#print(df["score_risk"].value_counts())