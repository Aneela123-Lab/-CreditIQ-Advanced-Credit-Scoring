import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import warnings
import io
from datetime import datetime

warnings.filterwarnings("ignore")

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="CreditIQ — Advanced Credit Scoring",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {
    color: #e0e0f0 !important;
}

/* ── Header banner ── */
.header-banner {
    background: linear-gradient(90deg, #6c63ff, #3ecf8e);
    padding: 2rem 2.5rem;
    border-radius: 18px;
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 32px rgba(108,99,255,0.3);
}
.header-banner h1 {
    color: #fff;
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0;
}
.header-banner p {
    color: rgba(255,255,255,0.85);
    margin: 0.4rem 0 0 0;
    font-size: 1rem;
}

/* ── Metric cards ── */
.metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    text-align: center;
    backdrop-filter: blur(10px);
}
.metric-card .metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.55);
    margin-bottom: 0.3rem;
}
.metric-card .metric-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: #fff;
}
.metric-card .metric-sub { font-size: 0.8rem; color: rgba(255,255,255,0.45); }

/* ── Result card ── */
.result-good {
    background: linear-gradient(135deg, rgba(62,207,142,0.15), rgba(62,207,142,0.05));
    border: 1.5px solid #3ecf8e;
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
}
.result-bad {
    background: linear-gradient(135deg, rgba(255,90,90,0.15), rgba(255,90,90,0.05));
    border: 1.5px solid #ff5a5a;
    border-radius: 18px;
    padding: 2rem;
    text-align: center;
}
.result-title { font-size: 1.6rem; font-weight: 700; color: #fff; margin-bottom: 0.3rem; }
.result-sub { font-size: 0.95rem; color: rgba(255,255,255,0.65); }

/* ── Section headers ── */
.section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #c9c4ff;
    border-bottom: 1px solid rgba(108,99,255,0.3);
    padding-bottom: 0.5rem;
    margin-bottom: 1rem;
}

