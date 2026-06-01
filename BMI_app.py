import streamlit as st
import math
import time
import random

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

/* Animated starfield background */
.stApp {
    background: radial-gradient(ellipse at 20% 50%, #1a0a2e 0%, #0a0a14 60%),
                radial-gradient(ellipse at 80% 20%, #0d1a2e 0%, transparent 50%);
    min-height: 100vh;
}

/* Hero title */
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

/* Card containers */
.glass-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 28px 32px;
    margin: 16px 0;
    backdrop-filter: blur(12px);
}

/* BMI Result big display */
.bmi-display {
    text-align: center;
    padding: 32px 0 20px;
}

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

/* Category color themes */
.cat-underweight { color: #38bdf8; }
.cat-normal      { color: #4ade80; }
.cat-overweight  { color: #fbbf24; }
.cat-obese       { color: #f87171; }

/* Progress bar custom */
.bmi-bar-wrap {
    margin: 20px 0;
    position: relative;
}

.bmi-bar-track {
    height: 10px;
    border-radius: 999px;
    background: linear-gradient(90deg, #38bdf8 0%, #4ade80 30%, #fbbf24 65%, #f87171 100%);
    position: relative;
    opacity: 0.7;
}

.bmi-bar-needle {
    position: absolute;
    top: -5px;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: white;
    box-shadow: 0 0 12px rgba(255,255,255,0.8);
    transform: translateX(-50%);
    transition: left 0.8s cubic-bezier(.34,1.56,.64,1);
}

/* Fun fact box */
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

/* Planet badge */
.planet-badge {
    display: inline-block;
    font-size: 3.5rem;
    animation: float 3s ease-in-out infinite;
    margin: 0 auto;
    display: block;
    text-align: center;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-10px); }
}

/* Metric pills */
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

/* Streamlit widget overrides */
div[data-testid="stSlider"] > div {
    padding: 4px 0;
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
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.4) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.6) !important;
}

/* History table */
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

/* Tabs override */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent !important;
}

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

hr { border-color: rgba(255,255,255,0.06) !important; }

/* Divider style */
.section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #4b5563;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)


# ── Helper functions ──────────────────────────────────────────────────────────

def calculate_bmi(weight_kg, height_m):
    return weight_kg / (height_m ** 2)

def get_category(bmi):
    if bmi < 18.5:
        return "Underweight", "cat-underweight", "🪐"
    elif bmi < 25:
        return "Normal", "cat-normal", "🌍"
    elif bmi < 30:
        return "Overweight", "cat-overweight", "🌙"
    else:
        return "Obese", "cat-obese", "☄️"

def bmi_needle_percent(bmi):
    """Map BMI 10–45 to 0–100% for the gradient bar."""
    clamped = max(10, min(45, bmi))
    return (clamped - 10) / 35 * 100

def ideal_weight_range(height_m):
    low  = 18.5 * (height_m ** 2)
    high = 24.9 * (height_m ** 2)
    return low, high

def calories_tdee(weight_kg, height_cm, age, gender, activity):
    if gender == "Male":
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
    else:
        bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    factors = {"Sedentary": 1.2, "Light": 1.375, "Moderate": 1.55, "Active": 1.725, "Very Active": 1.9}
    return bmr * factors[activity]

FUN_FACTS = [
    "💡 BMI was invented by Belgian mathematician Adolphe Quetelet in the 1830s — it's nearly 200 years old!",
    "🚀 On the Moon, you'd weigh ~16.5% of your Earth weight — everyone would be 'underweight' there!",
    "🏋️ Many elite athletes have a BMI in the 'overweight' range due to high muscle mass.",
    "🧬 BMI doesn't distinguish between fat, muscle, or bone — it's just weight vs. height.",
    "🌍 The average global BMI has risen ~1 unit per decade since 1975.",
    "🐘 An elephant's BMI equivalent would be astronomically high — nature disagrees with charts.",
    "⚡ Small changes make big differences: losing just 5–10% of body weight can significantly improve health markers.",
    "🎯 A 1 km daily walk can help maintain a stable BMI over time.",
]

MOTIVATIONAL = {
    "Underweight": [
        "Your body is asking for a little more fuel — nourish it with love 🌱",
        "Small, consistent gains make a universe of difference 🌟",
        "Focus on nutrient-dense foods — quality over quantity ✨",
    ],
    "Normal": [
        "You're in the sweet spot — keep riding this orbit! 🌍",
        "Balance is your superpower — maintain the momentum 🚀",
        "Stellar work! Keep those healthy habits locked in 🔐",
    ],
    "Overweight": [
        "Every journey starts with a single step — you've got this 💪",
        "Small lifestyle shifts compound into massive change ⚡",
        "Be kind to yourself — progress over perfection 🌙",
    ],
    "Obese": [
        "Your health journey is valid — every positive choice matters 💙",
        "Speak with a healthcare professional for a personalized plan 🩺",
        "Change is possible; it begins with today's choices 🌅",
    ],
}

# ── Session state ─────────────────────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []
if "streak" not in st.session_state:
    st.session_state.streak = 0

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<h1 class="hero-title">BMI UNIVERSE</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">Body Mass Index · Health Explorer</p>', unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🚀 Calculate", "📊 History", "ℹ️ About BMI"])

