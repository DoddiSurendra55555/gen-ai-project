
import streamlit as st

from utils.helpers import initialize_session_state, render_sidebar


st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed",
)

initialize_session_state()
render_sidebar()


# ---------------------------------------------------------
# PROFESSIONAL CSS
# ---------------------------------------------------------

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #ffffff;
    font-family: 'Inter', sans-serif;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1320px;
    padding: 2rem 2.5rem 3rem;
}

.hero-badge {
    display: inline-block;
    background: #eff6ff;
    color: #2563eb;
    border: 1px solid #dbeafe;
    padding: 10px 17px;
    border-radius: 30px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 22px;
}

.hero-heading {
    color: #172554;
    font-size: clamp(40px, 5vw, 65px);
    font-weight: 800;
    line-height: 1.12;
    letter-spacing: -2px;
    margin-bottom: 20px;
}

.hero-heading span {
    color: #2563eb;
}

.hero-description {
    color: #64748b;
    font-size: 17px;
    line-height: 1.85;
    margin-bottom: 20px;
}

.hero-trust {
    color: #64748b;
    font-size: 13px;
    line-height: 2;
    margin-top: 15px;
}

.section-eyebrow {
    text-align: center;
    color: #2563eb;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.8px;
    margin-bottom: 10px;
}

.section-heading {
    color: #172554;
    text-align: center;
    font-size: 35px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 10px;
}

.section-subtitle {
    color: #64748b;
    text-align: center;
    font-size: 15px;
    line-height: 1.8;
    margin-bottom: 35px;
}

.stats-panel {
    background: linear-gradient(115deg, #172554, #2563eb);
    border-radius: 20px;
    padding: 32px 20px;
    margin: 25px 0 55px;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}

.stat-number {
    color: #ffffff;
    font-size: 29px;
    font-weight: 800;
    text-align: center;
}

.stat-label {
    color: #dbeafe;
    font-size: 13px;
    text-align: center;
    margin-top: 7px;
}

.feature-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 17px;
    padding: 25px;
    min-height: 190px;
    box-shadow: 0 6px 22px rgba(30, 64, 175, 0.06);
}

.feature-icon {
    width: 48px;
    height: 48px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 13px;
    background: #eff6ff;
    font-size: 24px;
    margin-bottom: 17px;
}

.feature-title {
    font-size: 18px;
    font-weight: 750;
    color: #172554;
    margin-bottom: 10px;
}

.feature-description {
    font-size: 14px;
    color: #64748b;
    line-height: 1.7;
}

.workflow-card {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 15px;
    padding: 22px;
    min-height: 175px;
}

.workflow-number {
    color: #2563eb;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 13px;
}

.workflow-title {
    color: #172554;
    font-size: 17px;
    font-weight: 750;
    margin-bottom: 9px;
}

.workflow-description {
    color: #64748b;
    font-size: 13px;
    line-height: 1.7;
}

.preparation-heading {
    color: #172554;
    font-size: 30px;
    font-weight: 800;
    line-height: 1.3;
}

.preparation-description {
    color: #64748b;
    font-size: 15px;
    line-height: 1.9;
}

.preparation-list {
    color: #2563eb;
    font-size: 14px;
    font-weight: 700;
    line-height: 2.1;
}

.cta-panel {
    background: linear-gradient(120deg, #172554, #2563eb);
    border-radius: 20px;
    padding: 38px;
    margin: 30px 0 25px;
}

.cta-heading {
    color: #ffffff;
    font-size: 29px;
    font-weight: 800;
    margin-bottom: 10px;
}

.cta-description {
    color: #dbeafe;
    font-size: 15px;
    line-height: 1.8;
}

.privacy-panel {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 22px;
    margin-top: 25px;
}

.privacy-title {
    color: #172554;
    font-size: 16px;
    font-weight: 750;
    margin-bottom: 8px;
}

.privacy-description {
    color: #64748b;
    font-size: 13px;
    line-height: 1.8;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    padding: 30px 0 10px;
}

[data-testid="stImage"] img {
    border-radius: 20px;
    box-shadow: 0 15px 40px rgba(30, 64, 175, 0.12);
}

.stButton > button {
    min-height: 48px;
    border-radius: 10px;
    font-weight: 700;
}

.stButton > button[kind="primary"] {
    background: #2563eb !important;
    color: white !important;
    border: 1px solid #2563eb !important;
}

.stButton > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
}