/* ── Risk badge ── */
.badge-low    { background:#3ecf8e33; color:#3ecf8e; border:1px solid #3ecf8e; }
.badge-medium { background:#f5a62333; color:#f5a623; border:1px solid #f5a623; }
.badge-high   { background:#ff5a5a33; color:#ff5a5a; border:1px solid #ff5a5a; }
.risk-badge {
    display:inline-block; padding:0.3rem 0.9rem; border-radius:999px;
    font-size:0.85rem; font-weight:600; letter-spacing:0.04em;
}

/* ── Inputs ── */
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.9) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 8px !important;
    color: #000 !important;
}
[data-testid="stSelectbox"] select {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 8px !important;
    color: #fff !important;
}

/* Global text */
.stMarkdown, p, label, .stText { color: #e0e0f0 !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background: rgba(255,255,255,0.04);
    border-radius: 12px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: rgba(255,255,255,0.6) !important;
    font-weight: 500;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg, #6c63ff, #3ecf8e) !important;
    color: #fff !important;
}

/* ── Primary button ── */
[data-testid="baseButton-primary"] {
    background: linear-gradient(90deg, #6c63ff, #3ecf8e) !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    color: #fff !important;
    padding: 0.6rem 2rem !important;
    box-shadow: 0 4px 20px rgba(108,99,255,0.35) !important;
    transition: all 0.2s !important;
}
[data-testid="baseButton-secondary"] {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #fff !important;
    font-weight: 500 !important;
}

/* ── Expander ── */
.streamlit-expanderHeader { color: #c9c4ff !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA MAPS  (German Credit Dataset labels)
# ─────────────────────────────────────────────
CHECKING_ACCOUNT = {
    1: "< 0 DM  (Negative / No account)",
    2: "0 – 200 DM",
    3: "≥ 200 DM  (Well funded)",
    4: "No checking account",
}
CREDIT_HISTORY = {
    0: "No credits / all paid back duly",
    1: "All credits at this bank paid back duly",
    2: "Existing credits paid back duly till now",
    3: "Delay in paying off in the past",
    4: "Critical account / other credits existing",
}
PURPOSE = {
    0:  "Car (new)", 1:  "Car (used)", 2:  "Furniture / equipment",
    3:  "Radio / television", 4:  "Domestic appliances",
    5:  "Repairs", 6:  "Education", 7:  "Vacation",
    8:  "Retraining", 9:  "Business", 10: "Others",
}
SAVINGS = {
    1: "< 100 DM", 2: "100–500 DM",
    3: "500–1000 DM", 4: "≥ 1000 DM", 5: "Unknown / no savings",
}
EMPLOYMENT = {
    1: "Unemployed", 2: "< 1 year",
    3: "1–4 years", 4: "4–7 years", 5: "≥ 7 years",
}
INSTALLMENT_RATE = {1: "≥ 35 %", 2: "25–35 %", 3: "20–25 %", 4: "< 20 %"}
PERSONAL_STATUS  = {
    1: "Male – divorced / separated",
    2: "Female – divorced / separated / married",
    3: "Male – single",
    4: "Male – married / widowed",
}
GUARANTORS  = {1: "None", 2: "Co-applicant", 3: "Guarantor"}
RESIDENCE   = {1: "< 1 year", 2: "1–4 years", 3: "4–7 years", 4: "≥ 7 years"}
PROPERTY    = {1: "Real estate", 2: "Savings / life insurance", 3: "Car / other", 4: "Unknown / no property"}
OTHER_PLANS = {1: "Bank", 2: "Stores", 3: "None"}
HOUSING     = {1: "Rent", 2: "Own", 3: "For free"}
EXISTING_CREDITS = {1: "1", 2: "2", 3: "3–4", 4: "≥ 5"}
JOB = {
    1: "Unemployed / unskilled – non-resident",
    2: "Unskilled – resident",
    3: "Skilled employee / official",
    4: "Management / self-employed / highly qualified",
}
MAINTENANCE = {1: "3 or more", 2: "0 to 2"}
TELEPHONE   = {1: "None", 2: "Yes, registered"}
FOREIGN     = {1: "Yes", 2: "No"}

FEATURE_LABELS = {
    "laufkont":  "Checking Account Status",
    "laufzeit":  "Duration (months)",
    "moral":     "Credit History",
    "verw":      "Purpose",
    "hoehe":     "Credit Amount (DM)",
    "sparkont":  "Savings Account / Bonds",
    "beszeit":   "Employment Since",
    "rate":      "Installment Rate",
    "famges":    "Personal Status & Sex",
    "buerge":    "Guarantors",
    "wohnzeit":  "Residence Since",
    "verm":      "Property",
    "alter":     "Age (years)",
    "weitkred":  "Other Instalment Plans",
    "wohn":      "Housing",
    "bishkred":  "Existing Credits at Bank",
    "beruf":     "Job",
    "pers":      "Maintenance Liability",
    "telef":     "Telephone",
    "gastarb":   "Foreign Worker",
}

FEATURE_IMPORTANCES = {
    "laufkont": 0.1613, "hoehe": 0.0874, "laufzeit": 0.0836,
    "moral":    0.0783, "alter":  0.0772, "verm":    0.0624,
    "sparkont": 0.0590, "beszeit":0.0562, "verw":    0.0512,
    "rate":     0.0430, "wohnzeit":0.0406,"famges":  0.0370,
    "beruf":    0.0351, "weitkred":0.0259,"bishkred":0.0236,
    "wohn":     0.0230, "telef":  0.0207, "buerge":  0.0174,
    "pers":     0.0106, "gastarb":0.0062,
}

# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load("credit_scoring_model.joblib")

@st.cache_data
def load_dataset():
    return pd.read_csv("german_credit_data.csv")

model = load_model()
df_ref = load_dataset()

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
RISK_THRESHOLDS = {
    "Low":    (0.75, 1.01),
    "Medium": (0.45, 0.75),
    "High":   (0.00, 0.45),
}

def compute_credit_score(prob_good: float) -> int:
    """Map probability to a 300–850 credit score (FICO-like)."""
    return int(300 + (prob_good ** 0.7) * 550)

def risk_tier(prob_good: float) -> str:
    if prob_good >= 0.75: return "Low"
    if prob_good >= 0.45: return "Medium"
    return "High"

def badge_html(tier: str) -> str:
    cls = {"Low": "badge-low", "Medium": "badge-medium", "High": "badge-high"}[tier]
    icons = {"Low": "✅", "Medium": "⚠️", "High": "❌"}
    return f'<span class="risk-badge {cls}">{icons[tier]} {tier} Risk</span>'

def gauge_chart(score: int) -> go.Figure:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 40, "color": "#ffffff", "family": "Inter"}},
        gauge={
            "axis": {"range": [300, 850], "tickcolor": "#888", "tickfont": {"color": "#aaa"}},
            "bar":  {"color": "#6c63ff", "thickness": 0.25},
            "bgcolor": "rgba(0,0,0,0)",
            "bordercolor": "rgba(255,255,255,0.1)",
            "steps": [
                {"range": [300, 500], "color": "rgba(255,90,90,0.25)"},
                {"range": [500, 650], "color": "rgba(245,166,35,0.25)"},
                {"range": [650, 850], "color": "rgba(62,207,142,0.25)"},
            ],
            "threshold": {
                "line": {"color": "#fff", "width": 3},
                "thickness": 0.85,
                "value": score,
            },
        },
        title={"text": "Credit Score", "font": {"color": "#c9c4ff", "size": 16, "family": "Inter"}},
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=60, b=10, l=20, r=20),
        height=250,
    )
    return fig

