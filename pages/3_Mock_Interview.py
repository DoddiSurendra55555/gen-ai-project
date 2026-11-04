
import html
import streamlit as st

from utils.helpers import (
    initialize_session_state,
    render_sidebar,
)

from utils.ai_engine import evaluate_answer
from utils.browser_voice import browser_voice


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Mock Interview",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="collapsed",
)

initialize_session_state()
render_sidebar()


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "processed_voice_event_ids" not in st.session_state:
    st.session_state["processed_voice_event_ids"] = []


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
    background: linear-gradient(115deg, #172554, #1e40af, #2563eb);
    border-radius: 22px;
    padding: 38px;
    margin-bottom: 30px;
    box-shadow: 0 14px 35px rgba(37,99,235,0.15);
}

.hero-label {
    display: inline-block;
    background: rgba(255,255,255,0.13);
    border: 1px solid rgba(255,255,255,0.25);
    color: #dbeafe !important;
    padding: 9px 15px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.3px;
    margin-bottom: 17px;
}

.hero-title {
    color: #ffffff !important;
    font-size: clamp(30px, 4vw, 42px);
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: -1px;
    margin-bottom: 13px;
}

.hero-description {
    color: #dbeafe !important;
    font-size: 14px;
    line-height: 1.9;
    max-width: 760px;
}

.hero-points {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 20px;
}

.hero-point {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    color: #ffffff !important;
    border-radius: 30px;
    padding: 8px 13px;
    font-size: 12px;
    font-weight: 600;
}

/* Section headings */