.stButton > button[kind="primary"] p {
    color: white !important;
}

.stButton > button:not([kind="primary"]) {
    background: white !important;
    color: #2563eb !important;
    border: 1px solid #bfdbfe !important;
}

@media (max-width: 700px) {
    .stats-panel {
        grid-template-columns: 1fr;
    }
}
</style>
""")


# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

hero_left, hero_right = st.columns(
    [1.05, 1],
    gap="large",
    vertical_alignment="center",
)

with hero_left:

    st.html("""
    <div class="hero-badge">✨ AI-POWERED INTERVIEW PREPARATION</div>
    <div class="hero-heading">
        Your Personal<br>
        AI-Powered<br>
        <span>Interview Coach</span>
    </div>
    <div class="hero-description">
        Turn interview anxiety into confidence. Prepare with
        personalized questions, intelligent resume analysis,
        and instant AI-powered feedback designed to help you
        perform at your best.
    </div>
    """)

    if st.button(
        "Get Started Free  →",
        type="primary",
        use_container_width=True,
        key="hero_start",
    ):
        st.switch_page("pages/1_Resume_Analysis.py")

    st.html("""
    <div class="hero-trust">
        ✓ Resume-based questions &nbsp;&nbsp; ✓ Intelligent feedback<br>
        ✓ Personalized preparation &nbsp;&nbsp; ✓ Performance tracking
    </div>
    """)

with hero_right:

    st.image(
        "https://images.unsplash.com/photo-1551836022-d5d88e9218df?auto=format&fit=crop&w=1400&q=90",
        use_container_width=True,
    )


# ---------------------------------------------------------
# STATISTICS
# ---------------------------------------------------------

st.html("""
<div class="stats-panel">
    <div>
        <div class="stat-number">AI</div>
        <div class="stat-label">Intelligent Resume Analysis</div>
    </div>
    <div>
        <div class="stat-number">24/7</div>
        <div class="stat-label">Practice Whenever You Want</div>
    </div>
    <div>
        <div class="stat-number">360°</div>
        <div class="stat-label">Complete Interview Preparation</div>
    </div>
