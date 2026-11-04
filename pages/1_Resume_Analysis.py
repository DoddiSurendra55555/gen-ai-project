
import html

import streamlit as st

from utils.helpers import (
    render_sidebar,
    initialize_session_state,
)
from utils.resume_parser import extract_text_from_pdf
from utils.ai_engine import analyze_resume


st.set_page_config(
    page_title="Resume Analysis",
    page_icon="📄",
    layout="wide",
)

initialize_session_state()
render_sidebar()


# ---------------------------------------------------------
# PROFESSIONAL DESIGN SYSTEM
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

.hero-panel {
    position: relative;
    overflow: hidden;
    background: linear-gradient(115deg, #172554 0%, #1e40af 55%, #2563eb 100%);
    border-radius: 22px;
    padding: 42px;
    margin-bottom: 35px;
    box-shadow: 0 14px 35px rgba(37, 99, 235, 0.16);
}

.hero-panel:after {
    content: "";
    position: absolute;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    background: rgba(255,255,255,0.07);
    right: -80px;
    top: -100px;
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
    margin-bottom: 20px;
}

.hero-title {
    color: #ffffff !important;
    font-size: clamp(32px, 4vw, 45px);
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: -1.5px;
    margin-bottom: 15px;
}

.hero-description {
    color: #dbeafe !important;
    font-size: 15px;
    line-height: 1.9;
    max-width: 750px;
}

.hero-points {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 25px;
}

.hero-point {
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.18);
    border-radius: 30px;
    color: #ffffff !important;
    font-size: 12px;
    padding: 9px 13px;
    font-weight: 600;
}

.section-eyebrow {
    color: #2563eb !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.7px;
    margin-bottom: 8px;
}

.section-title {
    color: #172554 !important;
    font-size: 25px;
    font-weight: 800;
    letter-spacing: -0.6px;
    margin-bottom: 8px;
}

.section-description {
    color: #64748b !important;
    font-size: 14px;
    line-height: 1.8;
    margin-bottom: 20px;
}