.section-eyebrow {
    color: #2563eb !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}

.section-title {
    color: #172554 !important;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin-bottom: 8px;
}

.section-description {
    color: #64748b !important;
    font-size: 14px;
    line-height: 1.8;
    margin-bottom: 18px;
}

/* Information cards */

.info-card {
    background: linear-gradient(135deg, #eff6ff, #f8faff);
    border: 1px solid #dbeafe;
    border-radius: 15px;
    padding: 19px;
    min-height: 105px;
    margin-bottom: 15px;
}

.info-label {
    color: #64748b !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 10px;
}

.info-value {
    color: #172554 !important;
    font-size: 17px;
    font-weight: 800;
    overflow-wrap: anywhere;
}

/* General panels */

.light-panel {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 17px;
    padding: 23px;
    margin: 17px 0;
}

.panel-title {
    color: #172554 !important;
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 9px;
}

.panel-description {
    color: #64748b !important;
    font-size: 13px;
    line-height: 1.9;
}

/* Question */

.question-panel {
    background: linear-gradient(135deg, #eff6ff, #f8faff);
    border: 1px solid #bfdbfe;
    border-left: 5px solid #2563eb;
    border-radius: 17px;
    padding: 27px;
    margin: 18px 0 20px;
}

.question-label {
    color: #2563eb !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin-bottom: 15px;
}

.question-text {
    color: #172554 !important;
    font-size: 21px;
    font-weight: 750;
    line-height: 1.7;
    overflow-wrap: anywhere;
}

/* Voice area */

.voice-panel {
    background: #f0f6ff;
    border: 1px solid #bfdbfe;
    border-radius: 17px;
    padding: 23px;
    margin: 18px 0;
}

.voice-heading {
    color: #172554 !important;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 8px;
}

.voice-description {
    color: #64748b !important;
    font-size: 13px;
    line-height: 1.8;
}

/* Progress */

.progress-panel {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 15px;
    padding: 19px;
    margin: 17px 0;
}

.progress-label {
    color: #64748b !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.progress-value {
    color: #172554 !important;
    font-size: 20px;
    font-weight: 800;
}

/* Evaluation cards */

.evaluation-panel {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 15px;
    padding: 20px;
    margin: 13px 0;
}

.evaluation-heading {
    color: #172554 !important;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 10px;
}

.evaluation-score {
    display: inline-block;
    background: #dbeafe;
    color: #1d4ed8 !important;
    border-radius: 9px;
    padding: 7px 12px;
    font-size: 13px;
    font-weight: 800;
}

/* Text and controls */

.stApp,
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #172554;
}

[data-testid="stWidgetLabel"] {
    color: #172554 !important;
}

.stTextArea textarea,
.stTextInput input {
    background: #ffffff !important;
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
    border: 1px solid #bfdbfe !important;
    caret-color: #2563eb !important;
}

/* Buttons */

.stButton > button {
    min-height: 47px;
    border-radius: 11px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button[kind="primary"] {
    background: #2563eb !important;
    color: #ffffff !important;
    border: 1px solid #2563eb !important;
}

.stButton > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
    transform: translateY(-1px);
}

.stButton > button[kind="primary"] p {
    color: #ffffff !important;
}

.stButton > button:not([kind="primary"]) {
    background: #ffffff !important;
    color: #2563eb !important;
    border: 1px solid #bfdbfe !important;
}

/* Expanders */

[data-testid="stExpander"] {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 13px;
}

[data-testid="stExpander"] summary {
    color: #172554 !important;
    font-weight: 700;
}

/* Alerts */

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Progress bar */

[data-testid="stProgressBar"] > div > div {
    background: #2563eb !important;
}

/* Responsive */

@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1.2rem 1rem 2rem;
    }

    .hero-panel {
        padding: 26px 21px;
    }

    .hero-title {
        font-size: 29px;
    }

    .question-panel {
        padding: 20px;
    }

    .question-text {
        font-size: 18px;
    }

    .light-panel {
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
        STEP 03 &nbsp; • &nbsp; LIVE INTERVIEW PRACTICE
    </div>

    <div class="hero-title">
        Your Interview Starts Here.<br>
        Speak With Confidence.
    </div>

    <div class="hero-description">
        Experience a personalized mock interview powered by AI.
        Listen to each question, answer naturally using your
        microphone, and receive instant feedback from Gemini.
    </div>

    <div class="hero-points">
        <div class="hero-point">✓ Voice-Based Interview</div>
        <div class="hero-point">✓ Live Transcription</div>
        <div class="hero-point">✓ AI Answer Evaluation</div>
    </div>
</div>
""")


# ---------------------------------------------------------
# CHECK INTERVIEW SETUP
# ---------------------------------------------------------

questions = st.session_state.get("interview_questions", [])

if not questions:

    st.html("""
    <div class="light-panel">
        <div class="panel-title">📋 Interview Setup Required</div>
        <div class="panel-description">
            You have not generated interview questions yet.
            Complete Interview Setup first to begin your
            personalized mock interview.
        </div>
    </div>
    """)

    if st.button(
        "Go to Interview Setup →",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/2_Interview_Setup.py")

    st.stop()


# ---------------------------------------------------------
# INTERVIEW INFORMATION
# ---------------------------------------------------------

st.html("""
<div class="section-eyebrow">YOUR SESSION</div>
<div class="section-title">Interview Information</div>
<div class="section-description">
Review your selected interview settings before practising.
</div>
""")

information = [
    (
        "💼 JOB ROLE",
        st.session_state.get("job_role") or "Not selected",
    ),
    (
        "🎯 INTERVIEW TYPE",
        st.session_state.get("interview_type") or "Not selected",
    ),
    (
        "📈 DIFFICULTY",
        st.session_state.get("difficulty") or "Not selected",
    ),
]

columns = st.columns(3)

for column, (label, value) in zip(columns, information):

    safe_label = html.escape(str(label))
    safe_value = html.escape(str(value))

    with column:
        st.html(f"""
        <div class="info-card">
            <div class="info-label">{safe_label}</div>
            <div class="info-value">{safe_value}</div>
        </div>
        """)


st.divider()


# ---------------------------------------------------------
# START INTERVIEW
# ---------------------------------------------------------

if not st.session_state.get("interview_started"):

    st.html("""
    <div class="light-panel">
        <div class="panel-title">🎤 Ready to Begin Your Interview?</div>
        <div class="panel-description">
            Your interview questions will be read aloud by your
            browser. Use your microphone to answer, review the
            transcription, and submit it for Gemini evaluation.
            You can also edit your transcription before submitting.
        </div>
    </div>
    """)

    st.write(
        f"Your interview contains **{len(questions)} questions**."
    )

    if st.button(
        "▶️ Start Interview",
        type="primary",
        use_container_width=True,
    ):

        st.session_state["interview_started"] = True
        st.session_state["current_question_index"] = 0
        st.session_state["user_answers"] = []
        st.session_state["answer_evaluations"] = []
        st.session_state["interview_completed"] = False
        st.session_state["processed_voice_event_ids"] = []

        st.rerun()

    st.stop()


# ---------------------------------------------------------
# CHECK INTERVIEW COMPLETION
# ---------------------------------------------------------

current_index = st.session_state["current_question_index"]

if current_index >= len(questions):

    st.session_state["interview_completed"] = True

    st.html("""
    <div class="hero-panel">
        <div class="hero-label">INTERVIEW COMPLETED</div>
        <div class="hero-title">🎉 Excellent Work!</div>
        <div class="hero-description">
            You have completed all your interview questions.
            Your answers have been evaluated. Your performance
            report is now ready.
        </div>
    </div>
    """)

    st.success(
        "Congratulations! You have completed all interview questions."
    )

    st.write(
        "View your scores, feedback, strengths, and areas "
        "for improvement in your final interview report."
    )

    if st.button(
        "📊 View Interview Results",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/4_Interview_Results.py")

    st.stop()


# ---------------------------------------------------------
# INTERVIEW PROGRESS
# ---------------------------------------------------------

total_questions = len(questions)

answered_questions = len(
    st.session_state["answer_evaluations"]
)

progress = min(
    answered_questions / total_questions,
    1.0,
)

st.html("""
<div class="section-eyebrow">LIVE SESSION</div>
<div class="section-title">Your Interview Progress</div>
""")

st.progress(progress)

progress_col1, progress_col2 = st.columns(2)

with progress_col1:
    st.html(f"""
    <div class="progress-panel">
        <div class="progress-label">QUESTIONS COMPLETED</div>
        <div class="progress-value">
            {answered_questions} / {total_questions}
        </div>
    </div>
    """)

with progress_col2:
    st.html(f"""
    <div class="progress-panel">
        <div class="progress-label">CURRENT QUESTION</div>
        <div class="progress-value">
            {current_index + 1} / {total_questions}
        </div>
    </div>
    """)

st.divider()


# ---------------------------------------------------------
# CURRENT QUESTION
# ---------------------------------------------------------

current_question = questions[current_index]

question_text = str(
    current_question.get("question", "")
)

question_category = html.escape(
    str(current_question.get("category", "General"))
)

safe_question_text = html.escape(question_text)

st.html(f"""
<div class="section-eyebrow">LISTEN CAREFULLY AND ANSWER</div>
<div class="section-title">Current Interview Question</div>

<div class="question-panel">
    <div class="question-label">
        QUESTION {current_index + 1:02d}
        &nbsp; • &nbsp;
        {question_category}
    </div>

    <div class="question-text">
        {safe_question_text}
    </div>
</div>
""")

st.caption(
    "Your browser reads the question aloud automatically. "
    "You can use the Repeat Question button if needed."
)


# ---------------------------------------------------------
# BROWSER VOICE COMPONENT
# ---------------------------------------------------------

st.html("""
<div class="voice-panel">
    <div class="voice-heading">🎙️ Your Spoken Answer</div>
    <div class="voice-description">
        Start speaking using your microphone. Your words will
        appear as editable text. Review your answer and press
        Enter or use the Submit button when you are ready.
    </div>
</div>
""")

voice_result = browser_voice(
    question=question_text,
    key=f"voice_interview_question_{current_index}",
)


# ---------------------------------------------------------
# PROCESS SUBMITTED ANSWER
# ---------------------------------------------------------

if voice_result and voice_result.get("submitted"):

    user_answer = voice_result.get("transcript", "").strip()

    event_id = voice_result.get("event_id")

    processed_events = st.session_state[
        "processed_voice_event_ids"
    ]

    if event_id not in processed_events:

        if not user_answer:

            st.error(
                "No answer was received. Please speak or type "
                "an answer before submitting."
            )

        else:

            try:

                with st.spinner(
                    "Gemini is evaluating your answer. Please wait..."
                ):

                    evaluation = evaluate_answer(
                        question=question_text,
                        answer=user_answer,
                        resume_analysis=st.session_state.get(
                            "resume_analysis",
                            {},
                        ),
                    )

                # Prevent duplicate evaluation.

                processed_events.append(event_id)

                # Save answer and evaluation.

                st.session_state["user_answers"].append(
                    user_answer
                )

                st.session_state["answer_evaluations"].append(
                    evaluation
                )

                # Move to the next question.

                st.session_state["current_question_index"] += 1

                st.rerun()

            except ValueError as error:

                st.error(str(error))

            except RuntimeError as error:

                st.error(str(error))

            except Exception:

                st.error(
                    "An unexpected error occurred while evaluating "
                    "your answer. Please try submitting again."
                )


# ---------------------------------------------------------
# PREVIOUS ANSWER EVALUATIONS
# ---------------------------------------------------------

if st.session_state["answer_evaluations"]:

    st.divider()

    st.html("""
    <div class="section-eyebrow">YOUR PERFORMANCE SO FAR</div>
    <div class="section-title">Previous Answer Evaluations</div>
    <div class="section-description">
        Review the feedback Gemini provided for your previous answers.
    </div>
    """)

    evaluations = st.session_state["answer_evaluations"]
    answers = st.session_state["user_answers"]

    for index, evaluation in enumerate(evaluations):

        score = evaluation.get("score", 0)

        with st.expander(
            f"Question {index + 1}  |  Score: {score}/100"
        ):

            st.markdown("**Your Answer**")

            st.write(answers[index])

            st.markdown("**Answer Score**")

            st.metric(
                "Score",
                f"{score}/100",
            )

            st.markdown("**Feedback**")

            st.write(
                evaluation.get(
                    "feedback",
                    "No feedback available.",
                )
            )

            st.markdown("**Strengths**")

            strengths = evaluation.get("strengths", [])

            if strengths:
                for item in strengths:
                    st.markdown(f"- {item}")
            else:
                st.caption("No strengths provided.")

            st.markdown("**Areas for Improvement**")

            improvements = evaluation.get("improvements", [])

            if improvements:
                for item in improvements:
                    st.markdown(f"- {item}")
            else:
                st.caption("No improvements provided.")

            st.markdown("**Example of a Stronger Answer**")

            st.write(
                evaluation.get(
                    "ideal_answer",
                    "No example answer available.",
                )
            )