</div>
""")


# ---------------------------------------------------------
# FEATURES
# ---------------------------------------------------------

st.html("""
<div class="section-eyebrow">EVERYTHING YOU NEED</div>
<div class="section-heading">Your Complete Interview Toolkit</div>
<div class="section-subtitle">
One platform to analyse your resume, practise interviews,
improve your answers, and track your progress.
</div>
""")

features = [
    (
        "📄",
        "Smart Resume Analysis",
        "Upload your resume and let AI analyse your skills, education, projects, experience, strengths, and areas for improvement.",
        "Explore Resume Analysis →",
        "pages/1_Resume_Analysis.py",
    ),
    (
        "⚙️",
        "Personalized Interview Setup",
        "Select your target job role, interview type, difficulty level, and question count to build a personalized interview session.",
        "Configure Interview →",
        "pages/2_Interview_Setup.py",
    ),
    (
        "🎤",
        "Interactive Mock Interview",
        "Practise answering personalized interview questions and receive detailed AI-powered evaluation and feedback.",
        "Start Mock Interview →",
        "pages/3_Mock_Interview.py",
    ),
    (
        "📊",
        "Detailed Performance Report",
        "Explore your interview scores, strengths, improvement areas, and personalized recommendations.",
        "View Performance →",
        "pages/4_Interview_Results.py",
    ),
]

for start in (0, 2):

    columns = st.columns(2, gap="large")

    for column, feature in zip(columns, features[start:start + 2]):

        with column:

            st.html(f"""
            <div class="feature-card">
                <div class="feature-icon">{feature[0]}</div>
                <div class="feature-title">{feature[1]}</div>
                <div class="feature-description">{feature[2]}</div>
            </div>
            """)

            if st.button(
                feature[3],
                key=f"feature_{start}_{feature[0]}",
                use_container_width=True,
            ):
                st.switch_page(feature[4])

    st.write("")


# ---------------------------------------------------------
# HOW IT WORKS
# ---------------------------------------------------------

st.html("""
<div class="section-eyebrow">YOUR JOURNEY STARTS HERE</div>
<div class="section-heading">How It Works</div>
<div class="section-subtitle">
Follow four simple steps to prepare for your next interview.
</div>
""")

steps = [
    ("01", "📄", "Upload Your Resume",
     "Upload your PDF resume so the AI can understand your profile."),
    ("02", "⚙️", "Set Your Preferences",
     "Choose your job role, interview type, and difficulty."),
    ("03", "🎤", "Practise Your Interview",
     "Answer personalized questions and receive instant feedback."),
    ("04", "📈", "Review Your Results",
     "Understand your performance and discover how to improve."),
]

step_columns = st.columns(4, gap="medium")

for column, step in zip(step_columns, steps):

    with column:

        st.html(f"""
        <div class="workflow-card">
            <div class="workflow-number">STEP {step[0]} &nbsp; {step[1]}</div>
            <div class="workflow-title">{step[2]}</div>
            <div class="workflow-description">{step[3]}</div>
        </div>
        """)


# ---------------------------------------------------------
# PREPARATION SECTION
# ---------------------------------------------------------

st.write("")

image_column, text_column = st.columns(
    [0.9, 1.1],
    gap="large",
    vertical_alignment="center",
)

with image_column:

    st.image(
        "https://images.unsplash.com/photo-1521737711867-e3b97375f902?auto=format&fit=crop&w=1200&q=85",
        use_container_width=True,
    )

with text_column:

    st.html("""
    <div class="section-eyebrow" style="text-align:left">
        PREPARE WITH CONFIDENCE
    </div>
    <div class="preparation-heading">
        Every great interview starts with great preparation.
    </div>
    <div class="preparation-description">
        Build confidence through structured practice.
        Understand your strengths, identify areas to improve,
        and learn how to present your skills effectively.
    </div>
    <div class="preparation-list">
        ✓ Understand your resume<br>
        ✓ Practise role-specific questions<br>
        ✓ Improve your answers<br>
        ✓ Track your interview performance
    </div>
    """)

    if st.button(
        "Begin Your Preparation →",
        type="primary",
        use_container_width=True,
        key="preparation_button",
    ):
        st.switch_page("pages/1_Resume_Analysis.py")


# ---------------------------------------------------------
# CALL TO ACTION
# ---------------------------------------------------------

st.html("""
<div class="cta-panel">
    <div class="cta-heading">
        Your next opportunity starts with preparation.
    </div>
    <div class="cta-description">
        Take the first step towards becoming a more confident
        and interview-ready candidate.
    </div>
</div>
""")

if st.button(
    "Start Preparing Now →",
    type="primary",
    use_container_width=True,
    key="bottom_start",
):
    st.switch_page("pages/1_Resume_Analysis.py")


# ---------------------------------------------------------
# PRIVACY
# ---------------------------------------------------------

st.html("""
<div class="privacy-panel">
    <div class="privacy-title">🔒 Your Privacy Matters</div>
    <div class="privacy-description">
        Your application data is maintained temporarily using
        Streamlit Session State and is not stored in a database.
        Resume and answer content may be sent to Google's Gemini
        API when you use AI-powered features. Avoid uploading
        sensitive personal information that is not needed
        for interview preparation.
    </div>
</div>
""")


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.html("""
<div class="footer">
    <strong>AI Interview Coach</strong><br>
    Practice Better. Perform Confidently.<br><br>
    © 2026 AI Interview Coach. All rights reserved.
</div>
""")