.upload-panel {
    background: linear-gradient(135deg, #eff6ff, #f8faff);
    border: 1px solid #dbeafe;
    border-radius: 19px;
    padding: 25px;
    margin-bottom: 15px;
}

.upload-icon {
    width: 54px;
    height: 54px;
    background: #dbeafe;
    border-radius: 15px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 27px;
    margin-bottom: 16px;
}

.upload-title {
    color: #172554 !important;
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 8px;
}

.upload-description {
    color: #64748b !important;
    font-size: 13px;
    line-height: 1.8;
}

.file-panel {
    background: #ffffff;
    border: 1px solid #dbeafe;
    border-radius: 14px;
    padding: 17px;
    margin: 12px 0 20px;
}

.file-label {
    color: #64748b !important;
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 6px;
}

.file-value {
    color: #172554 !important;
    font-size: 14px;
    font-weight: 700;
    overflow-wrap: anywhere;
}

.content-panel {
    background: #f4f8ff;
    border: 1px solid #dbeafe;
    border-radius: 17px;
    padding: 23px;
    margin-bottom: 16px;
    min-width: 0;
}

.panel-title {
    color: #172554 !important;
    font-size: 17px;
    font-weight: 800;
    margin-bottom: 13px;
}

.panel-content {
    color: #334155 !important;
    font-size: 14px;
    line-height: 1.85;
    overflow-wrap: anywhere;
    word-break: normal;
}

.panel-content ul {
    padding-left: 20px;
    margin-bottom: 0;
}

.panel-content li {
    color: #334155 !important;
    line-height: 1.8;
    margin-bottom: 7px;
}

.preview-panel {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 17px;
    padding: 22px;
}

.preview-heading {
    color: #172554 !important;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 8px;
}

.preview-description {
    color: #64748b !important;
    font-size: 13px;
    line-height: 1.8;
}

.ai-panel {
    background: linear-gradient(115deg, #172554, #2563eb);
    border-radius: 20px;
    padding: 30px;
    margin: 30px 0 18px;
    box-shadow: 0 10px 26px rgba(37,99,235,0.12);
}

.ai-label {
    color: #bfdbfe !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

.ai-title {
    color: #ffffff !important;
    font-size: 26px;
    font-weight: 800;
    margin-bottom: 10px;
}

.ai-description {
    color: #dbeafe !important;
    font-size: 14px;
    line-height: 1.8;
}

.candidate-panel {
    background: linear-gradient(135deg, #eff6ff, #ffffff);
    border: 1px solid #bfdbfe;
    border-radius: 17px;
    padding: 24px;
    margin-bottom: 17px;
}

.candidate-label {
    color: #64748b !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
    margin-bottom: 8px;
}

.candidate-name {
    color: #1d4ed8 !important;
    font-size: 26px;
    font-weight: 800;
    overflow-wrap: anywhere;
}

.results-heading {
    color: #172554 !important;
    font-size: 24px;
    font-weight: 800;
    margin-bottom: 8px;
}

.results-description {
    color: #64748b !important;
    font-size: 14px;
    line-height: 1.8;
    margin-bottom: 22px;
}

.stApp,
.stApp p,
.stApp label,
.stApp li,
.stApp [data-testid="stMarkdownContainer"] {
    color: #172554;
}

[data-testid="stWidgetLabel"] {
    color: #172554 !important;
}

.stTextInput input,
.stTextArea textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background: #ffffff !important;
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
    border: 1px solid #bfdbfe !important;
    caret-color: #2563eb !important;
}

.stTextArea textarea:disabled {
    background: #f0f6ff !important;
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
    opacity: 1 !important;
}

[data-baseweb="select"] > div {
    background: #ffffff !important;
    border-color: #bfdbfe !important;
}

[data-baseweb="select"] span,
[data-baseweb="select"] input {
    color: #172554 !important;
    -webkit-text-fill-color: #172554 !important;
}

[data-testid="stFileUploader"] {
    background: #ffffff;
    border: 1px dashed #93c5fd;
    border-radius: 15px;
    padding: 17px;
}

[data-testid="stFileUploader"] section {
    background: transparent !important;
}

[data-testid="stFileUploader"] button {
    background: #eff6ff !important;
    color: #1d4ed8 !important;
    border: 1px solid #bfdbfe !important;
}

[data-testid="stFileUploader"] small {
    color: #64748b !important;
}

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

[data-testid="stMetric"] {
    background: #f4f8ff;
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

[data-testid="stMetricDelta"] {
    color: #2563eb !important;
}

[data-testid="stExpander"] {
    background: #f8faff;
    border: 1px solid #dbeafe;
    border-radius: 12px;
}

[data-testid="stExpander"] summary {
    color: #172554 !important;
    font-weight: 700;
}

[data-testid="stAlert"] {
    border-radius: 12px;
}

hr {
    border-color: #e2e8f0;
}

@media (max-width: 700px) {
    [data-testid="stMainBlockContainer"] {
        padding: 1.2rem 1rem 2rem;
    }

    .hero-panel {
        padding: 27px 23px;
    }

    .hero-title {
        font-size: 30px;
    }

    .section-title {
        font-size: 21px;
    }

    .content-panel {
        padding: 17px;
    }

    .ai-panel {
        padding: 23px;
    }
}
</style>
""")


# ---------------------------------------------------------
# HERO SECTION
# ---------------------------------------------------------

st.html("""
<div class="hero-panel">
    <div class="hero-label">
        STEP 01 &nbsp; • &nbsp; SMART RESUME ANALYSIS
    </div>

    <div class="hero-title">
        Understand Your Resume.<br>
        Discover Your Strengths.
    </div>

    <div class="hero-description">
        Turn your resume into a personalized preparation plan.
        Let AI understand your skills, education, projects,
        and experience so you can prepare with confidence.
    </div>

    <div class="hero-points">
        <div class="hero-point">✓ Resume Insights</div>
        <div class="hero-point">✓ Skills Analysis</div>
        <div class="hero-point">✓ Improvement Suggestions</div>
    </div>
</div>
""")


# ---------------------------------------------------------
# UPLOAD SECTION
# ---------------------------------------------------------

st.html("""
<div class="section-eyebrow">GET STARTED</div>
<div class="section-title">Upload Your Resume</div>
<div class="section-description">
Start by uploading your PDF resume. We'll extract its text
before sending it for AI-powered analysis.
</div>

<div class="upload-panel">
    <div class="upload-icon">📄</div>
    <div class="upload-title">Your Resume, Your Next Opportunity</div>
    <div class="upload-description">
        Upload a PDF containing selectable text.<br>
        Maximum file size: 5 MB.
    </div>
</div>
""")

uploaded_file = st.file_uploader(
    "Choose your resume (PDF)",
    type=["pdf"],
    accept_multiple_files=False,
    help="Upload a PDF resume containing selectable text.",
)

if uploaded_file is not None:

    file_size_kb = uploaded_file.size / 1024

    st.html(f"""
    <div class="file-panel">
        <div class="file-label">SELECTED DOCUMENT</div>
        <div class="file-value">📄 {html.escape(uploaded_file.name)}</div>
        <div class="file-label" style="margin-top:12px">FILE SIZE</div>
        <div class="file-value">{file_size_kb:.2f} KB</div>
    </div>
    """)

    if uploaded_file.size > 5 * 1024 * 1024:

        st.error(
            "File size exceeds the 5 MB limit. "
            "Please upload a smaller PDF."
        )

    else:

        if st.button(
            "📄 Extract Resume Text",
            type="primary",
            use_container_width=True,
        ):

            try:

                pdf_bytes = uploaded_file.getvalue()

                with st.spinner(
                    "Extracting text from your resume..."
                ):
                    resume_text = extract_text_from_pdf(pdf_bytes)

                st.session_state["resume_text"] = resume_text
                st.session_state["uploaded_resume_name"] = uploaded_file.name
                st.session_state["resume_analysis"] = None

                st.success(
                    "Resume text extracted successfully!"
                )

            except ValueError as error:
                st.error(str(error))

            except Exception:
                st.error(
                    "An unexpected error occurred while processing "
                    "your resume. Please try again."
                )

else:

    st.info(
        "No file selected yet. Choose your PDF resume above."
    )


# ---------------------------------------------------------
# EXTRACTED RESUME PREVIEW
# ---------------------------------------------------------

resume_text = st.session_state.get("resume_text")

if resume_text:

    st.divider()

    st.html("""
    <div class="section-eyebrow">DOCUMENT PREVIEW</div>
    <div class="section-title">Extracted Resume Content</div>
    <div class="section-description">
    Review the extracted text to make sure your resume
    information has been processed correctly.
    </div>
    """)

    st.html(f"""
    <div class="preview-panel">
        <div class="preview-heading">📄
        {html.escape(st.session_state.get('uploaded_resume_name') or 'Resume')}
        </div>
        <div class="preview-description">
        Text successfully extracted and ready for AI analysis.
        </div>
    </div>
    """)

    st.text_area(
        "Resume text preview",
        value=resume_text,
        height=300,
        disabled=True,
    )

    st.caption(
        "Your extracted resume text is temporarily held "
        "in Streamlit Session State."
    )

else:

    st.info(
        "Your extracted resume preview will appear here "
        "after you process a PDF."
    )


# ---------------------------------------------------------
# AI ANALYSIS CALL TO ACTION
# ---------------------------------------------------------

st.html("""
<div class="ai-panel">
    <div class="ai-label">INTELLIGENT RESUME REVIEW</div>
    <div class="ai-title">🤖 Let AI Analyse Your Resume</div>
    <div class="ai-description">
        Discover your professional strengths, technical skills,
        experience, missing skills, and practical suggestions
        to improve your resume.
    </div>
</div>
""")

if resume_text:

    if st.button(
        "🤖 Analyze My Resume",
        type="primary",
        use_container_width=True,
    ):

        try:

            with st.spinner(
                "Gemini is analyzing your resume. Please wait..."
            ):

                analysis = analyze_resume(resume_text)

                st.session_state["resume_analysis"] = analysis

            # Rerun so browser storage receives the completed analysis.
            st.rerun()

        except ValueError as error:
            st.error(str(error))

        except RuntimeError as error:
            st.error(str(error))

        except Exception:
            st.error(
                "An unexpected error occurred during AI analysis. "
                "Please try again."
            )

else:

    st.button(
        "🤖 Analyze My Resume",
        disabled=True,
        use_container_width=True,
    )


# ---------------------------------------------------------
# RESULT CARD FUNCTION
# ---------------------------------------------------------

def display_result_card(title, items=None, description=None):
    """Display a consistent light-blue result card."""

    safe_title = html.escape(str(title))

    st.html(f"""
    <div class="content-panel">
        <div class="panel-title">{safe_title}</div>
    </div>
    """)

    if description:

        st.markdown(
            f'<div class="panel-content">{html.escape(str(description))}</div>',
            unsafe_allow_html=True,
        )

    if items:

        safe_items = "".join(
            f"<li>{html.escape(str(item))}</li>"
            for item in items
        )

        st.html(f"""
        <div class="panel-content">
            <ul>{safe_items}</ul>
        </div>
        """)

    elif items is not None:

        st.caption("No information identified.")


# ---------------------------------------------------------
# AI ANALYSIS RESULTS
# ---------------------------------------------------------

analysis = st.session_state.get("resume_analysis")

if analysis:

    st.divider()

    st.html("""
    <div class="hero-panel">
        <div class="hero-label">YOUR PERSONALIZED AI REPORT</div>
        <div class="hero-title">📊 Your Resume Insights</div>
        <div class="hero-description">
            Your resume has been analysed. Explore your profile,
            strengths, and opportunities for improvement.
        </div>
    </div>
    """)

    # Candidate information

    candidate_name = html.escape(
        str(analysis.get("name") or "Not identified")
    )

    st.html(f"""
    <div class="candidate-panel">
        <div class="candidate-label">CANDIDATE INFORMATION</div>
        <div class="candidate-name">👤 {candidate_name}</div>
    </div>
    """)

    # Professional summary

    display_result_card(
        "📝 Professional Summary",
        description=analysis.get("summary") or "No summary available.",
    )

    # Education and experience

    left_column, right_column = st.columns(2, gap="large")

    with left_column:

        display_result_card(
            "🎓 Education",
            items=analysis.get("education", []),
        )

    with right_column:

        display_result_card(
            "💼 Work Experience",
            items=analysis.get("work_experience", []),
        )

    # Skills

    left_column, right_column = st.columns(2, gap="large")

    with left_column:

        display_result_card(
            "🛠️ Technical Skills",
            items=analysis.get("technical_skills", []),
        )

    with right_column:

        display_result_card(
            "💻 Programming Languages",
            items=analysis.get("programming_languages", []),
        )

    # Projects and certifications

    left_column, right_column = st.columns(2, gap="large")

    with left_column:

        display_result_card(
            "🚀 Projects",
            items=analysis.get("projects", []),
        )

    with right_column:

        display_result_card(
            "📜 Certifications",
            items=analysis.get("certifications", []),
        )

    st.divider()

    st.html("""
    <div class="section-eyebrow">PERSONALIZED FEEDBACK</div>
    <div class="section-title">Your Resume Improvement Plan</div>
    <div class="section-description">
    Use these AI-generated insights to strengthen your profile
    and prepare more effectively for interviews.
    </div>
    """)

    # Strengths and weaknesses

    left_column, right_column = st.columns(2, gap="large")

    with left_column:

        display_result_card(
            "💪 Your Strengths",
            items=analysis.get("strengths", []),
        )

    with right_column:

        display_result_card(
            "⚠️ Areas to Improve",
            items=analysis.get("weaknesses", []),
        )

    # Skills and suggestions

    left_column, right_column = st.columns(2, gap="large")

    with left_column:

        display_result_card(
            "📚 Suggested Skills to Develop",
            items=analysis.get("missing_skills", []),
        )

    with right_column:

        display_result_card(
            "✨ Improvement Suggestions",
            items=analysis.get("improvement_suggestions", []),
        )

    st.html("""
    <div class="upload-panel">
        <div class="upload-card-title">🎯 What's Next?</div>
        <div class="upload-card-description">
        Your resume analysis is complete. Continue to Interview
        Setup to generate personalized questions based on your
        resume and target job role.
        </div>
    </div>
    """)

    if st.button(
        "Continue to Interview Setup →",
        type="primary",
        use_container_width=True,
    ):
        st.switch_page("pages/2_Interview_Setup.py")

    st.divider()

    st.caption(
        "This analysis is AI-generated and should be reviewed "
        "for accuracy. Your resume content is sent to Google's "
        "Gemini API for analysis and is not saved in a database."
    )
