
import html
import streamlit as st

from utils.helpers import (
    initialize_session_state,
    render_sidebar,
)

from utils.ai_engine import generate_questions


st.set_page_config(
    page_title="Interview Setup",
    page_icon="⚙️",
    layout="wide",
)

initialize_session_state()
render_sidebar()


# ---------------------------------------------------------
# PROFESSIONAL DESIGN
# ---------------------------------------------------------

st.html("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background: #ffffff;
    font-family: 'Inter', sans-serif;
    color: #172554;
}

[data-testid="stMainBlockContainer"] {
    max-width: 1320px;
    padding: 2rem 2.5rem 3rem;
}

/* Hero */

.hero-panel {
    position: relative;
    overflow: hidden;
    background: linear-gradient(115deg, #172554, #1e40af, #2563eb);
    border-radius: 22px;
    padding: 40px;
    margin-bottom: 32px;
    box-shadow: 0 14px 35px rgba(37,99,235,0.15);
}

.hero-label {
    display: inline-block;
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.25);
    color: #dbeafe !important;
    padding: 9px 16px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.3px;
    margin-bottom: 18px;
}

.hero-title {
    color: #ffffff !important;
    font-size: clamp(30px, 4vw, 43px);
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: -1.2px;
    margin-bottom: 13px;
}

.hero-description {
    color: #dbeafe !important;
    font-size: 15px;
    line-height: 1.9;
    max-width: 760px;
}

.hero-points {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 22px;
}

.hero-point {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 30px;
    color: #ffffff !important;
    font-size: 12px;
    padding: 9px 13px;
    font-weight: 600;
}

/* Headings */

.section-eyebrow {
    color: #2563eb !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.6px;
    margin-bottom: 8px;
}

.section-title {
    color: #172554 !important;
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
}

.section-description {
    color: #64748b !important;
    font-size: 14px;
    line-height: 1.8;
    margin-bottom: 20px;
}

/* Cards */

