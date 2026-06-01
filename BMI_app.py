import streamlit as st
import math
import random
import numpy as np
import pandas as pd

# ── ML imports (scikit-learn — ships with most Python envs) ──────────────────
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="BMI Universe",
    page_icon="🌌",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: #0a0a14;
    color: #e8e8f0;
}
.stApp {
    background: radial-gradient(ellipse at 20% 50%, #1a0a2e 0%, #0a0a14 60%),
                radial-gradient(ellipse at 80% 20%, #0d1a2e 0%, transparent 50%);
    min-height: 100vh;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: clamp(2.4rem, 6vw, 4rem);
    background: linear-gradient(135deg, #a78bfa, #38bdf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 0;
}
.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #6366f1;
    text-align: center;
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 6px;
    margin-bottom: 32px;
}
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 28px 32px;
    margin: 16px 0;
    backdrop-filter: blur(12px);
}
.bmi-display { text-align: center; padding: 32px 0 20px; }
.bmi-number {
    font-family: 'Space Mono', monospace;
    font-size: 5.5rem;
    font-weight: 700;
    line-height: 1;
    letter-spacing: -3px;
}
.bmi-label {
    font-family: 'Syne', sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 8px;
}
.cat-underweight { color: #38bdf8; }
.cat-normal      { color: #4ade80; }
.cat-overweight  { color: #fbbf24; }
.cat-obese       { color: #f87171; }
.bmi-bar-wrap { margin: 20px 0; position: relative; }
.bmi-bar-track {
    height: 10px;
    border-radius: 999px;
    background: linear-gradient(90deg, #38bdf8 0%, #4ade80 30%, #fbbf24 65%, #f87171 100%);
    position: relative; opacity: 0.7;
}
.bmi-bar-needle {
    position: absolute; top: -5px;
    width: 20px; height: 20px;
    border-radius: 50%; background: white;
    box-shadow: 0 0 12px rgba(255,255,255,0.8);
    transform: translateX(-50%);
    transition: left 0.8s cubic-bezier(.34,1.56,.64,1);
}
.fun-fact {
    background: rgba(99,102,241,0.12);
    border-left: 3px solid #6366f1;
    border-radius: 0 12px 12px 0;
    padding: 14px 18px;
    font-size: 0.88rem;
    color: #c4b5fd;
    font-family: 'Space Mono', monospace;
    line-height: 1.6;
    margin: 16px 0;
}
.ml-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.12), rgba(167,139,250,0.08));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 20px;
    padding: 24px 28px;
    margin: 16px 0;
}
.ml-badge {
    display: inline-block;
    background: linear-gradient(135deg, #6366f1, #a78bfa);
    color: white;
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 12px;
}
.risk-low    { color: #4ade80; font-weight: 700; font-size: 1.3rem; }
.risk-medium { color: #fbbf24; font-weight: 700; font-size: 1.3rem; }
.risk-high   { color: #f87171; font-weight: 700; font-size: 1.3rem; }
.prob-bar-wrap { margin: 10px 0; }
.prob-bar-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #9ca3af;
    margin-bottom: 4px;
}
.planet-badge {
    display: block; text-align: center;
    font-size: 3.5rem;
    animation: float 3s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-10px); }
}
.metric-pill {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 50px;
    padding: 8px 20px;
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    display: inline-block;
    margin: 4px;
}
div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
    font-family: 'Space Mono', monospace !important;
}
div[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
    color: #e8e8f0 !important;
}
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #6366f1, #a78bfa) !important;
    color: white !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 14px 32px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    letter-spacing: 1px !important;
    cursor: pointer !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.4) !important;
}
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent !important; }
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 50px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: #9ca3af !important;
    font-family: 'Syne', sans-serif !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #6366f1, #a78bfa) !important;
    color: white !important;
    border-color: transparent !important;
}
.history-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-family: 'Space Mono', monospace;
    font-size: 0.8rem;
    color: #9ca3af;
}
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 12px;
}
hr { border-color: rgba(255,255,255,0.06) !important; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════
# ── ML MODEL 1: Health Risk Classifier (Random Forest) ──────────
# Trained on a synthetic but medically-grounded dataset
# Features: bmi, age, activity_encoded, gender_encoded
# Labels: Low / Medium / High (metabolic health risk)
# ════════════════════════════════════════════════════════════════

@st.cache_resource
def train_risk_model():
    """
    Train a Random Forest on synthetic health data.
    Ground truth is based on established clinical risk thresholds:
    - BMI ranges, age, activity level, gender
    Risk levels: 0=Low, 1=Medium, 2=High
    """
    rng = np.random.default_rng(42)
    n = 4000

    bmi      = rng.uniform(14, 45, n)
    age      = rng.uniform(18, 80, n)
    activity = rng.integers(0, 5, n)   # 0=sedentary … 4=very active
    gender   = rng.integers(0, 2, n)   # 0=Female, 1=Male

    # Rule-based risk labels (mimicking clinical guidelines)
    risk = np.zeros(n, dtype=int)
    for i in range(n):
        score = 0
        if bmi[i] < 16 or bmi[i] >= 35:        score += 3
        elif bmi[i] < 18.5 or bmi[i] >= 30:    score += 2
        elif bmi[i] >= 25:                       score += 1
        if age[i] > 60:                          score += 2
        elif age[i] > 45:                        score += 1
        if activity[i] == 0:                     score += 2
        elif activity[i] == 1:                   score += 1
        elif activity[i] >= 3:                   score -= 1
        # add slight noise
        score += rng.integers(-1, 2)
        risk[i] = 0 if score <= 1 else (1 if score <= 3 else 2)

    X = np.column_stack([bmi, age, activity, gender])
    clf = Pipeline([
        ("scaler", StandardScaler()),
        ("rf", RandomForestClassifier(n_estimators=200, max_depth=8,
                                       random_state=42, n_jobs=-1))
    ])
    clf.fit(X, risk)
    return clf


# ════════════════════════════════════════════════════════════════
# ── ML MODEL 2: BMI Trajectory Forecaster (Gradient Boosting) ──
# Uses the user's session BMI history to forecast next 30 days
# Features: day index, rolling mean, delta
# ════════════════════════════════════════════════════════════════

@st.cache_resource
def train_trajectory_model():
    """
    Pre-train a GBR on synthetic trajectories so it can extrapolate
    even from very short sequences (2+ points).
    """
    rng = np.random.default_rng(7)
    X_all, y_all = [], []

    for _ in range(500):
        start   = rng.uniform(16, 42)
        trend   = rng.uniform(-0.08, 0.08)
        noise   = rng.uniform(0.05, 0.3)
        length  = rng.integers(5, 30)
        series  = [start + trend * t + rng.normal(0, noise) for t in range(length)]
        for t in range(2, length):
            delta    = series[t-1] - series[t-2]
            roll_avg = np.mean(series[max(0, t-3):t])
            X_all.append([t, delta, roll_avg, series[t-1]])
            y_all.append(series[t])

    gbr = Pipeline([
        ("scaler", StandardScaler()),
        ("gbr", GradientBoostingRegressor(n_estimators=300, max_depth=4,
                                           learning_rate=0.05, random_state=42))
    ])
    gbr.fit(X_all, y_all)
    return gbr


# ── Helper functions ──────────────────────────────────────────────────────────

def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

def get_category(bmi):
    if bmi < 18.5:   return "Underweight", "cat-underweight", "🪐"
    elif bmi < 25:   return "Normal",       "cat-normal",      "🌍"
    elif bmi < 30:   return "Overweight",   "cat-overweight",  "🌙"
    else:            return "Obese",        "cat-obese",       "☄️"

def bmi_needle_percent(bmi):
    return (max(10, min(45, bmi)) - 10) / 35 * 100

def ideal_weight_range(height_m):
    return 18.5 * (height_m**2), 24.9 * (height_m**2)

def calories_tdee(weight_kg, height_cm, age, gender, activity):
    bmr = (10*weight_kg + 6.25*height_cm - 5*age + (5 if gender=="Male" else -161))
    return bmr * {"Sedentary":1.2,"Light":1.375,"Moderate":1.55,"Active":1.725,"Very Active":1.9}[activity]

def activity_to_int(act):
    return {"Sedentary":0,"Light":1,"Moderate":2,"Active":3,"Very Active":4}.get(act, 2)

def risk_label_color(pred):
    return [("Low", "risk-low", "🟢"), ("Medium", "risk-medium", "🟡"), ("High", "risk-high", "🔴")][pred]

FUN_FACTS = [
    "💡 BMI was invented by Belgian mathematician Adolphe Quetelet in the 1830s — nearly 200 years old!",
    "🚀 On the Moon, your weight drops to ~16.5% — everyone would be 'underweight' there!",
    "🏋️ Many elite athletes score 'overweight' on BMI due to high muscle mass.",
    "🧬 BMI can't distinguish between fat, muscle, or bone density.",
    "🌍 The average global BMI has risen ~1 unit per decade since 1975.",
    "⚡ Losing just 5–10% of body weight can significantly improve key health markers.",
]

MOTIVATIONAL = {
    "Underweight": ["Your body is asking for a little more fuel — nourish it with love 🌱",
                    "Small, consistent gains make a universe of difference 🌟"],
    "Normal":      ["You're in the sweet spot — keep riding this orbit! 🌍",
                    "Stellar work! Keep those healthy habits locked in 🔐"],
    "Overweight":  ["Every journey starts with a single step — you've got this 💪",
                    "Small lifestyle shifts compound into massive change ⚡"],
    "Obese":       ["Your health journey is valid — every positive choice matters 💙",
                    "Change is possible; it begins with today's choices 🌅"],
}

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "streak" not in st.session_state:
    st.session_state.streak = 0

# ── Load models (cached) ──────────────────────────────────────────────────────
risk_model       = train_risk_model()
trajectory_model = train_trajectory_model()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">BMI UNIVERSE</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Body Mass Index · AI Health Explorer</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🚀 Calculate", "🤖 AI Insights", "📊 History", "ℹ️ About"])


