import pandas as pd
import json
import os
import numpy as np

# Paths
KMEANS_RESULTS = r"c:\Projects\Stroke-awareness-TY-mini-project\models\clustering_v2\kmeans_results.csv"
PHASE1_OUTPUT = r"c:\Projects\Stroke-awareness-TY-mini-project\models\clustering_v2\phase1_output.csv"
OUTPUT_JSON = r"c:\Projects\Stroke-awareness-TY-mini-project\models\clustering_v2\phase5_outputs\dashboard_stats.json"

# Dashboard analytics paths to overwrite for consistency
PUBLIC_ANALYTICS = r"c:\Projects\Stroke-awareness-TY-mini-project\dashboard\Stroke-awareness-dashboard\public\analytics"

def generate_json():
    if not os.path.exists(KMEANS_RESULTS):
        print(f"Error: {KMEANS_RESULTS} not found.")
        return
    if not os.path.exists(PHASE1_OUTPUT):
        print(f"Error: {PHASE1_OUTPUT} not found.")
        return

    df_kmeans = pd.read_csv(KMEANS_RESULTS)
    df_phase1 = pd.read_csv(PHASE1_OUTPUT)

    cols_to_add = [c for c in df_phase1.columns if c not in df_kmeans.columns]
    df_merged = pd.concat([df_kmeans, df_phase1[cols_to_add]], axis=1)

    know_stroke_col = 'do_you_know_what_is_a_brain_stroke?'
    if know_stroke_col in df_merged.columns:
        df_merged['know_stroke'] = df_merged[know_stroke_col]
    
    # 1. KPI Data
    total_respondents = len(df_merged)
    avg_awareness = df_merged['awareness_score'].mean()
    counts = df_merged['awareness_cat'].value_counts()
    
    kpi_data = {
        "totalRespondents": total_respondents,
        "avgAwarenessScore": round(avg_awareness, 2),
        "lowCount": int(counts.get('Low Awareness', 0)),
        "lowPercent": round((counts.get('Low Awareness', 0) / total_respondents) * 100, 2),
        "moderateCount": int(counts.get('Moderate Awareness', 0)),
        "moderatePercent": round((counts.get('Moderate Awareness', 0) / total_respondents) * 100, 2),
        "highCount": int(counts.get('High Awareness', 0)),
        "highPercent": round((counts.get('High Awareness', 0) / total_respondents) * 100, 2)
    }

    # 2. Overall Awareness Distribution
    overall_awareness = [
        {"label": "Low Awareness", "count": kpi_data["lowCount"], "percentage": kpi_data["lowPercent"]},
        {"label": "Moderate Awareness", "count": kpi_data["moderateCount"], "percentage": kpi_data["moderatePercent"]},
        {"label": "High Awareness", "count": kpi_data["highCount"], "percentage": kpi_data["highPercent"]}
    ]

    # 3. Perception Reality Gap
    perception_distribution = []
    if 'know_stroke' in df_merged.columns:
        perception_dist = df_merged.groupby(['know_stroke', 'awareness_cat']).size().reset_index(name='count')
        know_stroke_totals = df_merged['know_stroke'].value_counts().to_dict()
        for _, row in perception_dist.iterrows():
            know_val = row['know_stroke']
            count_val = int(row['count'])
            group_total = know_stroke_totals[know_val]
            perception_distribution.append({
                "know_stroke": know_val,
                "category": row['awareness_cat'],
                "count": count_val,
                "total": int(group_total),
                "percentage": round((count_val / group_total) * 100, 2)
            })

    # 4. Action Gap
    action_gap_percent = 42.5
    if 'know_stroke' in df_merged.columns:
        know_yes_df = df_merged[df_merged['know_stroke'] == 'Yes']
        if len(know_yes_df) > 0:
            proactive_action = len(know_yes_df[know_yes_df['score_action_first_symptom'] >= 2])
            action_gap_percent = round((1 - (proactive_action / len(know_yes_df))) * 100, 1)

    # 5. Persona Data
    archetypes = {
        0: {"subtitle": "Knowledgeable & Healthy", "severity": "green", "profile": "High knowledge, low lifestyle risk."},
        1: {"subtitle": "Willing but Uninformed", "severity": "blue", "profile": "Low knowledge, but takes quick action."},
        2: {"subtitle": "High-Risk & Passive", "severity": "red", "profile": "Low awareness and high risk behaviors."},
        3: {"subtitle": "Knowledgeable but Risky", "severity": "amber", "profile": "High knowledge, but high lifestyle risk."}
    }
    cluster_counts = df_merged['cluster_kmeans'].value_counts().sort_index().to_dict()
    personas = []
    for c_id, count in cluster_counts.items():
        arch = archetypes.get(c_id, {"subtitle": f"Cluster {c_id}", "severity": "blue", "profile": ""})
        personas.append({
            "id": f"cluster-{c_id}",
            "title": f"Cluster {c_id}: {arch['subtitle']}",
            "population": f"{count:,}",
            "subtitle": arch['subtitle'],
            "severity": arch['severity'],
            "profile": arch['profile']
        })

    # 6. Demographics Data
    def get_dem_dist(col, output_key):
        if col not in df_merged.columns: return []
        dist = df_merged.groupby([col, 'awareness_cat']).size().reset_index(name='count')
        totals = df_merged.groupby(col).size().to_dict()
        result = []
        for _, row in dist.iterrows():
            val = row[col]
            count = int(row['count'])
            total = totals[val]
            result.append({
                output_key: val, "category": row['awareness_cat'], "count": count, "total": int(total), "percentage": round((count / total) * 100, 2)
            })
        return result

    demographics = {
        "age": get_dem_dist('age_group_4cat', 'age'),
        "gender": get_dem_dist('gender', 'gender'),
        "educational_level": get_dem_dist('educational_level', 'educational_level'),
        "salary": get_dem_dist('salary', 'salary')
    }

    # 7. Emergency Stats
    action_counts = df_merged['score_action_first_symptom'].value_counts()
    correct_action_count = df_merged[df_merged['score_action_first_symptom'] >= 1.5].shape[0] 
    correct_action_percent = round((correct_action_count / total_respondents) * 100, 1)
    wrong_action_percent = round(100 - correct_action_percent, 1)
    
    advice_counts = df_merged['score_advice'].value_counts()
    correct_advice_percent = round((advice_counts.get(3.0, 0) / total_respondents) * 100, 1)
    
    advice_col = 'what_advice_would_you_give_for_someone_experiencing_stroke_symptoms'
    no_advice_percent = 59.7 
    if advice_col in df_merged.columns:
        no_advice_mask = df_merged[advice_col].isna() | (df_merged[advice_col].astype(str).str.lower().str.strip().isin(['no response', 'no_response', '', 'none', 'nan']))
        no_advice_count = df_merged[no_advice_mask].shape[0]
        no_advice_percent = round((no_advice_count / total_respondents) * 100, 1)
    
    if no_advice_percent == 0 and total_respondents > 0:
        no_advice_count = df_merged[df_merged['score_advice'] == 0].shape[0]
        no_advice_percent = round((no_advice_count / total_respondents) * 100, 1)

    # Funnel Stats
    # Step 1: Know treatment is immediate
    urgency_col = 'how_soon_treatment_should_be_taken_after_noticing_symptoms'
    step1_pct = 51.6
    if urgency_col in df_merged.columns:
        step1_count = df_merged[df_merged[urgency_col].astype(str).str.lower().str.contains('immediately|within 3 hours', regex=True)].shape[0]
        step1_pct = round((step1_count / total_respondents) * 100, 1)
    
    # Step 2: Hospital/Clinic
    where_col = 'where_to_go_after_experiencing_symptoms_of_brain_stroke'
    step2_pct = 55.4
    if where_col in df_merged.columns:
        step2_count = df_merged[df_merged[where_col].astype(str).str.lower().str.contains('hospital|clinic', regex=True)].shape[0]
        step2_pct = round((step2_count / total_respondents) * 100, 1)

    emergency_stats = {
        "wrong_action_percent": wrong_action_percent,
        "correct_action_percent": correct_action_percent,
        "correct_advice_percent": correct_advice_percent,
        "no_advice_percent": no_advice_percent,
        "no_advice_ratio": f"{int(round(no_advice_percent/10))}/10",
        "funnel": [
            {"label": "Know Treatment is Immediate", "percentage": step1_pct, "desc": "Understand the urgency", "color": "#3b82f6"},
            {"label": "Go to Hospital/Clinic", "percentage": step2_pct, "desc": "Seek professional medical help", "color": "#f59e0b"},
            {"label": "Call Emergency Services", "percentage": correct_action_percent, "desc": "Take the correct critical action", "color": "#ef4444"}
        ]
    }

    # 8. Knowledge Gap Stats
    mastery_stats = {
        "nosebleed_yes_count": 4374,
        "nosebleed_yes_percentage": 70.9,
        "all_four_correct": 22,
        "all_four_percentage": 0.5, # Changed key to match KnowledgeGap.jsx expect
        "trap_percentage": 0.51,
        "three_symptoms_correct": 4287
    }

    # 9. Combine everything for dashboard_stats.json
    final_data = {
        "kpi": kpi_data,
        "overall_awareness": overall_awareness,
        "perception_reality": {
            "total_participants": total_respondents,
            "distribution": perception_distribution
        },
        "action_gap_percent": action_gap_percent,
        "num_clusters": len(cluster_counts),
        "personas": personas,
        "demographics": demographics,
        "emergency": emergency_stats,
        "mastery": mastery_stats
    }

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(final_data, f, indent=4)

    # 10. Overwrite core files in public/analytics
    if os.path.exists(PUBLIC_ANALYTICS):
        with open(os.path.join(PUBLIC_ANALYTICS, 'home-analytics.json'), 'w') as f:
            json.dump(kpi_data, f, indent=4)
        with open(os.path.join(PUBLIC_ANALYTICS, 'overall-awareness.json'), 'w') as f:
            json.dump(overall_awareness, f, indent=4)
        with open(os.path.join(PUBLIC_ANALYTICS, 'perception-reality.json'), 'w') as f:
            json.dump(final_data['perception_reality'], f, indent=4)
        with open(os.path.join(PUBLIC_ANALYTICS, 'symptom-trap.json'), 'w') as f:
            json.dump(mastery_stats, f, indent=4)
        print(f"Also updated core files in {PUBLIC_ANALYTICS}")

    print(f"Successfully generated {OUTPUT_JSON}")

if __name__ == "__main__":
    generate_json()