# ══════════════════════════════════════════════════════════════
# TAB 1 — CALCULATE
# ══════════════════════════════════════════════════════════════
with tab1:

    st.markdown('<div class="section-label">Unit System</div>', unsafe_allow_html=True)
    unit = st.radio("", ["Metric (kg / m)", "Imperial (lbs / ft & in)"], horizontal=True, label_visibility="collapsed")

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
            ft = st.number_input("📏 Height (ft)", min_value=1, max_value=8, value=5, step=1)
            inch = st.number_input("+ inches", min_value=0, max_value=11, value=9, step=1)
            height_m = (ft * 12 + inch) * 0.0254

    with st.expander("🔬 Advanced Inputs (for TDEE & extras)", expanded=False):
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            age = st.number_input("Age", min_value=10, max_value=120, value=25)
        with col_b:
            gender = st.selectbox("Gender", ["Male", "Female", "Prefer not to say"])
        with col_c:
            activity = st.selectbox("Activity Level", ["Sedentary", "Light", "Moderate", "Active", "Very Active"])

    st.markdown("")
    calc_btn = st.button("✦ CALCULATE MY BMI ✦")

    if calc_btn:
        if height_m < 0.5 or weight_kg < 1:
            st.error("Please enter valid weight and height values.")
        else:
            bmi = calculate_bmi(weight_kg, height_m)
            category, css_class, planet = get_category(bmi)
            needle_pct = bmi_needle_percent(bmi)
            ideal_low, ideal_high = ideal_weight_range(height_m)
            motivation = random.choice(MOTIVATIONAL[category])
            fun_fact = random.choice(FUN_FACTS)

            # Save to history
            st.session_state.history.append({
                "bmi": round(bmi, 1),
                "category": category,
                "weight": round(weight_kg, 1),
                "height": round(height_m, 2),
            })
            st.session_state.streak += 1

            # ── Result card ──
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

            # ── Metric pills ──
            height_cm = height_m * 100
            st.markdown(f"""
            <div style="text-align:center;margin:8px 0 16px;">
                <span class="metric-pill">⚖️ {weight_kg:.1f} kg</span>
                <span class="metric-pill">📏 {height_cm:.0f} cm</span>
                <span class="metric-pill">🎯 Ideal: {ideal_low:.1f}–{ideal_high:.1f} kg</span>
            </div>
            """, unsafe_allow_html=True)

            # ── TDEE if advanced inputs ──
            if gender in ["Male", "Female"]:
                tdee = calories_tdee(weight_kg, height_cm, age, gender, activity)
                st.markdown(f"""
                <div style="text-align:center;margin-bottom:16px;">
                    <span class="metric-pill">🔥 TDEE: {tdee:.0f} kcal/day</span>
                </div>
                """, unsafe_allow_html=True)

            # ── Motivation ──
            st.markdown(f'<div class="fun-fact">💬 {motivation}</div>', unsafe_allow_html=True)

            # ── Fun fact ──
            st.markdown(f'<div class="fun-fact">{fun_fact}</div>', unsafe_allow_html=True)

            # ── Confetti effect for Normal range ──
            if category == "Normal":
                st.balloons()

            # ── WHO scale reference ──
            st.markdown('<div class="section-label" style="margin-top:24px;">WHO BMI Scale</div>', unsafe_allow_html=True)
            scale_data = {
                "Severely Underweight": "< 16.0",
                "Underweight": "16 – 18.4",
                "Normal": "18.5 – 24.9",
                "Overweight": "25 – 29.9",
                "Obese Class I": "30 – 34.9",
                "Obese Class II": "35 – 39.9",
                "Obese Class III": "≥ 40",
            }
            for k, v in scale_data.items():
                is_current = k.lower() in category.lower() or (k == "Normal" and category == "Normal")
                highlight = "background:rgba(99,102,241,0.12);border-radius:8px;padding:2px 8px;" if is_current else ""
                st.markdown(
                    f'<div style="display:flex;justify-content:space-between;'
                    f'font-family:Space Mono,monospace;font-size:0.78rem;padding:6px 0;'
                    f'border-bottom:1px solid rgba(255,255,255,0.04);">'
                    f'<span style="{highlight}">{k}</span>'
                    f'<span style="color:#6366f1;">{v}</span></div>',
                    unsafe_allow_html=True
                )