def probability_bar(prob_good: float) -> go.Figure:
    prob_bad = 1 - prob_good
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Good Credit",
        x=["Probability"],
        y=[prob_good * 100],
        marker_color="#3ecf8e",
        text=[f"{prob_good*100:.1f}%"],
        textposition="inside",
        textfont={"color": "#fff", "size": 14},
    ))
    fig.add_trace(go.Bar(
        name="Bad Credit",
        x=["Probability"],
        y=[prob_bad * 100],
        marker_color="#ff5a5a",
        text=[f"{prob_bad*100:.1f}%"],
        textposition="inside",
        textfont={"color": "#fff", "size": 14},
    ))
    fig.update_layout(
        barmode="stack",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#fff",
        font_family="Inter",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font={"size": 11}),
        margin=dict(t=30, b=10, l=0, r=0),
        height=130,
        xaxis=dict(showgrid=False, visible=False),
        yaxis=dict(showgrid=False, range=[0, 100], visible=False),
    )
    return fig

def feature_importance_chart() -> go.Figure:
    fi = sorted(FEATURE_IMPORTANCES.items(), key=lambda x: x[1])
    names  = [FEATURE_LABELS[k] for k, _ in fi]
    values = [v for _, v in fi]
    colors = [f"rgba(108,99,255,{0.4 + v*4:.2f})" for v in values]
    fig = go.Figure(go.Bar(
        x=values, y=names,
        orientation="h",
        marker_color=colors,
        marker_line_width=0,
        text=[f"{v*100:.1f}%" for v in values],
        textposition="outside",
        textfont={"color": "#aaa", "size": 10},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ddd",
        font_family="Inter",
        margin=dict(t=10, b=10, l=10, r=60),
        height=460,
        xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.07)", visible=False),
        yaxis=dict(showgrid=False, tickfont={"size": 11}),
    )
    return fig

def dataset_distribution() -> go.Figure:
    counts = df_ref["kredit"].value_counts().reset_index()
    counts.columns = ["class", "count"]
    counts["label"] = counts["class"].map({1: "Good Credit", 0: "Bad Credit"})
    fig = px.pie(counts, names="label", values="count",
                 color="label",
                 color_discrete_map={"Good Credit": "#3ecf8e", "Bad Credit": "#ff5a5a"},
                 hole=0.55)
    fig.update_traces(textfont_size=13, textfont_color="#fff")
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ddd",
        font_family="Inter",
        legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
        margin=dict(t=10, b=20, l=0, r=0),
        height=260,
    )
    return fig

def age_credit_scatter() -> go.Figure:
    fig = px.scatter(
        df_ref, x="alter", y="hoehe",
        color=df_ref["kredit"].map({1: "Good Credit", 0: "Bad Credit"}),
        opacity=0.5, size_max=8,
        color_discrete_map={"Good Credit": "#3ecf8e", "Bad Credit": "#ff5a5a"},
        labels={"alter": "Age", "hoehe": "Credit Amount (DM)", "color": "Outcome"},
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ddd", font_family="Inter",
        legend_title_text="",
        margin=dict(t=10, b=10, l=10, r=10),
        height=260,
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
    )
    return fig

def duration_distribution() -> go.Figure:
    good = df_ref[df_ref["kredit"] == 1]["laufzeit"]
    bad  = df_ref[df_ref["kredit"] == 0]["laufzeit"]
    fig = go.Figure()
    fig.add_trace(go.Histogram(x=good, name="Good Credit", marker_color="#3ecf8e", opacity=0.7, nbinsx=20))
    fig.add_trace(go.Histogram(x=bad,  name="Bad Credit",  marker_color="#ff5a5a", opacity=0.7, nbinsx=20))
    fig.update_layout(
        barmode="overlay",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ddd", font_family="Inter",
        margin=dict(t=10, b=10, l=10, r=10),
        height=260,
        xaxis=dict(title="Duration (months)", gridcolor="rgba(255,255,255,0.07)"),
        yaxis=dict(title="Count", gridcolor="rgba(255,255,255,0.07)"),
        legend=dict(orientation="h", yanchor="top", y=1.15, xanchor="right", x=1),
    )
    return fig