.light-card {
    background: linear-gradient(135deg, #eff6ff, #f8faff);
    border: 1px solid #dbeafe;
    border-radius: 17px;
    padding: 22px;
    margin-bottom: 17px;
}

.card-title {
    color: #172554 !important;
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 9px;
}

.card-description {
    color: #64748b !important;
    font-size: 13px;
    line-height: 1.8;
}

.resume-card {
    background: #f0f6ff;
    border: 1px solid #bfdbfe;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 25px;
}

.resume-label {
    color: #64748b !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin-bottom: 7px;
}

.resume-name {
    color: #1d4ed8 !important;
    font-size: 20px;
    font-weight: 800;
    overflow-wrap: anywhere;
}

/* Configuration */

.config-panel {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 18px;
    padding: 24px;
    margin-bottom: 20px;
}

.config-heading {
    color: #172554 !important;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 5px;
}

.config-description {
    color: #64748b !important;
    font-size: 13px;
    line-height: 1.8;
    margin-bottom: 17px;
}

/* ---------------------------------------------------------
   INPUT AND DROPDOWN TEXT VISIBILITY FIX
--------------------------------------------------------- */

/* General widget labels */

[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #172554 !important;
}

/* Text input */

.stTextInput input,
[data-baseweb="input"] input,
[data-baseweb="input"] {
    background-color: #ffffff !important;
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
    caret-color: #2563eb !important;
}

/* Text input placeholder */

.stTextInput input::placeholder,
[data-baseweb="input"] input::placeholder {
    color: #64748b !important;
    -webkit-text-fill-color: #64748b !important;
    opacity: 1 !important;
}

/* Select box container */

[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border-color: #bfdbfe !important;
}

/* Selected dropdown value */

[data-baseweb="select"] div,
[data-baseweb="select"] span,
[data-baseweb="select"] input {
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
}

/* Dropdown menu background */

[data-baseweb="popover"],
[data-baseweb="popover"] > div,
[data-baseweb="menu"],
[data-baseweb="menu"] ul {
    background-color: #ffffff !important;
}

/* Dropdown option text */

[data-baseweb="menu"] li,
[data-baseweb="menu"] li div,
[data-baseweb="menu"] li span,
[data-baseweb="option"],
[data-baseweb="option"] div,
[data-baseweb="option"] span {
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
    background-color: #ffffff;
}

/* Hovered dropdown option */

[data-baseweb="menu"] li:hover,
[data-baseweb="option"]:hover {
    background-color: #eff6ff !important;
}

/* Highlighted or selected dropdown option */

[data-baseweb="menu"] li[aria-selected="true"],
[data-baseweb="option"][aria-selected="true"] {
    background-color: #dbeafe !important;
    color: #172554 !important;
}

/* Dropdown option text remains dark */

[data-baseweb="menu"] li[aria-selected="true"] *,
[data-baseweb="option"][aria-selected="true"] * {
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
}

/* Slider */

[data-testid="stSlider"] {
    padding-top: 8px;
}

[data-testid="stSlider"] [role="slider"] {
    background: #2563eb !important;
}

/* Radio buttons */

[data-testid="stRadio"] label {
    color: #172554 !important;
}

/* Buttons */

.stButton > button,
.stFormSubmitButton > button {
    min-height: 47px;
    border-radius: 11px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {
    background: #2563eb !important;
    color: #ffffff !important;
    border: 1px solid #2563eb !important;
}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
    transform: translateY(-1px);
}

.stButton > button[kind="primary"] p,
.stFormSubmitButton > button[kind="primary"] p {
    color: #ffffff !important;
}

.stButton > button:not([kind="primary"]) {
    background: #ffffff !important;
    color: #2563eb !important;
    border: 1px solid #bfdbfe !important;
}

/* Generated questions */

.question-card {
    background: #f0f6ff;
    border: 1px solid #dbeafe;
    border-radius: 15px;
    padding: 19px;
    margin-bottom: 13px;
}

.question-number {
    color: #2563eb !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.1px;
    margin-bottom: 9px;
}

.question-category {
    color: #172554 !important;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 10px;
}

.question-text {
    color: #334155 !important;
    font-size: 14px;
    line-height: 1.8;
    overflow-wrap: anywhere;
}

.question-topics {
    color: #64748b !important;
    font-size: 12px;
    line-height: 1.8;
    margin-top: 12px;
}

/* Summary */

.summary-panel {
    background: linear-gradient(115deg, #172554, #2563eb);
    border-radius: 18px;
    padding: 25px;
    margin: 25px 0 18px;
}

.summary-label {
    color: #bfdbfe !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

.summary-title {
    color: #ffffff !important;
    font-size: 23px;
    font-weight: 800;
    margin-bottom: 12px;
}

.summary-text {
    color: #dbeafe !important;
    font-size: 14px;
    line-height: 1.9;
}

.summary-item {
    color: #ffffff !important;
    font-size: 13px;
    font-weight: 600;
    padding: 5px 0;
    overflow-wrap: anywhere;
}

/* Alerts and expanders */

[data-testid="stAlert"] {
    border-radius: 12px;
}

[data-testid="stExpander"] {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 13px;
}

[data-testid="stExpander"] summary {
    color: #172554 !important;
    font-weight: 700;
}

hr {
    border-color: #e2e8f0;
}

/* Responsive */

@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1.2rem 1rem 2rem;
    }

    .hero-panel {
        padding: 27px 22px;
    }

    .hero-title {
        font-size: 30px;
    }

    .section-title {
        font-size: 21px;
    }

    .config-panel {
        padding: 17px;
    }
}
</style>
""")


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.html("""
<div class="hero-panel">
    <div class="hero-label">
        STEP 02 &nbsp; • &nbsp; PERSONALIZED PREPARATION
    </div>

    <div class="hero-title">
        Build Your Interview.<br>
        Prepare With Confidence.
    </div>

    <div class="hero-description">
        Customize your mock interview based on your target
        job role, interview type, and experience level.
        Gemini will create personalized questions using
        your resume information.
    </div>

    <div class="hero-points">
        <div class="hero-point">✓ Role-Based Questions</div>
        <div class="hero-point">✓ Flexible Difficulty</div>
        <div class="hero-point">✓ Personalized Practice</div>
    </div>
</div>
""")


# ---------------------------------------------------------
# CHECK RESUME ANALYSIS
# ---------------------------------------------------------

if not st.session_state.get("resume_analysis"):

    st.html("""
    <div class="light-card">
        <div class="card-title">📄 Resume Analysis Required</div>
        <div class="card-description">
        Complete your resume analysis before configuring
        a personalized interview. This helps Gemini generate
        questions based on your actual skills and experience.
        </div>
    </div>
    """)

    if st.button(
        "Go to Resume Analysis →",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/1_Resume_Analysis.py")

    st.stop()


# ---------------------------------------------------------
# RESUME INFORMATION
# ---------------------------------------------------------

analysis = st.session_state["resume_analysis"]

candidate_name = html.escape(
    str(analysis.get("name") or "Candidate")
)

st.html("""
<div class="section-eyebrow">YOUR PROFILE</div>
<div class="section-title">Resume Successfully Connected</div>
<div class="section-description">
Your interview questions will be personalized using your
resume analysis.
</div>
""")

st.html(f"""
<div class="resume-card">
    <div class="resume-label">CANDIDATE PROFILE</div>
    <div class="resume-name">👤 {candidate_name}</div>
    <div class="card-description" style="margin-top:8px">
        Your resume analysis is ready for interview preparation.
    </div>
</div>
""")


# ---------------------------------------------------------
# INTERVIEW CONFIGURATION
# ---------------------------------------------------------

st.html("""
<div class="section-eyebrow">CUSTOMIZE YOUR SESSION</div>
<div class="section-title">⚙️ Interview Configuration</div>
<div class="section-description">
Choose your target position and preferred interview settings.
</div>
""")

with st.form("interview_setup_form"):

    st.markdown(
        """
        <div class="config-panel">
            <div class="config-heading">💼 Target Job Role</div>
            <div class="config-description">
                Enter the position you want to prepare for.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    job_role = st.text_input(
        "Target Job Role",
        value=st.session_state.get("job_role") or "",
        placeholder="Example: Python Developer",
        help="Enter the job role you are preparing for.",
    )

    st.markdown(
        """
        <div class="config-panel">
            <div class="config-heading">🎯 Interview Type</div>
            <div class="config-description">
                Select the style of questions you want to practise.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    interview_types = ["Technical", "Behavioral", "Mixed"]

    current_type = st.session_state.get("interview_type")

    type_index = (
        interview_types.index(current_type)
        if current_type in interview_types
        else 0
    )

    interview_type = st.selectbox(
        "Select Interview Type",
        options=interview_types,
        index=type_index,
        help="Technical focuses on technical knowledge, Behavioral on workplace experiences, and Mixed combines both.",
    )

    st.markdown(
        """
        <div class="config-panel">
            <div class="config-heading">📈 Difficulty Level</div>
            <div class="config-description">
                Choose how challenging your interview should be.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    difficulties = ["Easy", "Medium", "Hard"]

    current_difficulty = st.session_state.get("difficulty")

    difficulty_index = (
        difficulties.index(current_difficulty)
        if current_difficulty in difficulties
        else 1
    )

    difficulty = st.selectbox(
        "Select Difficulty",
        options=difficulties,
        index=difficulty_index,
        help="Easy is suitable for beginners, Medium for intermediate preparation, and Hard for advanced practice.",
    )

    st.markdown(
        """
        <div class="config-panel">
            <div class="config-heading">🔢 Number of Questions</div>
            <div class="config-description">
                Choose how many personalized questions
                Gemini should generate.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    previous_count = st.session_state.get("num_questions", 5)

    if not isinstance(previous_count, int) or not 1 <= previous_count <= 15:
        previous_count = 5

    num_questions = st.slider(
        "Choose Question Count",
        min_value=1,
        max_value=15,
        value=previous_count,
        help="You can generate between 1 and 15 interview questions.",
    )

    st.caption(
        f"You have selected {num_questions} interview questions."
    )

    submitted = st.form_submit_button(
        "✨ Generate Personalized Questions",
        type="primary",
        use_container_width=True,
    )


# ---------------------------------------------------------
# GENERATE PERSONALIZED QUESTIONS
# ---------------------------------------------------------

if submitted:

    if not job_role.strip():

        st.error("Please enter a target job role.")

    else:

        try:

            with st.spinner(
                "Gemini is preparing your personalized "
                "interview questions..."
            ):

                questions = generate_questions(
                    resume_analysis=analysis,
                    job_role=job_role.strip(),
                    interview_type=interview_type,
                    difficulty=difficulty,
                    num_questions=num_questions,
                )

            st.session_state["job_role"] = job_role.strip()
            st.session_state["interview_type"] = interview_type
            st.session_state["difficulty"] = difficulty
            st.session_state["num_questions"] = num_questions

            st.session_state["interview_questions"] = questions

            st.session_state["current_question_index"] = 0
            st.session_state["user_answers"] = []
            st.session_state["answer_evaluations"] = []
            st.session_state["final_report"] = None
            st.session_state["interview_started"] = False
            st.session_state["interview_completed"] = False

            st.success(
                f"Successfully generated {len(questions)} "
                "personalized interview questions!"
            )

        except ValueError as error:

            st.error(str(error))

        except RuntimeError as error:

            st.error(str(error))

        except Exception:

            st.error(
                "An unexpected error occurred while generating "
                "questions. Please try again."
            )


# ---------------------------------------------------------
# GENERATED QUESTION PREVIEW
# ---------------------------------------------------------

questions = st.session_state.get("interview_questions", [])

if questions:

    st.divider()

    st.html("""
    <div class="section-eyebrow">YOUR INTERVIEW IS READY</div>
    <div class="section-title">📋 Generated Interview Questions</div>
    <div class="section-description">
    Review your personalized questions before starting
    the mock interview.
    </div>
    """)

    job_summary = html.escape(
        str(st.session_state.get("job_role") or "Not specified")
    )

    type_summary = html.escape(
        str(st.session_state.get("interview_type") or "Not specified")
    )

    difficulty_summary = html.escape(
        str(st.session_state.get("difficulty") or "Not specified")
    )

    st.html(f"""
    <div class="summary-panel">
        <div class="summary-label">INTERVIEW SUMMARY</div>
        <div class="summary-title">Your Practice Session</div>
        <div class="summary-item">💼 Job Role: {job_summary}</div>
        <div class="summary-item">🎯 Interview Type: {type_summary}</div>
        <div class="summary-item">📈 Difficulty: {difficulty_summary}</div>
        <div class="summary-item">🔢 Total Questions: {len(questions)}</div>
    </div>
    """)

    for index, question_data in enumerate(questions, start=1):

        category = html.escape(
            str(question_data.get("category") or "General")
        )

        question_text = html.escape(
            str(question_data.get("question") or "No question available.")
        )

        expected_topics = question_data.get("expected_topics", [])

        safe_topics = "".join(
            f"<li>{html.escape(str(topic))}</li>"
            for topic in expected_topics
        )

        topics_html = (
            f"""
            <div class="question-topics">
                <strong>Expected topics:</strong>
                <ul>{safe_topics}</ul>
            </div>
            """
            if safe_topics
            else ""
        )

        st.html(f"""
        <div class="question-card">
            <div class="question-number">
                QUESTION {index:02d}
            </div>
            <div class="question-category">
                {category}
            </div>
            <div class="question-text">
                {question_text}
            </div>
            {topics_html}
        </div>
        """)

    st.html("""
    <div class="light-card">
        <div class="card-title">🎤 Ready to Start Practising?</div>
        <div class="card-description">
            Your personalized questions are ready.
            Continue to the Mock Interview page to begin
            answering questions using your microphone or text.
        </div>
    </div>
    """)

    if st.button(
        "Start Mock Interview →",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/3_Mock_Interview.py")
