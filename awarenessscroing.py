import pandas as pd
import numpy as np

# === Step 1: Load the dataset ===
file_path = "C:/Projects/stroke_ml_project/cleaned_awareness_datasheet.csv"
df = pd.read_csv(file_path, encoding='utf-8')

# === Step 2: Define scoring rules ===

def score_yes_no(value):
    if isinstance(value, str):
        value = value.strip().lower()
        if value in ['yes', 'y', 'true']:
            return 1
        elif value in ['no', 'n', 'false']:
            return 0
    return 0  # skipped or invalid → 0

def score_specialist(value):
    if isinstance(value, str):
        val = value.strip().lower()
        if 'neuro' in val:
            return 4
        elif any(x in val for x in ['general physician', 'cardiologist', 'ent']):
            return 2
        elif 'doctor' in val:
            return 1
    return 0  # skipped → 0

def score_action(value):
    if isinstance(value, str):
        val = value.strip().lower()
        if any(x in val for x in ['immediately', 'within 1 hour', 'as soon as possible']):
            return 2
        elif 'within a few hours' in val:
            return 1
    return 0  # skipped → 0

def score_location(value):
    if isinstance(value, str):
        val = value.strip().lower()
        if 'emergency room' in val:
            return 4
        elif any(x in val for x in ['hospital', 'neurology department']):
            return 3
    return 0  # skipped → 0

def score_misconception(value):
    # Correct: "No" → 2; "Maybe"/"Not sure" → 1; "Yes"/wrong → 0
    if isinstance(value, str):
        val = value.strip().lower()
        if val == 'no':
            return 2
        elif val in ['maybe', 'not sure']:
            return 1
        else:
            return 0
    return 0  # skipped → 0

# === Step 3: Apply scoring to relevant columns ===
df["score_specialist"] = df["if_you_experience_symptoms_of_warning_signs,_which_specialist_would_you_consult?"].apply(score_specialist)
df["score_know_stroke"] = df["do_you_know_what_is_a_brain_stroke?"].apply(score_yes_no)
df["score_confusion"] = df["do_you_think_sudden_confusion_,trouble_speaking_or_understanding_speech_is_a_stroke_symptom?"].apply(score_yes_no)
df["score_numbness"] = df["do_you_think_sudden_numbness_or_weakness_of_face,_arm_or_leg_is_a_symptom_of_stroke?"].apply(score_yes_no)
df["score_vision"] = df["do_you_think_trouble_seeing_in_one_or_both_the_eyes_is_a_stroke_symptom?"].apply(score_yes_no)
df["score_nosebleed"] = df["do_you_think_sudden_nosebleed_is_a_stroke_of_symptom?"].apply(score_misconception)
df["score_urgency"] = df["how_soon_treatment_should_be_taken_after_noticing_symptoms"].apply(score_action)
df["score_location"] = df["where_to_go_after_experiencing_symptoms_of_brain_stroke"].apply(score_location)

# === Step 4: Weighted sum and normalization ===
weights = {
    "score_specialist": 3,
    "score_know_stroke": 5,
    "score_confusion": 5,
    "score_numbness": 5,
    "score_vision": 2,
    "score_nosebleed": 2,
    "score_urgency": 5,
    "score_location": 5,
}

df["total_raw_score"] = sum(df[col] * w for col, w in weights.items())

# Correct normalization: use the true maximum possible raw score
max_values = {
    "score_specialist": 4,
    "score_know_stroke": 1,
    "score_confusion": 1,
    "score_numbness": 1,
    "score_vision": 1,
    "score_nosebleed": 2,
    "score_urgency": 2,
    "score_location": 4,
}

max_score = sum(weights[col] * max_values[col] for col in weights)
# max_score = 63

# Scale awareness_score to 0–10 range
df["awareness_score"] = (df["total_raw_score"] / max_score * 10).clip(0, 10).round(2)
# === Step 5: Save output ===
#output_path = "C:/Projects/stroke_ml_project/awareness_scores.csv"
#df.to_csv(output_path, index=False)

#print(f"✅ Awareness scores calculated and saved to {output_path}")
print("Sample data:")
print(df[["awareness_score"]].head())

print(f"Minimum Awareness Score: {df['awareness_score'].min()}")
print(f"Maximum Awareness Score: {df['awareness_score'].max()}")