# ══════════════════════════════════════════════════════════════
# TAB 1 — CALCULATE
# ══════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-label">Unit System</div>', unsafe_allow_html=True)
    unit = st.radio("Unit", ["Metric (kg / m)", "Imperial (lbs / ft & in)"],
                    horizontal=True, label_visibility="collapsed")

    col1, col2 = st.columns(2)
    with col1:
        if unit == "Metric (kg / m)":
            weight_kg = st.number_input("⚖️ Weight (kg)", min_value=1.0, max_value=500.0, value=70.0, step=0.5)
        else:
            weight_lbs = st.number_input("⚖️ Weight (lbs)", min_value=2.0, max_value=1100.0, value=154.0, step=1.0)
            weight_kg = weight_lbs * 0.453592
    with col2:
        if unit == "Metric (kg / m)":
            height_m = st.number_input("📏 Height (m)", min_value=0.5, max_value=2.5, value=1.75, step=0.01)
        else:
            ft   = st.number_input("📏 Height (ft)",   min_value=1, max_value=8,  value=5, step=1)
            inch = st.number_input("+ inches",          min_value=0, max_value=11, value=9, step=1)
            height_m = (ft * 12 + inch) * 0.0254

    with st.expander("🔬 Advanced Inputs (TDEE + AI Risk)", expanded=False):
        col_a, col_b, col_c = st.columns(3)
        with col_a: age      = st.number_input("Age", min_value=10, max_value=120, value=25)
        with col_b: gender   = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
        with col_c: activity = st.selectbox("Activity Level", ["Sedentary","Light","Moderate","Active","Very Active"])

    st.markdown("")
    calc_btn = st.button("✦ CALCULATE MY BMI ✦")

    if calc_btn:
        bmi = calculate_bmi(weight_kg, height_m)
        category, css_class, planet = get_category(bmi)
        needle_pct = bmi_needle_percent(bmi)
        ideal_low, ideal_high = ideal_weight_range(height_m)
        motivation = random.choice(MOTIVATIONAL[category])
        fun_fact   = random.choice(FUN_FACTS)

        st.session_state.history.append({
            "bmi": round(bmi, 2),
            "category": category,
            "weight": round(weight_kg, 1),
            "height": round(height_m, 2),
            "age": age,
            "gender": gender,
            "activity": activity,
        })
        st.session_state.streak += 1

        # Result card
        st.markdown(f"""
        <div class="glass-card bmi-display">
            <div class="planet-badge">{planet}</div>
            <div class="bmi-number {css_class}">{bmi:.1f}</div>
            <div class="bmi-label {css_class}">{category}</div>
            <div class="bmi-bar-wrap" style="margin-top:24px;">
                <div class="bmi-bar-track"></div>
                <div class="bmi-bar-needle" style="left:{needle_pct:.1f}%"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-family:'Space Mono',monospace;font-size:0.65rem;color:#4b5563;margin-top:6px;">
                <span>10</span><span>18.5</span><span>25</span><span>30</span><span>45</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        height_cm = height_m * 100
        st.markdown(f"""
        <div style="text-align:center;margin:8px 0 16px;">
            <span class="metric-pill">⚖️ {weight_kg:.1f} kg</span>
            <span class="metric-pill">📏 {height_cm:.0f} cm</span>
            <span class="metric-pill">🎯 Ideal: {ideal_low:.1f}–{ideal_high:.1f} kg</span>
        </div>
        """, unsafe_allow_html=True)

        if gender in ["Male", "Female"]:
            tdee = calories_tdee(weight_kg, height_cm, age, gender, activity)
            st.markdown(f'<div style="text-align:center;margin-bottom:16px;"><span class="metric-pill">🔥 TDEE: {tdee:.0f} kcal/day</span></div>', unsafe_allow_html=True)

        # ── Quick AI Risk Preview ──────────────────────────────
        if gender in ["Male", "Female"]:
            act_enc = activity_to_int(activity)
            gen_enc = 1 if gender == "Male" else 0
            X_pred  = np.array([[bmi, age, act_enc, gen_enc]])
            risk_pred  = risk_model.predict(X_pred)[0]
            risk_proba = risk_model.predict_proba(X_pred)[0]
            label, css, emoji = risk_label_color(risk_pred)

            st.markdown(f"""
            <div class="ml-card">
                <span class="ml-badge">🤖 Random Forest · Health Risk</span>
                <div style="display:flex;align-items:center;gap:16px;margin:8px 0;">
                    <span style="font-size:2rem;">{emoji}</span>
                    <div>
                        <span class="{css}">{label} Risk</span>
                        <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#6b7280;margin-top:4px;">
                            Confidence: {max(risk_proba)*100:.0f}%
                        </div>
                    </div>
                </div>
                <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#6b7280;">
                    Based on BMI · age · activity level · gender<br>
                    → See the <strong>AI Insights</strong> tab for full breakdown
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f'<div class="fun-fact">💬 {motivation}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="fun-fact">{fun_fact}</div>', unsafe_allow_html=True)
        if category == "Normal":
            st.balloons()