def risk_factors_radar(input_dict: dict) -> go.Figure:
    """Normalised radar chart of the 8 most important features for the current applicant."""
    top_feats = ["laufkont", "hoehe", "laufzeit", "moral", "alter", "verm", "sparkont", "beszeit"]
    # Normalise each to 0-1 (0=worst, 1=best for credit)
    norms = {
        "laufkont":  (input_dict["laufkont"] - 1) / 3,
        "hoehe":     1 - min(input_dict["hoehe"] / 18000, 1),
        "laufzeit":  1 - min(input_dict["laufzeit"] / 72, 1),
        "moral":     input_dict["moral"] / 4,
        "alter":     min((input_dict["alter"] - 19) / 56, 1),
        "verm":      (input_dict["verm"] - 1) / 3,
        "sparkont":  min((int(input_dict["sparkont"]) - 1) / 4, 1),
        "beszeit":   min((int(input_dict["beszeit"]) - 1) / 4, 1),
    }
    labels = [FEATURE_LABELS[f] for f in top_feats]
    values = [norms[f] for f in top_feats]
    values += [values[0]]
    labels += [labels[0]]

    fig = go.Figure(go.Scatterpolar(
        r=values, theta=labels, fill="toself",
        line_color="#6c63ff",
        fillcolor="rgba(108,99,255,0.2)",
        marker=dict(color="#6c63ff", size=6),
    ))
    fig.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, range=[0, 1], showticklabels=False,
                            gridcolor="rgba(255,255,255,0.1)", linecolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(gridcolor="rgba(255,255,255,0.1)", linecolor="rgba(255,255,255,0.1)",
                             tickfont=dict(color="#ccc", size=10)),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font_family="Inter", font_color="#ddd",
        margin=dict(t=30, b=30, l=40, r=40),
        height=300,
    )
    return fig

def predict_batch(df: pd.DataFrame):
    """Run model on a cleaned dataframe and return augmented results."""
    feature_cols = list(FEATURE_LABELS.keys())
    df_in = df[[c for c in feature_cols if c in df.columns]].copy()
    proba  = model.predict_proba(df_in)[:, 1]
    pred   = model.predict(df_in)
    scores = [compute_credit_score(p) for p in proba]
    tiers  = [risk_tier(p) for p in proba]
    out = df_in.copy()
    out["prediction"]   = ["Good" if p == 1 else "Bad" for p in pred]
    out["prob_good"]    = (proba * 100).round(1)
    out["credit_score"] = scores
    out["risk_tier"]    = tiers
    return out

