import pandas as pd

try:
    df = pd.read_csv(r"C:\Projects\Stroke-awareness-TY-mini-project\current_work\awareness_scores.csv")
    
    # Rename the corrupted column
    df.rename(columns={'do_you_currently_have_any_complaints_or_health_issues_related_to_your_heart_or_kidneys?"=': 'do_you_currently_have_any_complaints_or_health_issues_related_to_your_heart_or_kidneys?'}, inplace=True)
    
    cols_to_check = [
        "gender",
        "educational_level",
        "salary",
        "location",
        "do_you__consume_alcohol?",
        "do_you_smoke?_if_so,_how_much_and_often?",
        "do_you_engage_in_regular_physical_activity_or_exercise?",
        "do_you_currently_have_any_complaints_or_health_issues_related_to_your_heart_or_kidneys?",
        "do_you_have_a_family_history_of_brain_or_heart_stroke,_of_hypertension_or_diabetes_?",
        "tia",
        "score_specialist"
    ]
    
    for c in cols_to_check:
        if c in df.columns:
            print(f"\n=== {c} ===")
            print(df[c].unique())
        else:
            print(f"\nMissing column: {c}")

except Exception as e:
    print(f"Error: {e}")
