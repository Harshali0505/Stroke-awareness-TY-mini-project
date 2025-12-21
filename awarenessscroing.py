import pandas as pd

df = pd.read_excel("C:/Projects/stroke_ml_project/cleaned_datasheet_2.xlsx")

# ========= Basic Scoring Functions ========= #

def score_yes_no(value):
    if isinstance(value, str):
        v = value.strip().lower()
        if v in ["yes", "y", "true"]:
            return 1
        elif v in ["no", "n", "false"]:
            return 0
    return 0

def score_specialist(value):
    if isinstance(value, str):
        v = value.lower()
        if "neuro" in v:
            return 4
        elif "physician" in v:
            return 2
        elif "doctor" in v:
            return 1
    return 0

def score_action(value):
    if isinstance(value, str):
        v = value.lower()
        if any(x in v for x in ["immediately", "within 1 hour", "asap"]):
            return 2
        elif any(y in v for y in ["within a day", "within 24 hours", "within a few hours"]):
            return 1
    return 0

def score_location(value):
    if isinstance(value, str):
        v = value.lower()
        if "emergency" in v:
            return 4
        elif any(x in v for x in ["hospital", "neurology"]):
            return 3
    return 0

def score_misconception(value):
    if isinstance(value, str):
        v = value.lower()
        if v == "no":
            return 2
        elif v in ["maybe", "not sure"]:
            return 1
        else:
            return 0
    return 0

# ======= New scoring functions for new columns ======= #

def score_symptom_checklist(value):
    # correct symptoms: confusion, numbness, vision trouble
    correct = ["confusion", "numbness", "weakness", "vision", "seeing"]
    
    if not isinstance(value, str):
        return 0

    v = value.lower()
    count = sum(1 for c in correct if c in v)
    return min(count, 3)  # max 3 points

def score_risk_factors(value):
    if not isinstance(value, str):
        return 0
    v = value.lower()
    risk_categories = {
        "blood_pressure": ["blood_pressure", "heart_problem", "hypertension"],
        "diabetes": ["diabetes", "obesity"],
        "smoking": ["smoking", "alcohol", "drugs"],
        "age_family": ["age", "family_history"]
    }
    score = 0
    for keywords in risk_categories.values():
        if any(k in v for k in keywords):
            score += 1
    return score  # max = 4


def score_advice(value):
    if not isinstance(value, str):
        return 0
    v = value.lower()
    if "hospital" in v or "emergency" in v or "ambulance" in v:
        return 3
    elif "doctor" in v:
        return 1
    return 0

# ===== Applying Scores ===== #

df["score_specialist"] = df.iloc[:,0].apply(score_specialist)
df["score_know_stroke"] = df.iloc[:,1].apply(score_yes_no)
df["score_action_first_symptom"] = df.iloc[:,2].apply(score_action)
df["score_confusion"] = df.iloc[:,3].apply(score_yes_no)
df["score_numbness"] = df.iloc[:,4].apply(score_yes_no)
df["score_nosebleed"] = df.iloc[:,5].apply(score_misconception)
df["score_vision"] = df.iloc[:,6].apply(score_yes_no)
df["score_first_contact"] = df.iloc[:,11].apply(score_location)
df["score_urgency"] = df.iloc[:,12].apply(score_action)
df["score_location"] = df.iloc[:,13].apply(score_location)
df["score_symptoms"] = df["stroke_symptoms"].apply(score_symptom_checklist)
df["score_risk"] = df["risk_factors"].apply(score_risk_factors)
df["score_advice"] = df["what_advice_would_you_give_for_someone_experiencing_stroke_symptoms"].apply(score_advice)
# ===== Weights ===== #

weights = {
    "score_specialist": 3,
    "score_know_stroke": 5,
    "score_action_first_symptom": 3,
    "score_confusion": 5,
    "score_numbness": 5,
    "score_vision": 2,
    "score_nosebleed": 2,
    "score_first_contact": 5,
    "score_urgency": 5,
    "score_location": 5,
    "score_symptoms": 3,
    "score_risk": 3,
    "score_advice": 2
}
weights_symptom = {
    "score_confusion": 5,
    "score_numbness": 5,
    "score_vision": 2,
    "score_nosebleed": 2,
    "score_symptoms": 3
}
df["score_symptoms_combined"] = sum(df[col] * w for col, w in weights_symptom.items())
df["total_raw_score"] = sum(df[col] * w for col, w in weights.items())

max_values = {
    "score_specialist": 4,
    "score_know_stroke": 1,
    "score_action_first_symptom": 2,
    "score_confusion": 1,
    "score_numbness": 1,
    "score_vision": 1,
    "score_nosebleed": 2,
    "score_first_contact": 4,
    "score_urgency": 2,
    "score_location": 4,
    "score_symptoms": 3,
    "score_risk": 4,
    "score_advice": 3
}

max_symptom_score = sum(weights_symptom[col] * max_values[col] for col in weights_symptom)
max_score = sum(weights[col] * max_values[col] for col in weights)

df["symptom_awareness_score"] = (df["score_symptoms_combined"] / max_symptom_score * 10).clip(0, 10).round(2)
df["awareness_score"] = (df["total_raw_score"] / max_score * 10).clip(0, 10).round(2)

print(df[["awareness_score"]].head())
print(f"Min Score: {df['awareness_score'].min()}")
print(f"Max Score: {df['awareness_score'].max()}")
print(df[["symptom_awareness_score"]].head())
print(f"Min Symptom Score: {df['symptom_awareness_score'].min()}")
print(f"Max Symptom Score: {df['symptom_awareness_score'].max()}")
# === Step 5: Save output ===
output_path = "C:/Projects/stroke_ml_project/awareness_scores.csv"
df.to_csv(output_path, index=False)
print(f"✅ Awareness scores calculated and saved to {output_path}")
print(df["risk_factors"].value_counts())
print(df["if_you_experience_symptoms_of_warning_signs,_which_specialist_would_you_consult?"].value_counts())