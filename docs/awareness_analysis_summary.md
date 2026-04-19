# Stroke Awareness Scoring Analysis

This analysis breaks down the scoring algorithm used in the **Stroke Awareness TY Mini Project** and defines the characteristics of individuals across three levels of awareness: **Low, Moderate, and High**.

---

## 🏗️ The Scoring Algorithm

The project uses a weighted scoring system (out of 10) to quantify awareness. The score is derived from several key behavioral and knowledge-based dimensions.

### Core Scoring Components & Weights

| Component | Weight | Max Variable Score | Logic Summary |
| :--- | :---: | :---: | :--- |
| **General Knowledge** | 5 | 1 | "Do you know what a brain stroke is?" (Yes=1, No=0). |
| **Symptom Recognition** | 5-20 | Variable | Identifying confusion, numbness, and vision issues. Sub-checklist identifies specific medical signs. |
| **Clinical Intuition** | 3 | 4 | Choice of specialist (Neurologist=4, Physician=2, Doctor=1). |
| **Response Urgency** | 8 | 2+2 | Speed of action (Immediately=2, Within 24hrs=1) and perceived urgency. |
| **Emergency Literacy** | 10 | 4+4 | Knowing where to go (Emergency=4, Hospital=3). |
| **Risk Factors** | 3 | Variable | Recognizing BP, Diabetes, Obesity, Smoking, etc. |

---

## 🔍 Awareness Level Characteristics

Based on the thresholds defined in `awareness_visualization.py` and the scoring logic in `awareness_scoring.py`, here are the archetypal characteristics for each group:

### 🔴 1. Low Awareness (Score < 6.0)
*These individuals are the highest priority for medical education and intervention.*

- **Knowledge Gap**: Often lacks a basic definition of what a brain stroke is.
- **Symptom Recognition**: Identifies **3 or fewer** symptoms. Likely misses "silent" or sudden signs like confusion or vision loss.
- **Passive Response**: Would wait **24 hours or more** to seek help. Does not equate symptoms with a medical emergency.
- **Healthcare Miscue**: Would consult a general practitioner ("Doctor") rather than a specialist. Might go to a clinic or general hospital instead of an Emergency Room.
- **Risk Ignorance**: Recognizes very few (0-3) risk factors, potentially ignoring silent killers like hypertension or lifestyle risks.
- **Misconceptions**: More likely to believe incorrect symptoms (e.g., nosebleeds) are signs of a stroke.

### 🔵 2. Moderate Awareness (Score 6.0 - 8.5)
*These individuals have "fragmented knowledge"—they know something is wrong but may hesitate.*

- **Baseline Knowledge**: Generally knows what a stroke is but may not understand the pathophysiology.
- **Symptom Recognition**: Identifies **4 core symptoms**. Recognizes physical signs like numbness but may be less certain about cognitive signs (confusion).
- **Delayed Urgency**: Understands the need for help but might wait "within a few hours" to see if symptoms resolve.
- **Generalist Approach**: Would seek a "Physician" or a "Hospital," showing good intent but lacking the specific knowledge of "Neurology" or "Emergency" priority.
- **Partial Risk Awareness**: Recognizes a moderate number (**4-6**) of risk factors.
- **Advice**: Would advise others to see a doctor but might not use "Ambulance" or "Emergency" as the first line of advice.

### 🟢 3. High Awareness (Score ≥ 8.5)
*These individuals are medical-literate and proactive ("Time is Brain").*

- **Deep Knowledge**: Clear and accurate understanding of stroke.
- **Full Recognition**: Identifies **5 or more** symptoms correctly and holds no common misconceptions.
- **Immediate Action**: Recognizes a stroke as a 911/Emergency event. Would seek help **"Immediately / ASAP."**
- **Specialist Focused**: Explicitly identifies a **"Neurologist"** as the required specialist.
- **Emergency Literacy**: Knows to go straight to an **"Emergency Room"** or **"Neurology"** department.
- **Holistic Risk Awareness**: Identifies a wide breadth of risk factors (**>6**), including age, family history, and lifestyle factors.
- **Advocacy**: Strong advice to others to call an ambulance or head to the ER immediately.

---

## 📊 Summary of Categorization Thresholds

| Category | Awareness Score (0-10) | Checklist Symptoms (Avg) | Risk Factors (Avg) | Priority |
| :--- | :---: | :---: | :---: | :--- |
| **Low** | < 6.0 | 0 - 3 | 0 - 3 | **Critical** |
| **Moderate** | 6.0 - 8.5 | 4 | 4 - 6 | **Maintain** |
| **High** | ≥ 8.5 | 5+ | 7+ | **Advocate** |

> [!TIP]
> The "Awareness-Action Gap" (Cognitive Paradox) is most prevalent in the **Moderate** group—they know the symptoms but often lack the "High Awareness" urgency to seek emergency care immediately.