# ══════════════════════════════════════════════════════════════
# TAB 2 — AI INSIGHTS
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">Machine Learning Health Analysis</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:48px 32px;">
            <div style="font-size:3rem;">🤖</div>
            <div style="font-family:'Space Mono',monospace;color:#4b5563;font-size:0.85rem;margin-top:12px;">
                Calculate your BMI first to unlock AI insights.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        last = st.session_state.history[-1]
        bmi_val  = last["bmi"]
        age_val  = last.get("age", 30)
        act_str  = last.get("activity", "Moderate")
        gen_str  = last.get("gender", "Male")

        act_enc = activity_to_int(act_str)
        gen_enc = 1 if gen_str == "Male" else 0

        # ── MODEL 1: Risk Classification ──────────────────────
        st.markdown("### 🤖 Model 1 · Health Risk Classifier")
        st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;color:#6b7280;margin-bottom:12px;">Algorithm: Random Forest (200 trees) · Trained on 4,000 synthetic profiles</div>', unsafe_allow_html=True)

        X_pred     = np.array([[bmi_val, age_val, act_enc, gen_enc]])
        risk_pred  = risk_model.predict(X_pred)[0]
        risk_proba = risk_model.predict_proba(X_pred)[0]
        label, css, emoji = risk_label_color(risk_pred)

        st.markdown(f"""
        <div class="ml-card">
            <div style="display:flex;align-items:center;gap:16px;margin-bottom:16px;">
                <span style="font-size:2.5rem;">{emoji}</span>
                <div>
                    <span class="{css}">{label} Metabolic Risk</span>
                    <div style="font-family:'Space Mono',monospace;font-size:0.75rem;color:#9ca3af;margin-top:4px;">
                        Model confidence: {max(risk_proba)*100:.1f}%
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Probability bars
        risk_names  = ["Low Risk", "Medium Risk", "High Risk"]
        risk_colors = ["#4ade80",  "#fbbf24",     "#f87171"]
        prob_df = pd.DataFrame({
            "Risk Level": risk_names,
            "Probability": [p * 100 for p in risk_proba],
        })
        st.markdown('<div class="section-label">Probability Distribution</div>', unsafe_allow_html=True)
        st.bar_chart(prob_df.set_index("Risk Level"), color=["#a78bfa"], height=200)

        # Feature importance from the RF
        rf_model   = risk_model.named_steps["rf"]
        feat_names = ["BMI", "Age", "Activity Level", "Gender"]
        importance = rf_model.feature_importances_
        imp_df = pd.DataFrame({"Feature": feat_names, "Importance": importance * 100})
        imp_df = imp_df.sort_values("Importance", ascending=False)

        st.markdown('<div class="section-label" style="margin-top:16px;">What drives this prediction?</div>', unsafe_allow_html=True)
        for _, row in imp_df.iterrows():
            bar_w = int(row["Importance"] * 2.5)
            st.markdown(
                f'<div style="display:flex;align-items:center;gap:12px;margin:6px 0;">'
                f'<span style="font-family:Space Mono,monospace;font-size:0.75rem;color:#9ca3af;width:110px;">{row["Feature"]}</span>'
                f'<div style="flex:1;height:8px;border-radius:999px;background:rgba(255,255,255,0.06);">'
                f'<div style="width:{bar_w}%;height:100%;border-radius:999px;background:linear-gradient(90deg,#6366f1,#a78bfa);"></div>'
                f'</div>'
                f'<span style="font-family:Space Mono,monospace;font-size:0.72rem;color:#6366f1;">{row["Importance"]:.1f}%</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        # ── What-if simulator ─────────────────────────────────
        st.markdown("---")
        st.markdown("### 🔮 What-If Simulator")
        st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;color:#6b7280;margin-bottom:16px;">Adjust sliders to see how lifestyle changes shift your predicted risk</div>', unsafe_allow_html=True)

        wi_col1, wi_col2 = st.columns(2)
        with wi_col1:
            wi_bmi = st.slider("Simulated BMI", 14.0, 45.0, float(round(bmi_val, 1)), 0.1)
            wi_age = st.slider("Simulated Age", 18, 80, int(age_val))
        with wi_col2:
            wi_act = st.select_slider("Simulated Activity",
                                       options=["Sedentary","Light","Moderate","Active","Very Active"],
                                       value=act_str)
            wi_gen = st.selectbox("Simulated Gender", ["Male","Female"],
                                   index=0 if gen_str=="Male" else 1)

        wi_X     = np.array([[wi_bmi, wi_age, activity_to_int(wi_act), 1 if wi_gen=="Male" else 0]])
        wi_pred  = risk_model.predict(wi_X)[0]
        wi_proba = risk_model.predict_proba(wi_X)[0]
        wi_label, wi_css, wi_emoji = risk_label_color(wi_pred)
        delta_conf = (max(wi_proba) - max(risk_proba)) * 100

        st.markdown(f"""
        <div class="ml-card">
            <span class="ml-badge">Simulated Result</span>
            <div style="display:flex;align-items:center;gap:16px;margin-top:8px;">
                <span style="font-size:2rem;">{wi_emoji}</span>
                <div>
                    <span class="{wi_css}">{wi_label}</span>
                    <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#6b7280;margin-top:4px;">
                        Confidence: {max(wi_proba)*100:.1f}%
                        {"  ▲" if delta_conf > 0 else "  ▼" if delta_conf < 0 else ""} {abs(delta_conf):.1f}% vs current
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── MODEL 2: Trajectory Forecast ─────────────────────
        st.markdown("---")
        st.markdown("### 📈 Model 2 · BMI Trajectory Forecaster")
        st.markdown('<div style="font-family:\'Space Mono\',monospace;font-size:0.72rem;color:#6b7280;margin-bottom:12px;">Algorithm: Gradient Boosting Regressor · Pre-trained on 500 synthetic trajectories</div>', unsafe_allow_html=True)

        bmi_series = [h["bmi"] for h in st.session_state.history]

        if len(bmi_series) < 2:
            st.markdown("""
            <div class="ml-card" style="text-align:center;padding:32px;">
                <div style="font-size:2rem;">📊</div>
                <div style="font-family:'Space Mono',monospace;font-size:0.8rem;color:#6b7280;margin-top:8px;">
                    Log <strong>2+ BMI readings</strong> to unlock the trajectory forecast
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Forecast 30 days forward
            forecast_days = 30
            extended = list(bmi_series)
            for t in range(len(extended), len(extended) + forecast_days):
                delta    = extended[-1] - extended[-2]
                roll_avg = np.mean(extended[max(0, len(extended)-3):])
                x_row    = [[t, delta, roll_avg, extended[-1]]]
                nxt      = trajectory_model.predict(x_row)[0]
                nxt      = max(10, min(60, nxt))  # clamp
                extended.append(round(nxt, 2))

            actual_len   = len(bmi_series)
            forecast_len = forecast_days

            chart_df = pd.DataFrame({
                "Actual BMI":   bmi_series + [None] * forecast_len,
                "Forecast BMI": [None] * (actual_len - 1) + [bmi_series[-1]] + extended[actual_len:],
            })
            st.line_chart(chart_df, height=240, color=["#4ade80", "#a78bfa"])

            proj_bmi = extended[-1]
            proj_cat, proj_css, proj_planet = get_category(proj_bmi)
            direction = "📈" if proj_bmi > bmi_series[-1] else ("📉" if proj_bmi < bmi_series[-1] else "➡️")
            delta_bmi = proj_bmi - bmi_series[-1]

            st.markdown(f"""
            <div class="ml-card">
                <span class="ml-badge">30-Day Projection</span>
                <div style="display:flex;align-items:center;gap:16px;margin-top:8px;">
                    <span style="font-size:2rem;">{direction}</span>
                    <div>
                        <span style="font-family:'Space Mono',monospace;font-size:1.4rem;color:#a78bfa;font-weight:700;">{proj_bmi:.1f}</span>
                        <span style="font-family:'Space Mono',monospace;font-size:0.8rem;color:#6b7280;"> predicted BMI</span>
                        <div style="font-family:'Space Mono',monospace;font-size:0.72rem;color:#6b7280;margin-top:4px;">
                            {'+' if delta_bmi >= 0 else ''}{delta_bmi:.2f} from current · Category: <span class="{proj_css}">{proj_cat}</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="fun-fact">
            ⚠️ This forecast extrapolates your <em>session trend only</em>.
            It assumes similar lifestyle and is for educational purposes — not medical advice.
            More data points = more accurate forecast.
            </div>
            """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 3 — HISTORY
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-label">Your BMI Log</div>', unsafe_allow_html=True)
    if not st.session_state.history:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:48px 32px;">
            <div style="font-size:3rem;">🌌</div>
            <div style="font-family:'Space Mono',monospace;color:#4b5563;font-size:0.85rem;margin-top:12px;">
                No calculations yet. Head to the Calculate tab to begin.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        bmi_values = [h["bmi"] for h in st.session_state.history]
        if len(bmi_values) > 1:
            st.markdown('<div class="section-label">BMI Trend</div>', unsafe_allow_html=True)
            st.line_chart(pd.DataFrame({"BMI": bmi_values}), color="#a78bfa", height=180)

        st.markdown('<div class="section-label">Log Entries</div>', unsafe_allow_html=True)
        cat_colors = {"Underweight":"#38bdf8","Normal":"#4ade80","Overweight":"#fbbf24","Obese":"#f87171"}
        for i, h in enumerate(reversed(st.session_state.history), 1):
            color = cat_colors.get(h["category"], "#9ca3af")
            n = len(st.session_state.history) - i + 1
            st.markdown(
                f'<div class="history-row">'
                f'<span>#{n}</span>'
                f'<span style="color:{color};font-weight:700;">{h["bmi"]}</span>'
                f'<span style="color:{color};">{h["category"]}</span>'
                f'<span>{h["weight"]} kg / {h["height"]} m</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        st.markdown("")
        if st.button("🗑️ Clear History"):
            st.session_state.history = []
            st.session_state.streak = 0
            st.rerun()

        streak = st.session_state.streak
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;padding:20px;">
            <div style="font-size:2rem;">🔥</div>
            <div style="font-family:'Space Mono',monospace;font-size:0.8rem;color:#a78bfa;">
                {streak} calculation{"s" if streak != 1 else ""} tracked this session
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# TAB 4 — ABOUT
# ══════════════════════════════════════════════════════════════
with tab4:
    st.markdown("""
    <div class="glass-card">
        <div class="section-label">What is BMI?</div>
        <p style="font-size:0.9rem;line-height:1.8;color:#d1d5db;">
        Body Mass Index is a simple screening value from <strong>weight ÷ height²</strong>.
        It provides a general indicator of weight categories that may affect health.
        </p>
        <div style="font-family:'Space Mono',monospace;background:rgba(99,102,241,0.1);
        border-radius:12px;padding:16px;text-align:center;font-size:1.1rem;margin:16px 0;color:#a78bfa;">
            BMI = weight (kg) ÷ height² (m²)
        </div>
    </div>
    <div class="glass-card">
        <div class="section-label">About the ML Models</div>
        <p style="font-size:0.88rem;line-height:1.8;color:#d1d5db;">
        🤖 <strong>Health Risk Classifier</strong> — Random Forest with 200 decision trees,
        trained on 4,000 synthetic profiles using clinically-grounded risk thresholds (BMI bands,
        age, activity level, gender). Outputs Low / Medium / High risk with probability scores.<br><br>
        📈 <strong>BMI Trajectory Forecaster</strong> — Gradient Boosting Regressor pre-trained on
        500 synthetic BMI time series. Uses rolling averages and momentum to extrapolate your trend
        up to 30 days ahead from your session history.
        </p>
    </div>
    <div class="glass-card">
        <div class="section-label">Limitations</div>
        <p style="font-size:0.88rem;line-height:1.8;color:#d1d5db;">
        ⚠️ BMI ignores fat vs muscle mass, ethnicity, and bone density.<br>
        ⚠️ The ML models are trained on <em>synthetic</em> data — not a clinical dataset.<br>
        ⚠️ All outputs are <strong>educational only</strong>. Always consult a healthcare professional.
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;margin-top:48px;font-family:'Space Mono',monospace;
font-size:0.65rem;color:#374151;letter-spacing:2px;">
    BMI UNIVERSE · FOR EDUCATIONAL USE ONLY · NOT MEDICAL ADVICE
</div>
""", unsafe_allow_html=True)
