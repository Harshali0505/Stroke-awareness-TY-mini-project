import pandas as pd

df = pd.read_excel(r"C:\Projects\Stroke-awareness-TY-mini-project\current_work\cleaned_datasheet_5.xlsx")

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
    if not isinstance(value, str):
        return 0

    v = value.lower().strip()

    # Hard stop
    if v in ["unaware", "no_response","other"]:
        return 0

    # Normalize "_or_" → ","
    v = v.replace("_or_", ",")

    valid_symptoms = {
        "balance_coordination_problem",
        "motor_weakness",
        "speech_language_problem",
        "vision_problem",
        "severe_headache",
        "swallowing_or_consciousness"
    }

    reported = {x.strip() for x in v.split(",")}

    return len(reported.intersection(valid_symptoms))


def score_risk_factors(value):
    if not isinstance(value, str):
        return 0

    v = value.lower().strip()

    # Hard stop
    if v in ["unaware", "no_response","other"]:
        return 0

    # Normalize "_or_" → ","
    v = v.replace("_or_", ",")

    risk_categories = {
        "blood_pressure", "heart_problem", "hypertension",
        "diabetes", "obesity",
        "smoking", "alcohol", "drugs",
        "age", "family_history"
    }

    reported = {x.strip() for x in v.split(",")}

    return len(reported.intersection(risk_categories))


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

df["score_specialist"] = df[
    "if_you_experience_symptoms_of_warning_signs,_which_specialist_would_you_consult?"
].apply(score_specialist)

df["score_know_stroke"] = df[
    "do_you_know_what_is_a_brain_stroke?"
].apply(score_yes_no)

df["score_action_first_symptom"] = df[
    "how_soon_would_you_consult_a_specialist_after_experiencing_the_first_symptom?"
].apply(score_action)

df["score_confusion"] = df[
    "do_you_think_sudden_confusion_,trouble_speaking_or_understanding_speech_is_a_stroke_symptom?"
].apply(score_yes_no)

df["score_numbness"] = df[
    "do_you_think_sudden_numbness_or_weakness_of_face,_arm_or_leg_is_a_symptom_of_stroke?"
].apply(score_yes_no)

df["score_nosebleed"] = df[
    "do_you_think_sudden_nosebleed_is_a_stroke_of_symptom?"
].apply(score_misconception)

df["score_vision"] = df[
    "do_you_think_trouble_seeing_in_one_or_both_the_eyes_is_a_stroke_symptom?"
].apply(score_yes_no)

df["score_first_contact"] = df[
    "first_contact_after_experiencing_symptom"
].apply(score_location)

df["score_urgency"] = df[
    "how_soon_treatment_should_be_taken_after_noticing_symptoms"
].apply(score_action)

df["score_location"] = df[
    "where_to_go_after_experiencing_symptoms_of_brain_stroke"
].apply(score_location)

df["score_symptoms"] = df[
    "stroke_symptoms"
].apply(score_symptom_checklist)

df["score_risk"] = df[
    "risk_factors"
].apply(score_risk_factors)

df["score_advice"] = df[
    "what_advice_would_you_give_for_someone_experiencing_stroke_symptoms"
].apply(score_advice)

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
# ===== Dynamic max values (post-capping removal) ===== #

max_values = {}

# Compute max observed value for each scored column
for col in weights:
    max_values[col] = df[col].max()

# Symptom-specific max (weighted)
max_symptom_score = sum(
    weights_symptom[col] * max_values[col]
    for col in weights_symptom
)

# Overall max (weighted)
max_score = sum(
    weights[col] * max_values[col]
    for col in weights
)

# ===== Normalization ===== #

df["symptom_awareness_score"] = (
    df["score_symptoms_combined"] / max_symptom_score * 10
).clip(0, 10).round(2)

df["awareness_score"] = (
    df["total_raw_score"] / max_score * 10
).clip(0, 10).round(2)


# === Step 5: Save output ===
output_path = r"C:\Projects\Stroke-awareness-TY-mini-project\current_work\awareness_scores.csv"
df.to_csv(output_path, index=False)
print(f"✅ Awareness scores calculated and saved to {output_path}")
print(df["awareness_score"].value_counts())
print(df["score_symptoms"].value_counts())
print(df["score_risk"].value_counts())
print("Awareness score range:",
      df["awareness_score"].min(),
      df["awareness_score"].max())

print("Symptom score range:",
      df["symptom_awareness_score"].min(),
      df["symptom_awareness_score"].max())
