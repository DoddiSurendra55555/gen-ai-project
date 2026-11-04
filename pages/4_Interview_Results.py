
import html
import json

import plotly.express as px
import streamlit as st

from utils.helpers import (
    initialize_session_state,
    render_sidebar,
)

from utils.ai_engine import generate_final_report


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Interview Results",
    page_icon="📊",
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
    background: linear-gradient(115deg, #172554, #1e40af, #2563eb);
    border-radius: 22px;
    padding: 40px;
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

/* Score cards */

.score-card {
    background: linear-gradient(135deg, #eff6ff, #f8faff);
    border: 1px solid #bfdbfe;
    border-radius: 17px;
    padding: 22px;
    min-height: 125px;
    margin-bottom: 16px;
}

.score-label {
    color: #64748b !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 12px;
}

.score-value {
    color: #1d4ed8 !important;
    font-size: 31px;
    font-weight: 800;
    letter-spacing: -0.8px;
}

.score-caption {
    color: #64748b !important;
    font-size: 12px;
    margin-top: 5px;
}

/* General panels */

.light-panel {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 16px;
    padding: 22px;
    margin: 16px 0;
}

.panel-title {
    color: #172554 !important;
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 10px;
}

.panel-description {
    color: #64748b !important;
    font-size: 13px;
    line-height: 1.9;
}

/* Evaluation sections */

.feedback-panel {
    background: #f0f6ff;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 19px;
    margin: 12px 0;
}

.feedback-heading {
    color: #172554 !important;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 9px;
}

.feedback-text {
    color: #475569 !important;
    font-size: 13px;
    line-height: 1.9;
    overflow-wrap: anywhere;
}

/* Final report */

.report-panel {
    background: linear-gradient(115deg, #172554, #1e40af, #2563eb);
    border-radius: 19px;
    padding: 28px;
    margin: 18px 0;
}

.report-label {
    color: #bfdbfe !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 11px;
}

.report-title {
    color: #ffffff !important;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 12px;
}

.report-text {
    color: #dbeafe !important;
    font-size: 14px;
    line-height: 1.9;
    overflow-wrap: anywhere;
}

.report-score {
    display: inline-block;
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.25);
    color: #ffffff !important;
    border-radius: 12px;
    padding: 12px 16px;
    margin-top: 16px;
    font-size: 18px;
    font-weight: 800;
}

/* Buttons */

.stButton > button,
.stDownloadButton > button {
    min-height: 47px;
    border-radius: 11px;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button[kind="primary"],
.stDownloadButton > button[kind="primary"] {
    background: #2563eb !important;
    color: #ffffff !important;
    border: 1px solid #2563eb !important;
}

.stButton > button[kind="primary"]:hover,
.stDownloadButton > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
    border-color: #1d4ed8 !important;
    transform: translateY(-1px);
}

.stButton > button[kind="primary"] p,
.stDownloadButton > button[kind="primary"] p {
    color: #ffffff !important;
}

.stButton > button:not([kind="primary"]) {
    background: #ffffff !important;
    color: #2563eb !important;
    border: 1px solid #bfdbfe !important;
}

/* General text */

.stApp,
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #172554;
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

/* Metrics */

[data-testid="stMetric"] {
    background: #f0f6ff;
    border: 1px solid #dbeafe;
    border-radius: 13px;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #64748b !important;
}

[data-testid="stMetricValue"] {
    color: #172554 !important;
}

/* Chart */

[data-testid="stPlotlyChart"] {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 15px;
    padding: 10px;
}

/* Responsive */

@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1.2rem 1rem 2rem;
    }

    .hero-panel {
        padding: 27px 21px;
    }

    .hero-title {
        font-size: 29px;
    }

    .section-title {
        font-size: 21px;
    }

    .score-card {
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
        STEP 04 &nbsp; • &nbsp; PERFORMANCE ANALYSIS
    </div>

    <div class="hero-title">
        Your Interview Results.<br>
        Your Next Step to Success.
    </div>

    <div class="hero-description">
        Explore your interview performance, review personalized
        AI feedback, understand your strengths, and discover
        practical ways to improve your interview skills.
    </div>
</div>
""")


# ---------------------------------------------------------
# CHECK INTERVIEW COMPLETION
# ---------------------------------------------------------

questions = st.session_state.get("interview_questions", [])
evaluations = st.session_state.get("answer_evaluations", [])
answers = st.session_state.get("user_answers", [])

if not questions or not evaluations:

    st.html("""
    <div class="light-panel">
        <div class="panel-title">📋 No Interview Results Yet</div>
        <div class="panel-description">
            Complete a mock interview before viewing your
            performance analysis and final AI report.
        </div>
    </div>
    """)

    if st.button(
        "Go to Mock Interview →",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/3_Mock_Interview.py")

    st.stop()


if not st.session_state.get("interview_completed"):

    st.warning(
        "Your interview is not complete yet. "
        "Please answer all questions before generating your final report."
    )

    st.write(
        f"**Completed:** {len(evaluations)} of {len(questions)} questions"
    )

    if st.button(
        "Continue Mock Interview →",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/3_Mock_Interview.py")

    st.stop()


if len(evaluations) != len(questions):

    st.error(
        "The number of evaluations does not match the number "
        "of interview questions. Please check your interview progress."
    )

    st.stop()


if len(answers) != len(questions):

    st.error(
        "Some interview answers are missing. "
        "Please check your interview progress."
    )

    st.stop()


# ---------------------------------------------------------
# INTERVIEW SUMMARY
# ---------------------------------------------------------

st.html("""
<div class="section-eyebrow">SESSION OVERVIEW</div>
<div class="section-title">📋 Interview Summary</div>
<div class="section-description">
Your completed interview configuration and performance overview.
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


# ---------------------------------------------------------
# CALCULATE SCORES
# ---------------------------------------------------------

scores = [
    evaluation.get("score", 0)
    for evaluation in evaluations
]

if not all(
    isinstance(score, int)
    and not isinstance(score, bool)
    and 0 <= score <= 100
    for score in scores
):

    st.error(
        "Some evaluation scores are invalid. "
        "Please review your interview results."
    )

    st.stop()


average_score = round(sum(scores) / len(scores))
highest_score = max(scores)
lowest_score = min(scores)


# ---------------------------------------------------------
# PERFORMANCE OVERVIEW
# ---------------------------------------------------------

st.divider()

st.html("""
<div class="section-eyebrow">YOUR PERFORMANCE</div>
<div class="section-title">📈 Interview Score Overview</div>
<div class="section-description">
Understand your overall performance across all interview questions.
</div>
""")

score_information = [
    (
        "OVERALL AVERAGE",
        average_score,
        "Average score across all questions",
    ),
    (
        "HIGHEST SCORE",
        highest_score,
        "Your best individual answer",
    ),
    (
        "LOWEST SCORE",
        lowest_score,
        "Your lowest individual answer",
    ),
]

columns = st.columns(3)

for column, (label, value, caption) in zip(
    columns,
    score_information,
):

    with column:
        st.html(f"""
        <div class="score-card">
            <div class="score-label">{label}</div>
            <div class="score-value">{value}/100</div>
            <div class="score-caption">{caption}</div>
        </div>
        """)


# ---------------------------------------------------------
# INDIVIDUAL QUESTION SCORES
# ---------------------------------------------------------

st.divider()

st.html("""
<div class="section-eyebrow">QUESTION ANALYSIS</div>
<div class="section-title">📊 Question-wise Performance</div>
<div class="section-description">
Compare your scores across individual interview questions.
</div>
""")

score_data = {
    "Question": [
        f"Q{index + 1}"
        for index in range(len(scores))
    ],
    "Score": scores,
}

figure = px.bar(
    score_data,
    x="Question",
    y="Score",
    title="Your Score for Each Interview Question",
    range_y=[0, 110],
    text="Score",
    color="Score",
    color_continuous_scale=[
        "#bfdbfe",
        "#60a5fa",
        "#2563eb",
    ],
)

figure.update_traces(
    textposition="outside",
    marker_line_width=0,
)

figure.update_layout(
    yaxis_title="Score (out of 100)",
    xaxis_title="Interview Question",
    plot_bgcolor="#f8faff",
    paper_bgcolor="#f8faff",
    font=dict(
        family="Inter, sans-serif",
        color="#172554",
    ),
    title_font=dict(
        size=18,
        color="#172554",
    ),
    yaxis=dict(
        range=[0, 110],
        gridcolor="#dbeafe",
    ),
    xaxis=dict(
        gridcolor="#dbeafe",
    ),
    coloraxis_showscale=False,
    margin=dict(l=20, r=20, t=60, b=20),
)

st.plotly_chart(
    figure,
    use_container_width=True,
)


# ---------------------------------------------------------
# INDIVIDUAL EVALUATION DETAILS
# ---------------------------------------------------------

st.divider()

st.html("""
<div class="section-eyebrow">DETAILED FEEDBACK</div>
<div class="section-title">📝 Answer-by-Answer Analysis</div>
<div class="section-description">
Review your answers and understand the feedback Gemini provided.
</div>
""")

for index, evaluation in enumerate(evaluations):

    score = evaluation.get("score", 0)

    question_text = html.escape(
        str(questions[index].get("question", "Question unavailable."))
    )

    with st.expander(
        f"Question {index + 1}  |  Score: {score}/100"
    ):

        st.markdown("**Interview Question**")

        st.write(questions[index].get("question", "Question unavailable."))

        st.markdown("**Your Answer**")

        st.write(answers[index])

        st.metric(
            "Answer Score",
            f"{score}/100",
        )

        st.markdown("**AI Feedback**")

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
            st.caption("No improvement suggestions provided.")

        st.markdown("**Example of a Stronger Answer**")

        st.write(
            evaluation.get(
                "ideal_answer",
                "No example answer available.",
            )
        )


# ---------------------------------------------------------
# GENERATE FINAL AI REPORT
# ---------------------------------------------------------

st.divider()

st.html("""
<div class="section-eyebrow">PERSONALIZED AI INSIGHTS</div>
<div class="section-title">🤖 Final AI Performance Report</div>
<div class="section-description">
Get a complete summary of your interview, including your
strengths, improvement areas, and recommendations.
</div>
""")

if not st.session_state.get("final_report"):

    st.html("""
    <div class="light-panel">
        <div class="panel-title">Generate Your Personalized Report</div>
        <div class="panel-description">
            Gemini will analyze all your interview evaluations
            and prepare a final performance report with practical
            recommendations.
        </div>
    </div>
    """)

    if st.button(
        "✨ Generate Final Performance Report",
        type="primary",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Gemini is preparing your final performance report..."
            ):

                report = generate_final_report(
                    evaluations=evaluations,
                    job_role=st.session_state.get("job_role", ""),
                    interview_type=st.session_state.get(
                        "interview_type",
                        "",
                    ),
                    difficulty=st.session_state.get(
                        "difficulty",
                        "",
                    ),
                )

            st.session_state["final_report"] = report

            st.success(
                "Your final performance report is ready!"
            )

            st.rerun()

        except ValueError as error:

            st.error(str(error))

        except RuntimeError as error:

            st.error(str(error))

        except Exception:

            st.error(
                "An unexpected error occurred while generating "
                "your final report. Please try again."
            )


# ---------------------------------------------------------
# DISPLAY FINAL AI REPORT
# ---------------------------------------------------------

report = st.session_state.get("final_report")

if report:

    st.success("Your AI performance report is available.")

    report_score = report.get(
        "overall_score",
        average_score,
    )

    if (
        not isinstance(report_score, int)
        or isinstance(report_score, bool)
        or not 0 <= report_score <= 100
    ):
        report_score = average_score

    safe_summary = html.escape(
        str(
            report.get(
                "overall_summary",
                "No summary available.",
            )
        )
    )

    safe_level = html.escape(
        str(
            report.get(
                "performance_level",
                "Not specified",
            )
        )
    )

    st.html(f"""
    <div class="report-panel">
        <div class="report-label">GEMINI PERFORMANCE ANALYSIS</div>

        <div class="report-title">
            Your Interview Performance Report
        </div>

        <div class="report-text">
            {safe_summary}
        </div>

        <div class="report-score">
            {report_score}/100 &nbsp; • &nbsp; {safe_level}
        </div>
    </div>
    """)

    # Overall strengths.

    st.html("""
    <div class="section-title">💪 Overall Strengths</div>
    """)

    strengths = report.get("strengths", [])

    if strengths:
        for item in strengths:
            st.markdown(f"- {item}")
    else:
        st.caption("No strengths provided.")

    st.divider()

    # Areas for improvement.

    st.html("""
    <div class="section-title">📚 Areas for Improvement</div>
    """)

    areas = report.get("areas_for_improvement", [])

    if areas:
        for item in areas:
            st.markdown(f"- {item}")
    else:
        st.caption("No improvement areas provided.")

    st.divider()

    # Recommendations.

    st.html("""
    <div class="section-title">💡 Recommendations</div>
    """)

    recommendations = report.get("recommendations", [])

    if recommendations:
        for item in recommendations:
            st.markdown(f"- {item}")
    else:
        st.caption("No recommendations provided.")

    # Prepare downloadable report.

    report_content = {
        "job_role": st.session_state.get("job_role"),
        "interview_type": st.session_state.get("interview_type"),
        "difficulty": st.session_state.get("difficulty"),
        "question_scores": scores,
        "average_score": average_score,
        "highest_score": highest_score,
        "lowest_score": lowest_score,
        "detailed_evaluations": evaluations,
        "final_ai_report": report,
    }

    report_json = json.dumps(
        report_content,
        indent=4,
        ensure_ascii=False,
    )

    st.divider()

    st.html("""
    <div class="light-panel">
        <div class="panel-title">⬇️ Download Your Interview Report</div>
        <div class="panel-description">
            Keep a copy of your interview scores, individual
            evaluations, and final AI recommendations.
        </div>
    </div>
    """)

    st.download_button(
        label="⬇️ Download Interview Report (JSON)",
        data=report_json,
        file_name="interview_performance_report.json",
        mime="application/json",
        type="primary",
        use_container_width=True,
    )


# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------

st.divider()

st.html("""
<div class="section-eyebrow">KEEP IMPROVING</div>
<div class="section-title">What's Next?</div>
<div class="section-description">
You have completed your interview practice.
Continue preparing and keep improving your skills.
</div>
""")

if st.button(
    "← Return to Home",
    use_container_width=True,
):
    st.switch_page("app.py")

st.caption(
    "Your interview results are maintained temporarily in "
    "Streamlit Session State. They are not saved in a database."
)