# ─────────────────────────────────────────────
# SIDEBAR – Config & Summary Statistics
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🏦 CreditIQ")
    st.markdown("**Advanced Credit Scoring Tool**")
    st.markdown("---")

    st.markdown("#### ⚙️ Model Info")
    st.markdown(f"- **Algorithm:** Random Forest (200 trees)")
    st.markdown(f"- **Training Set:** German Credit [{len(df_ref)} records]")
    st.markdown(f"- **Features:** {len(FEATURE_LABELS)}")
    st.markdown("---")

    total  = len(df_ref)
    n_good = int((df_ref["kredit"] == 1).sum())
    n_bad  = int((df_ref["kredit"] == 0).sum())
    st.markdown("#### 📊 Dataset Statistics")
    st.markdown(f"- **Good Credit:** {n_good} ({n_good/total*100:.0f}%)")
    st.markdown(f"- **Bad Credit:** {n_bad} ({n_bad/total*100:.0f}%)")
    st.markdown(f"- **Avg Age:** {df_ref['alter'].mean():.0f} yrs")
    st.markdown(f"- **Avg Amount:** {df_ref['hoehe'].mean():,.0f} DM")
    st.markdown(f"- **Avg Duration:** {df_ref['laufzeit'].mean():.0f} months")
    st.markdown("---")

    # Quick threshold tuner
    st.markdown("#### 🎚️ Decision Threshold")
    threshold = st.slider(
        "Classify as 'Good' if P(good) ≥",
        min_value=0.30, max_value=0.90,
        value=0.50, step=0.05,
        help="Lower = more approvals; Higher = more conservative lending.",
    )
    st.caption(f"Current threshold: **{threshold:.0%}**")
    st.markdown("---")
    st.markdown("<small style='color:#666'>© 2025 CreditIQ Analytics</small>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
    <h1>🏦 CreditIQ — Advanced Credit Scoring</h1>
    <p>AI-powered credit risk assessment platform · German Credit Dataset · Random Forest Model</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAIN TABS
# ─────────────────────────────────────────────
tab_single, tab_batch, tab_analytics, tab_guide = st.tabs([
    "🔍 Single Applicant",
    "📂 Batch Scoring",
    "📈 Analytics Dashboard",
    "📖 Feature Guide",
])

# ══════════════════════════════════════════════
# TAB 1 – SINGLE APPLICANT
# ══════════════════════════════════════════════
with tab_single:
    st.markdown('<div class="section-header">📋 Applicant Details</div>', unsafe_allow_html=True)
    col_form, col_result = st.columns([1.1, 0.9], gap="large")

    with col_form:
        with st.expander("🤵 Personal Information", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                alter = st.slider("Age", 19, 75, 35)
                famges_label = st.selectbox("Personal Status & Sex", list(PERSONAL_STATUS.values()), index=2)
                famges = [k for k, v in PERSONAL_STATUS.items() if v == famges_label][0]
                wohn_label = st.selectbox("Housing", list(HOUSING.values()), index=1)
                wohn = [k for k, v in HOUSING.items() if v == wohn_label][0]
            with c2:
                wohnzeit_label = st.selectbox("Residence Since", list(RESIDENCE.values()), index=2)
                wohnzeit = [k for k, v in RESIDENCE.items() if v == wohnzeit_label][0]
                gastarb_label = st.selectbox("Foreign Worker", list(FOREIGN.values()), index=1)
                gastarb = [k for k, v in FOREIGN.items() if v == gastarb_label][0]
                pers_label = st.selectbox("Maintenance Liability", list(MAINTENANCE.values()), index=1)
                pers = [k for k, v in MAINTENANCE.items() if v == pers_label][0]
                telef_label = st.selectbox("Telephone", list(TELEPHONE.values()), index=0)
                telef = [k for k, v in TELEPHONE.items() if v == telef_label][0]

        with st.expander("💰 Financial & Employment", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                laufkont_label = st.selectbox("Checking Account", list(CHECKING_ACCOUNT.values()), index=0)
                laufkont = [k for k, v in CHECKING_ACCOUNT.items() if v == laufkont_label][0]
                sparkont_label = st.selectbox("Savings Account / Bonds", list(SAVINGS.values()), index=0)
                sparkont = [k for k, v in SAVINGS.items() if v == sparkont_label][0]
                verm_label = st.selectbox("Property / Assets", list(PROPERTY.values()), index=0)
                verm = [k for k, v in PROPERTY.items() if v == verm_label][0]
            with c2:
                beruf_label = st.selectbox("Job Type", list(JOB.values()), index=2)
                beruf = [k for k, v in JOB.items() if v == beruf_label][0]
                beszeit_label = st.selectbox("Employment Since", list(EMPLOYMENT.values()), index=2)
                beszeit = [k for k, v in EMPLOYMENT.items() if v == beszeit_label][0]

        with st.expander("📑 Loan & Credit History", expanded=True):
            c1, c2 = st.columns(2)
            with c1:
                hoehe = st.number_input("Credit Amount (DM)", 250, 20000, 3000, step=100)
                laufzeit = st.slider("Duration (months)", 4, 72, 24)
                moral_label = st.selectbox("Credit History", list(CREDIT_HISTORY.values()), index=2)
                moral = [k for k, v in CREDIT_HISTORY.items() if v == moral_label][0]
                verw_label = st.selectbox("Loan Purpose", list(PURPOSE.values()), index=2)
                verw = [k for k, v in PURPOSE.items() if v == verw_label][0]
            with c2:
                rate_label = st.selectbox("Installment Rate (% of income)", list(INSTALLMENT_RATE.values()), index=3)
                rate = [k for k, v in INSTALLMENT_RATE.items() if v == rate_label][0]
                weitkred_label = st.selectbox("Other Instalment Plans", list(OTHER_PLANS.values()), index=2)
                weitkred = [k for k, v in OTHER_PLANS.items() if v == weitkred_label][0]
                bishkred_label = st.selectbox("Existing Credits at Bank", list(EXISTING_CREDITS.values()), index=0)
                bishkred = [k for k, v in EXISTING_CREDITS.items() if v == bishkred_label][0]
                buerge_label = st.selectbox("Guarantors / Co-applicant", list(GUARANTORS.values()), index=0)
                buerge = [k for k, v in GUARANTORS.items() if v == buerge_label][0]

        predict_btn = st.button("⚡ Assess Credit Risk", type="primary", use_container_width=True)

    # ── Results column ──────────────────────────
    with col_result:
        input_dict = {
            "laufkont": laufkont, "laufzeit": laufzeit, "moral": moral,
            "verw": verw, "hoehe": hoehe, "sparkont": sparkont,
            "beszeit": beszeit, "rate": rate, "famges": famges,
            "buerge": buerge, "wohnzeit": wohnzeit, "verm": verm,
            "alter": alter, "weitkred": weitkred, "wohn": wohn,
            "bishkred": bishkred, "beruf": beruf, "pers": pers,
            "telef": telef, "gastarb": gastarb,
        }

        if predict_btn:
            df_in = pd.DataFrame([input_dict])
            try:
                proba  = model.predict_proba(df_in)[0]
                prob_good = proba[1]
                prob_bad  = proba[0]

                # Apply custom threshold
                prediction = "Good" if prob_good >= threshold else "Bad"
                score      = compute_credit_score(prob_good)
                tier       = risk_tier(prob_good)

                # Store in session state
                st.session_state["last_result"]    = prediction
                st.session_state["last_prob_good"] = prob_good
                st.session_state["last_score"]     = score
                st.session_state["last_tier"]      = tier
                st.session_state["last_input"]     = input_dict

            except Exception as e:
                st.error(f"Prediction failed: {e}")

        # Display results if available
        if "last_result" in st.session_state:
            r       = st.session_state["last_result"]
            pg      = st.session_state["last_prob_good"]
            score   = st.session_state["last_score"]
            tier    = st.session_state["last_tier"]
            inp     = st.session_state["last_input"]
            div_cls = "result-good" if r == "Good" else "result-bad"
            icon    = "✅" if r == "Good" else "❌"
            color   = "#3ecf8e" if r == "Good" else "#ff5a5a"

            st.markdown(f"""
            <div class="{div_cls}">
                <div style="font-size:3rem">{icon}</div>
                <div class="result-title">{r} Credit Risk</div>
                <div class="result-sub">Threshold: {threshold:.0%} · Model confidence shown below</div>
            </div>""", unsafe_allow_html=True)

            st.markdown(f'<div style="text-align:center;margin-top:0.6rem">{badge_html(tier)}</div>',
                        unsafe_allow_html=True)

            # Gauge
            st.plotly_chart(gauge_chart(score), use_container_width=True, config={"displayModeBar": False})

            # Probability bar
            st.plotly_chart(probability_bar(pg), use_container_width=True, config={"displayModeBar": False})

            # KPI tiles
            k1, k2, k3 = st.columns(3)
            with k1:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-label">Credit Score</div>
                    <div class="metric-value">{score}</div>
                    <div class="metric-sub">300 – 850 scale</div>
                </div>""", unsafe_allow_html=True)
            with k2:
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-label">P(Good Credit)</div>
                    <div class="metric-value" style="color:{color}">{pg*100:.1f}%</div>
                    <div class="metric-sub">Model probability</div>
                </div>""", unsafe_allow_html=True)
            with k3:
                tier_color = {"Low": "#3ecf8e", "Medium": "#f5a623", "High": "#ff5a5a"}[tier]
                st.markdown(f"""<div class="metric-card">
                    <div class="metric-label">Risk Tier</div>
                    <div class="metric-value" style="color:{tier_color}">{tier}</div>
                    <div class="metric-sub">Based on probability</div>
                </div>""", unsafe_allow_html=True)

            st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

            # Radar profile
            st.markdown('<div class="section-header" style="margin-top:1rem">🕸️ Applicant Risk Profile</div>',
                        unsafe_allow_html=True)
            st.plotly_chart(risk_factors_radar(inp), use_container_width=True, config={"displayModeBar": False})

            # Recommendations
            st.markdown('<div class="section-header">💡 Recommendations</div>', unsafe_allow_html=True)
            recs = []
            if inp["laufkont"] in [1, 2]:
                recs.append("🔴 **Checking account** balance is low — a significant risk indicator.")
            if inp["laufzeit"] > 36:
                recs.append("🟡 **Loan duration** exceeds 3 years — increases default risk.")
            if inp["moral"] in [3, 4]:
                recs.append("🔴 **Credit history** shows past delays or critical accounts.")
            if inp["hoehe"] > 10000:
                recs.append("🟡 **High credit amount** requested — verify income sufficiency.")
            if inp["sparkont"] == 1:
                recs.append("🟡 **Savings** are below 100 DM — limited financial buffer.")
            if inp["alter"] < 25:
                recs.append("🟡 **Young applicant** (< 25) — limited credit history expected.")
            if r == "Good" and not recs:
                recs.append("🟢 Strong applicant profile across all key indicators.")
            for rec in (recs or ["🟢 No major risk flags detected."]):
                st.markdown(f"- {rec}")

            # Exportable summary
            with st.expander("📥 Download Assessment Report"):
                now = datetime.now().strftime("%Y-%m-%d %H:%M")
                report_lines = [
                    f"CreditIQ Assessment Report — {now}",
                    "=" * 50,
                    f"Decision:       {r} Credit Risk",
                    f"Risk Tier:      {tier}",
                    f"Credit Score:   {score} / 850",
                    f"P(Good Credit): {pg*100:.2f}%",
                    f"Threshold Used: {threshold:.0%}",
                    "",
                    "── Applicant Profile ──",
                ]
                for k, v in inp.items():
                    report_lines.append(f"  {FEATURE_LABELS.get(k, k):<30}: {v}")
                report_lines += ["", "── Recommendations ──"]
                report_lines += [f"  {r}" for r in recs]
                report_text = "\n".join(report_lines)
                st.download_button(
                    "⬇️ Download .txt Report",
                    data=report_text,
                    file_name=f"credit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True,
                )

        else:
            st.markdown("""
            <div style="border:2px dashed rgba(108,99,255,0.3);border-radius:16px;
                        padding:3rem 2rem;text-align:center;margin-top:1rem;color:rgba(255,255,255,0.4)">
                <div style="font-size:3rem">🔍</div>
                <div style="font-size:1.1rem;font-weight:600;margin-top:0.5rem">
                    Fill in applicant details and click<br>"Assess Credit Risk"
                </div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════
# TAB 2 – BATCH SCORING
# ══════════════════════════════════════════════
with tab_batch:
    st.markdown('<div class="section-header">📂 Batch Applicant Scoring</div>', unsafe_allow_html=True)
    st.markdown("Upload a **CSV file** with the same 20 feature columns as the German Credit dataset. "
                "The tool will score every row and let you download the results.")

    # Template download
    template_df = pd.DataFrame(columns=list(FEATURE_LABELS.keys()))
    buf = io.StringIO()
    template_df.to_csv(buf, index=False)
    st.download_button(
        "⬇️ Download CSV Template",
        data=buf.getvalue(),
        file_name="credit_scoring_template.csv",
        mime="text/csv",
    )

    uploaded = st.file_uploader("Upload applicants CSV", type=["csv"])
    if uploaded:
        try:
            df_upload = pd.read_csv(uploaded)
            st.success(f"Loaded **{len(df_upload)} rows** · {df_upload.shape[1]} columns")
            st.dataframe(df_upload.head(5), use_container_width=True)

            if st.button("⚡ Score All Applicants", type="primary"):
                with st.spinner("Scoring applicants…"):
                    results_df = predict_batch(df_upload)

                st.markdown("---")
                st.markdown(f"### Results — {len(results_df)} applicants scored")

                # Summary stats
                n_good_b = int((results_df["prediction"] == "Good").sum())
                n_bad_b  = int((results_df["prediction"] == "Bad").sum())
                avg_sc   = int(results_df["credit_score"].mean())
                avg_pg   = results_df["prob_good"].mean()

                a, b, c, d = st.columns(4)
                for col, label, val, sub in [
                    (a, "Total Applicants", len(results_df), ""),
                    (b, "Approved (Good)", n_good_b, f"{n_good_b/len(results_df)*100:.0f}%"),
                    (c, "Flagged (Bad)", n_bad_b, f"{n_bad_b/len(results_df)*100:.0f}%"),
                    (d, "Avg Credit Score", avg_sc, f"Avg P(good): {avg_pg:.1f}%"),
                ]:
                    with col:
                        st.markdown(f"""<div class="metric-card">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{val}</div>
                            <div class="metric-sub">{sub}</div>
                        </div>""", unsafe_allow_html=True)

                st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

                # Risk tier breakdown
                tier_counts = results_df["risk_tier"].value_counts().reset_index()
                tier_counts.columns = ["tier", "count"]
                tier_fig = px.bar(
                    tier_counts, x="tier", y="count",
                    color="tier",
                    color_discrete_map={"Low": "#3ecf8e", "Medium": "#f5a623", "High": "#ff5a5a"},
                    title="Risk Tier Distribution",
                )
                tier_fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    font_color="#ddd", font_family="Inter", showlegend=False,
                    xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
                    yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
                    margin=dict(t=40, b=10, l=10, r=10), height=250,
                )
                st.plotly_chart(tier_fig, use_container_width=True, config={"displayModeBar": False})

                # Scrollable results table
                st.dataframe(
                    results_df[["prediction", "prob_good", "credit_score", "risk_tier"] +
                               list(FEATURE_LABELS.keys()[:5])],
                    use_container_width=True,
                )

                # Download
                dl_buf = io.StringIO()
                results_df.to_csv(dl_buf, index=False)
                st.download_button(
                    "⬇️ Download Full Results CSV",
                    data=dl_buf.getvalue(),
                    file_name=f"batch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True,
                    type="primary",
                )
        except Exception as e:
            st.error(f"Error processing file: {e}")

# ══════════════════════════════════════════════
# TAB 3 – ANALYTICS DASHBOARD
# ══════════════════════════════════════════════
with tab_analytics:
    st.markdown('<div class="section-header">📈 Dataset Insights & Model Analytics</div>',
                unsafe_allow_html=True)

    # Row 1
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.markdown("##### 🥧 Credit Outcome Distribution")
        st.plotly_chart(dataset_distribution(), use_container_width=True, config={"displayModeBar": False})
    with r1c2:
        st.markdown("##### 📊 Loan Duration by Outcome")
        st.plotly_chart(duration_distribution(), use_container_width=True, config={"displayModeBar": False})

    # Row 2
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.markdown("##### 🔵 Age vs Credit Amount")
        st.plotly_chart(age_credit_scatter(), use_container_width=True, config={"displayModeBar": False})
    with r2c2:
        st.markdown("##### 📦 Credit Amount Distribution")
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(
            y=df_ref[df_ref["kredit"] == 1]["hoehe"], name="Good Credit",
            marker_color="#3ecf8e", line_color="#3ecf8e",
        ))
        fig_box.add_trace(go.Box(
            y=df_ref[df_ref["kredit"] == 0]["hoehe"], name="Bad Credit",
            marker_color="#ff5a5a", line_color="#ff5a5a",
        ))
        fig_box.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font_color="#ddd", font_family="Inter",
            yaxis=dict(title="Credit Amount (DM)", gridcolor="rgba(255,255,255,0.07)"),
            xaxis=dict(showgrid=False),
            margin=dict(t=10, b=10, l=10, r=10), height=260,
            legend=dict(orientation="h", yanchor="top", y=1.15, x=1, xanchor="right"),
        )
        st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})

    # Row 3 – Feature Importance (full width)
    st.markdown("##### 🎯 Feature Importance (Random Forest)")
    st.plotly_chart(feature_importance_chart(), use_container_width=True, config={"displayModeBar": False})

    # Checking account breakdown
    st.markdown("##### 🏦 Checking Account Status vs Credit Outcome")
    check_df = df_ref.groupby(["laufkont", "kredit"]).size().reset_index(name="count")
    check_df["laufkont_label"] = check_df["laufkont"].map(CHECKING_ACCOUNT)
    check_df["outcome"]        = check_df["kredit"].map({1: "Good", 0: "Bad"})
    fig_check = px.bar(
        check_df, x="laufkont_label", y="count", color="outcome", barmode="group",
        color_discrete_map={"Good": "#3ecf8e", "Bad": "#ff5a5a"},
        labels={"laufkont_label": "Checking Account Status", "count": "Applicants"},
    )
    fig_check.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font_color="#ddd", font_family="Inter",
        xaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        yaxis=dict(gridcolor="rgba(255,255,255,0.07)"),
        legend_title_text="Outcome",
        margin=dict(t=10, b=10, l=10, r=10), height=300,
    )
    st.plotly_chart(fig_check, use_container_width=True, config={"displayModeBar": False})

# ══════════════════════════════════════════════
# TAB 4 – FEATURE GUIDE
# ══════════════════════════════════════════════
with tab_guide:
    st.markdown('<div class="section-header">📖 Feature Reference Guide</div>', unsafe_allow_html=True)
    st.markdown("Each feature below corresponds to a column in the German Credit Dataset. "
                "The **Impact** column shows the feature's relative importance in the model.")

    guide_rows = []
    for feat, label in FEATURE_LABELS.items():
        imp = FEATURE_IMPORTANCES[feat]
        stars = "🔴 High" if imp >= 0.07 else ("🟡 Medium" if imp >= 0.04 else "🟢 Low")
        guide_rows.append({
            "Column": feat,
            "Feature Name": label,
            "Importance (%)": f"{imp*100:.2f}",
            "Impact Level": stars,
        })
    guide_df = pd.DataFrame(guide_rows).sort_values("Importance (%)", ascending=False).reset_index(drop=True)
    st.dataframe(guide_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("#### 📚 Value Mappings")

    with st.expander("Checking Account Status (laufkont)"):
        for k, v in CHECKING_ACCOUNT.items():
            st.markdown(f"- **{k}** → {v}")
    with st.expander("Credit History (moral)"):
        for k, v in CREDIT_HISTORY.items():
            st.markdown(f"- **{k}** → {v}")
    with st.expander("Loan Purpose (verw)"):
        for k, v in PURPOSE.items():
            st.markdown(f"- **{k}** → {v}")
    with st.expander("Savings Account (sparkont)"):
        for k, v in SAVINGS.items():
            st.markdown(f"- **{k}** → {v}")
    with st.expander("Employment Since (beszeit)"):
        for k, v in EMPLOYMENT.items():
            st.markdown(f"- **{k}** → {v}")
    with st.expander("Property / Assets (verm)"):
        for k, v in PROPERTY.items():
            st.markdown(f"- **{k}** → {v}")
    with st.expander("Personal Status & Sex (famges)"):
        for k, v in PERSONAL_STATUS.items():
            st.markdown(f"- **{k}** → {v}")
    with st.expander("Housing (wohn)"):
        for k, v in HOUSING.items():
            st.markdown(f"- **{k}** → {v}")
    with st.expander("Job Type (beruf)"):
        for k, v in JOB.items():
            st.markdown(f"- **{k}** → {v}")