# ══════════════════════════════════════════════════════════════
# TAB 2 — HISTORY
# ══════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-label">Your BMI Log</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.markdown("""
        <div class="glass-card" style="text-align:center;padding:48px 32px;">
            <div style="font-size:3rem;">🌌</div>
            <div style="font-family:'Space Mono',monospace;color:#4b5563;font-size:0.85rem;margin-top:12px;">
                No calculations yet.<br>Head to the Calculate tab to begin your journey.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Chart with st.line_chart
        bmi_values = [h["bmi"] for h in st.session_state.history]
        if len(bmi_values) > 1:
            st.markdown('<div class="section-label">BMI Trend</div>', unsafe_allow_html=True)
            import pandas as pd
            df = pd.DataFrame({"BMI": bmi_values})
            st.line_chart(df, color="#a78bfa", height=180)

        st.markdown('<div class="section-label">Log Entries</div>', unsafe_allow_html=True)
        for i, h in enumerate(reversed(st.session_state.history), 1):
            cat_colors = {"Underweight": "#38bdf8", "Normal": "#4ade80",
                          "Overweight": "#fbbf24", "Obese": "#f87171"}
            color = cat_colors.get(h["category"], "#9ca3af")
            st.markdown(
                f'<div class="history-row">'
                f'<span>#{len(st.session_state.history) - i + 1}</span>'
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
# TAB 3 — ABOUT BMI
# ══════════════════════════════════════════════════════════════
with tab3:
    st.markdown("""
    <div class="glass-card">
        <div class="section-label">What is BMI?</div>
        <p style="font-size:0.9rem;line-height:1.8;color:#d1d5db;">
        Body Mass Index (BMI) is a simple numerical value calculated from a person's
        <strong>weight</strong> and <strong>height</strong>. It provides a general
        screening tool to identify weight categories that may lead to health problems.
        </p>
        <div style="font-family:'Space Mono',monospace;background:rgba(99,102,241,0.1);
        border-radius:12px;padding:16px;text-align:center;font-size:1.1rem;margin:16px 0;
        color:#a78bfa;">
            BMI = weight (kg) ÷ height² (m²)
        </div>
    </div>

    <div class="glass-card">
        <div class="section-label">Limitations</div>
        <p style="font-size:0.88rem;line-height:1.8;color:#d1d5db;">
        ⚠️ BMI does <strong>not</strong> distinguish between fat and muscle mass.<br>
        ⚠️ It does <strong>not</strong> account for age, sex, ethnicity, or bone density.<br>
        ⚠️ Athletes may appear <strong>overweight</strong> due to high muscle mass.<br>
        ⚠️ Always consult a <strong>healthcare professional</strong> for a full assessment.
        </p>
    </div>

    <div class="glass-card">
        <div class="section-label">Better Indicators to Combine with BMI</div>
        <p style="font-size:0.88rem;line-height:1.8;color:#d1d5db;">
        🔬 Waist-to-hip ratio<br>
        🔬 Body fat percentage (DEXA scan)<br>
        🔬 Blood pressure & lipid panels<br>
        🔬 Visceral fat measurement
        </p>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:48px;font-family:'Space Mono',monospace;
font-size:0.65rem;color:#374151;letter-spacing:2px;">
    BMI UNIVERSE · FOR EDUCATIONAL USE ONLY · NOT MEDICAL ADVICE
</div>
""", unsafe_allow_html=True)